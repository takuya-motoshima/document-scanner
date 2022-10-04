import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import cv2
import numpy as np
from google.cloud import vision
from dotmap import DotMap
from namedivider import NameDivider
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utils
from normalize_japanese_addresses import normalize

def scan_text(img, type, scan_fields = None, debug_img_callback = None):
  """Scanning text.
  Args:
      img (str): Image path or DataURL.
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      scan_fields (list, optional): Fields to be scanned. Defaults to None(all fields).
      debug_img_callback (function, optional): Callback function for image transformation. Defaults to None.
  Returns:
      dotmap.DotMap: Text read from the image.
  Raises:
      ValueError: The img parameter is incorrect.
      ValueError: The type parameter is incorrect.
  """
  _validate_params(img, type)
  _set_field_to_calc_age(scan_fields)
  if not debug_img_callback:
    debug_img_callback = lambda label, img: None
  mime_type = utils.get_mime_type(img)
  img = utils.load_img(img)
  page = _detect_text(img, mime_type)
  if not page:
    utils.logging.debug('Text not found in image')
    return DotMap()
  symbols = _get_text_and_rectangle_coordinates(page, img)
  annots = _load_annotation(type, scan_fields)
  debug_img_callback('annotation', _draw_annotation_rectangle(img, annots))

  # Find text that inscribes matches the field template rectangle.
  matches = _matching(annots, symbols)
  debug_img_callback('detected', _draw_detection_text_rectangle(img, matches))

  # If a driver's license or my number card.
  if type == 'driverslicense' or type == 'mynumber':
    if 'fullName' in matches:
      # If there is a first name and last name, split the first name and last name.
      matches.firstName = DotMap(text = '')
      matches.lastName = DotMap(text = '')
      if matches.fullName.text:
        divide_name = NameDivider().divide_name(matches.fullName.text)
        matches.firstName.text = divide_name.given
        matches.lastName.text = divide_name.family

    if 'birthday' in matches:
      # Clean up the Japanese calendar birthdays.
      matches.birthday.text = utils.cleanup_japanese_birthday(matches.birthday.text)

      # Birthdays in Western calendar format.
      matches.wrnBirthday = DotMap(text = '')
      if matches.birthday.text:
        matches.wrnBirthday.text = utils.to_western_date(matches.birthday.text)

      # Calculate age from birthday.
      matches.age = DotMap(text = '')
      if matches.wrnBirthday.text:
        matches.age.text = utils.calc_age(matches.wrnBirthday.text)

    # Clean up the expiration date.
    if type == 'driverslicense' and 'expiryDate' in matches:
      matches.expiryDate.text = utils.cleanup_japanese_expiration_date(matches.expiryDate.text)
    elif type == 'mynumber':
      if 'cardExpiryDate' in matches:
        matches.cardExpiryDate.text = utils.cleanup_japanese_expiration_date(matches.cardExpiryDate.text)
      if 'digiExpiryDate' in matches:
        matches.digiExpiryDate.text = utils.cleanup_japanese_expiration_date(matches.digiExpiryDate.text)

    # Normalized address.
    if 'address' in matches:
      matches.normalizedAddress = DotMap(
        pref = DotMap(text = ''),
        city = DotMap(text = ''),
        town = DotMap(text = ''),
        addr = DotMap(text = '')
      )
      if matches.address.text:
        normalized = normalize(matches.address.text)
        matches.normalizedAddress.pref.text = normalized['pref']
        matches.normalizedAddress.city.text = normalized['city']
        matches.normalizedAddress.town.text = normalized['town']
        matches.normalizedAddress.addr.text = normalized['addr']
  return matches

def _validate_params(img, type):
  if (not utils.is_data_url(img) and not os.path.exists(img) and not os.path.isfile(img)):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')
  if type != 'driverslicense' and type != 'mynumber':
    raise ValueError('Incorrect type. Type can be "driverslicense" or "mynumber"')

def _set_field_to_calc_age(scan_fields):
  # If the scan item has age, add the date of birth to the scan item because the calculation of age requires the date of birth.
  if scan_fields and 'age' in scan_fields and 'birthday' not in scan_fields:
    scan_fields.append('birthday')

def _detect_text(img, mime_type):
  client = utils.instantiate_image_annotator_client(f'{Path(__file__).parents[2]}/.env')
  encoded = cv2.imencode(f'.{mime_type}', img)[1].tostring()
  res = client.document_text_detection(image = vision.Image(content=encoded), image_context = vision.ImageContext(language_hints =['ja']))
  utils.write_json(f'logs/response_{utils.get_now("%Y%m%d%H%M%S")}.json', vision.AnnotateImageResponse.to_dict(res))
  if not res:
    return None
  return res.full_text_annotation.pages[0]

def _get_text_and_rectangle_coordinates(page, img, ndigits = 3):
  """Get the text and position coordinates of the symbol.
  Args:
      page (list): Text detection result of document_text_detection.
      img (numpy.ndarray): CV2 Image.
      ndigits (int, optional): Number of decimal places in the ratio of rectangular points. Defaults to 3.
  Returns:
      list: List of symbols found (text and position coordinates)
  """
  height, width, _ = img.shape
  symbols = []
  for block in page.blocks:
    for paragraph in block.paragraphs:
      for word in paragraph.words:
        for symbol in word.symbols:
          # Convert symbol coordinates from px to ratio.
          symbols.append(DotMap(
            text = symbol.text,
            rect = np.array([[round(pt.x / width, ndigits), round(pt.y / height, ndigits)] for pt in symbol.bounding_box.vertices])
          ))
  # Sort symbols by position (top left to bottom right).
  return sorted(symbols, key=lambda sym: np.linalg.norm(np.array((sym.rect[0][0], sym.rect[0][1])) - np.array([0,0])))

def _load_annotation(type, scan_fields = None, ndigits = 3):
  """Returns the rectangular point of the OCR field.
  Args:
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      scan_fields (list, optional): Fields to be scanned. Defaults to None(all fields).
      ndigits (int, optional): _description_. Defaults to 3.
  Returns:
      list: Returns a list where the key is the field name and the value is a rectangular point. The points of the rectangle are in the order of upper left, upper right, lower right, lower left.
  """  
  # Annotation XML to load.
  src_dir = Path(__file__).parents[1]
  if type == 'driverslicense':
    xml_path = f'{src_dir}/annotations/driverslicense.xml'
  elif type == 'mynumber':
    xml_path = f'{src_dir}/annotations/mynumber.xml'

  # Parse XML.
  tree = ET.parse(xml_path)
  root = tree.getroot()

  # Overall width and height of the image.
  size = root.find('size')
  width = float(size.find('width').text)
  height = float(size.find('height').text)

  # Coordinates for each field.
  annots = []
  for obj in root.findall('object'):
    # Annotation Item Name.
    name = obj.find('name').text

    # If a scan item is specified.
    if scan_fields and name not in scan_fields:
      # No items other than the specified scan items are read.
      continue

    # Convert points from px to ratios.
    bb = obj.find('bndbox')
    xmin = round(float(bb.find('xmin').text) / width, ndigits)
    ymin = round(float(bb.find('ymin').text) / height, ndigits)
    xmax = round(float(bb.find('xmax').text) / width, ndigits)
    ymax = round(float(bb.find('ymax').text) / height, ndigits)

    # To rectangular four points.
    annots.append(DotMap(
      name = name,
      rect = np.array(((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)))
    ))
  return annots

def _matching(annots, symbols):
  """Find text that inscribes matches the field template rectangle.
  Args:
      annots (list): Template annotation.
      symbols (list): Rectangle point of symbol.
  Returns:
      dotmap.DotMap: Returns the found text.
  """
  # Initialize the return value. (Key is field name, value is rectangular point and text).
  matches = DotMap.fromkeys([annot.get('name') for annot in annots])
  for name in matches:
    matches[name] = DotMap(text = '', rect = DotMap(xmin = None, ymin = None, xmax = None, ymax = None))

  # Annotation and text overlap rate threshold.
  threshold_rate_of_overlap = .5

  # Read the field coordinates of the template.
  for annot in annots:
    # Template field rectangle.
    annot_xmin = annot.rect[0][0]
    annot_ymin = annot.rect[0][1]
    annot_xmax = annot.rect[2][0]
    annot_ymax = annot.rect[2][1]
    for symbol in symbols:
      # Detected text symbol rectangle.
      symbol_xmin = symbol.rect[0][0]
      symbol_ymin = symbol.rect[0][1]
      symbol_xmax = symbol.rect[2][0]
      symbol_ymax = symbol.rect[2][1]

      # Skip if template and symbol do not intersect.
      iou, inter_area, _, symbol_area = utils.calc_iou(
        (annot_xmin, annot_ymin, annot_xmax, annot_ymax),
        (symbol_xmin, symbol_ymin, symbol_xmax, symbol_ymax))
      if iou == 0:
        continue

      # Calculate the overlap between the template field and the detected text symbol.
      ratio = round(inter_area / symbol_area, 3)

      # If the overlap rate between the template and the text is less than a certain value, the text is not retrieved.
      if ratio < threshold_rate_of_overlap:
        continue
      matches[annot.name].text += symbol.text
      matches[annot.name].rect.xmin = symbol_xmin if matches[annot.name].rect.xmin is None or symbol_xmin < matches[annot.name].rect.xmin else matches[annot.name].rect.xmin
      matches[annot.name].rect.ymin = symbol_ymin if matches[annot.name].rect.ymin is None or symbol_ymin < matches[annot.name].rect.ymin else matches[annot.name].rect.ymin
      matches[annot.name].rect.xmax = symbol_xmax if matches[annot.name].rect.xmax is None or symbol_xmax > matches[annot.name].rect.xmax else matches[annot.name].rect.xmax
      matches[annot.name].rect.ymax = symbol_ymax if matches[annot.name].rect.ymax is None or symbol_ymax > matches[annot.name].rect.ymax else matches[annot.name].rect.ymax
  return matches

def _draw_annotation_rectangle(img, annots):
  """Draw annotation rectangle.
  Args:
      img (numpy.ndarray): CV2 Image.
      annots (list): Template annotation.
  Returns:
      numpy.ndarray: CV2 Image.
  """
  tmp_img = img.copy()
  height, width, _ = tmp_img.shape
  for annot in annots:
    pt1, _, pt2, _ = annot.rect
    cv2.rectangle(tmp_img,
      [round(pt1[0] * width), round(pt1[1] * height)],
      [round(pt2[0] * width), round(pt2[1] * height)],
      (0,255,0), 3)
  return tmp_img

def _draw_detection_text_rectangle(img, matches):
  """Drawing detection text rectangle.
  Args:
      img (numpy.ndarray): CV2 Image.
      matches (dict): Detected text rectangle.
  Returns:
      numpy.ndarray: CV2 Image.
  """
  tmp_img = img.copy()
  height, width, _ = tmp_img.shape
  for _, match in matches.items():
    if not match.text:
      continue
    cv2.rectangle(tmp_img,
      [round(match.rect.xmin * width), round(match.rect.ymin * height)],
      [round(match.rect.xmax * width), round(match.rect.ymax * height)],
      (0,255,0), 3)
  return tmp_img