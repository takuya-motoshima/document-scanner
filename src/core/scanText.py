import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import cv2
import numpy as np
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import dotenv_values
from dotmap import DotMap
from namedivider import NameDivider
import utils

def scanText(input, type, transformCallback = None):
  """Scanning text.
  Args:
      input (str): Image path or DataURL.
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      transformCallback (function, optional): Callback function for image transformation. Defaults to None.
  Raises:
      ValueError: The input parameter is incorrect.
      ValueError: The type parameter is incorrect.
  Returns:
      dotmap.DotMap: Text read from the image.
  """  
  # Validate parameters
  if (not utils.isDataUrl(input) and
      not os.path.exists(input) and
      not os.path.isfile(input)
  ):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')
  if type != 'driverslicense' and type != 'mynumber':
    raise ValueError('Incorrect type. Type can be "driverslicense" or "mynumber"')

  # Initialize transformation callbacks.
  if not transformCallback:
    transformCallback = lambda label, img: None

  # Load the image.
  if utils.isDataUrl(input):
    img = utils.toNdarray(input)
  else:
    img = cv2.imread(input)

  # Detect text from image.
  texts = _detectText(img, utils.getMime(input))
  if not texts:
    utils.logging.debug('Text not found in image')
    return None

  # Find the rectangular point of the symbol from the result of document_text_detection.
  symbols = _findSymbol(texts, img)

  # Get annotations.
  annotations = _loadAnnotation(type)
  transformCallback('Annotation rectangle', _drawAnnotationRectangle(img, annotations))

  # Find text that inscribes matches the field template rectangle.
  matches = _matching(annotations, symbols)
  transformCallback('Detected text rectangle', _drawDetectionTextRectangle(img, matches))

  # If there is a first name and last name, split the first name and last name.
  if (type == 'driverslicense' or type == 'mynumber') and matches['fullName']:
    divideName = NameDivider().divide_name(matches.fullName.text)
    matches.firstName = DotMap(text = divideName.given)
    matches.lastName = DotMap(text = divideName.family)
  return matches

def _detectText(img, mime):
  """Detect text from image.
  Args:
      img (numpy.ndarray): CV2 Image.
      mime (str): Image MIME type.
  Raises:
      RuntimeError: Cannot find .env file.
      RuntimeError: GOOGLE_APPLICATION_CREDENTIALS is not defined in .env.
  Returns:
      list: Text detection results.
  """
  # Load .env.
  envPath = './.env';
  if not os.path.exists(envPath):
    raise RuntimeError(f'{envPath} not found')
  env = dotenv_values(envPath)

  # Find google cloud credentials from ".env".
  if 'GOOGLE_APPLICATION_CREDENTIALS' not in env:
    raise RuntimeError('GOOGLE_APPLICATION_CREDENTIALS not found in ".env"')
  credentials = json.loads(env['GOOGLE_APPLICATION_CREDENTIALS'])
  
  # Loading private key (which contains line terminators like '\n') as an environment variable is tricky. Most shells would pad the terminator and treat it as a literal -- i.e. '\\n'. You will have to inspect how that value gets fed into your Python code, and preprocess/unpad accordingly.
  credentials['private_key'] = credentials['private_key'].replace('\\n', '\n')

  # Instantiates a client.
  client = vision.ImageAnnotatorClient(credentials = service_account.Credentials.from_service_account_info(credentials))

  # Detect text.
  content = cv2.imencode(f'.{mime}', img)[1].tostring()
  res = client.document_text_detection(
    image = vision.Image(content=content),
    image_context = vision.ImageContext(language_hints =['ja']))

  # Write OCR results to a file for debugging.
  utils.writeJson(f'logs/response_{utils.getNow("%Y%m%d%H%M%S")}.json', vision.AnnotateImageResponse.to_dict(res))

  # Returns None if the text cannot be found.
  if not res:
    return None

  # Returns the text detection result of the first image.
  return res.full_text_annotation.pages[0]

def _findSymbol(texts, img, ndigits = 3):
  """Find the rectangular point of the symbol from the result of document_text_detection.
  Args:
      texts (list): Text detection result of document_text_detection.
      img (numpy.ndarray): CV2 Image.
      ndigits (int, optional): Number of decimal places in the ratio of rectangular points. Defaults to 3.
  Returns:
      list: List of text coordinates.
  """
  # Find the rectangular points of all the symbols.
  height, width, _ = img.shape
  symbols = []
  for block in texts.blocks:
    for par in block.paragraphs:
      for word in par.words:
        for sym in word.symbols:
          # Convert the rectangular point of a symbol from px to ratio.
          symbols.append(DotMap(
            text = sym.text,
            rect = np.array([[round(pt.x / width, ndigits), round(pt.y / height, ndigits)] for pt in sym.bounding_box.vertices])
          ))

  # Sort the symbol rectangles from top left to bottom right.
  return sorted(symbols, key=lambda sym: np.linalg.norm(np.array((sym.rect[0][0], sym.rect[0][1])) - np.array([0,0])))

def _loadAnnotation(type, ndigits = 3):
  """Returns the rectangular point of the OCR field.
  Args:
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      ndigits (int, optional): _description_. Defaults to 3.
  Returns:
      list: Returns a list where the key is the field name and the value is a rectangular point. The points of the rectangle are in the order of upper left, upper right, lower right, lower left.
  """  
  # Annotation XML to load.
  srcDir = Path(__file__).resolve().parents[1]
  if type == 'driverslicense':
    xmlPath = f'{srcDir}/annotations/driverslicense.xml'
  elif type == 'mynumber':
    xmlPath = f'{srcDir}/annotations/mynumber.xml'

  # Parse XML.
  tree = ET.parse(xmlPath)
  root = tree.getroot()

  # Overall width and height of the image.
  size = root.find('size')
  width = float(size.find('width').text)
  height = float(size.find('height').text)

  # Coordinates for each field.
  annotations = []
  for obj in root.findall('object'):
    # Convert points from px to ratios.
    bb = obj.find('bndbox')
    xmin = round(float(bb.find('xmin').text) / width, ndigits)
    ymin = round(float(bb.find('ymin').text) / height, ndigits)
    xmax = round(float(bb.find('xmax').text) / width, ndigits)
    ymax = round(float(bb.find('ymax').text) / height, ndigits)

    # To rectangular four points.
    annotations.append(DotMap(
      name = obj.find('name').text,
      rect = np.array(((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)))
    ))
  return annotations

def _matching(annotations, symbols, ):
  """Find text that inscribes matches the field template rectangle.
  Args:
      annotations (list): Template annotation.
      symbols (list): Rectangle point of symbol.
  Returns:
      dotmap.DotMap: Returns the found text.
  """
  # Initialize the return value. (Key is field name, value is rectangular point and text).
  matches = DotMap.fromkeys([annotation.get('name') for annotation in annotations])
  for name in matches:
    matches[name] = DotMap(text = '', rect = DotMap(xmin = None, ymin = None, xmax = None, ymax = None))

  # Annotation and text overlap rate threshold.
  thresholdRateOfOverlap = .5

  # Read the field coordinates of the template.
  for annotation in annotations:
    # Template field rectangle.
    annotationXmin = annotation.rect[0][0]
    annotationYmin = annotation.rect[0][1]
    annotationXmax = annotation.rect[2][0]
    annotationYmax = annotation.rect[2][1]
    for symbol in symbols:
      # Detected text symbol rectangle.
      symbolXmin = symbol.rect[0][0]
      symbolYmin = symbol.rect[0][1]
      symbolXmax = symbol.rect[2][0]
      symbolYmax = symbol.rect[2][1]

      # Skip if template and symbol do not intersect.
      iou, interArea, _, symbolArea = utils.calcIoU(
        (annotationXmin, annotationYmin, annotationXmax, annotationYmax),
        (symbolXmin, symbolYmin, symbolXmax, symbolYmax))
      if iou == 0:
        continue

      # Calculate the overlap between the template field and the detected text symbol.
      ratio = round(interArea / symbolArea, 3)

      # # Debug template fields and detected text.
      # utils.logging.debug(f'{annotation.name} -> {symbol.text} (iou={iou}, ratio={ratio})')

      # If the overlap rate between the template and the text is less than a certain value, the text is not retrieved.
      if ratio < thresholdRateOfOverlap:
        continue
      matches[annotation.name].text += symbol.text
      matches[annotation.name].rect.xmin = symbolXmin if matches[annotation.name].rect.xmin is None or symbolXmin < matches[annotation.name].rect.xmin else matches[annotation.name].rect.xmin
      matches[annotation.name].rect.ymin = symbolYmin if matches[annotation.name].rect.ymin is None or symbolYmin < matches[annotation.name].rect.ymin else matches[annotation.name].rect.ymin
      matches[annotation.name].rect.xmax = symbolXmax if matches[annotation.name].rect.xmax is None or symbolXmax > matches[annotation.name].rect.xmax else matches[annotation.name].rect.xmax
      matches[annotation.name].rect.ymax = symbolYmax if matches[annotation.name].rect.ymax is None or symbolYmax > matches[annotation.name].rect.ymax else matches[annotation.name].rect.ymax
  return matches

def _drawAnnotationRectangle(img, annotations):
  """Draw annotation rectangle.
  Args:
      img (numpy.ndarray): CV2 Image.
      annotations (list): Template annotation.
  Returns:
      numpy.ndarray: CV2 Image.
  """
  tmpImg = img.copy()
  height, width, _ = tmpImg.shape
  for annotation in annotations:
    pt1, _, pt2, _ = annotation.rect
    cv2.rectangle(tmpImg,
      [round(pt1[0] * width), round(pt1[1] * height)],
      [round(pt2[0] * width), round(pt2[1] * height)],
      (0,255,0), 3)
  return tmpImg

def _drawDetectionTextRectangle(img, matches):
  """Drawing detection text rectangle.
  Args:
      img (numpy.ndarray): CV2 Image.
      matches (dict): Detected text rectangle.
  Returns:
      numpy.ndarray: CV2 Image.
  """
  tmpImg = img.copy()
  height, width, _ = tmpImg.shape
  for key, match in matches.items():
    if not match.text:
      continue
    cv2.rectangle(tmpImg,
      [round(match.rect.xmin * width), round(match.rect.ymin * height)],
      [round(match.rect.xmax * width), round(match.rect.ymax * height)],
      (0,255,0), 3)
  return tmpImg