from google.cloud import vision
from google.oauth2 import service_account
from dotenv import dotenv_values
import json
import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import datetime
from dotmap import DotMap
import ocr.utils as utils
from ocr.logger import logging

def main(opts = dict()):
  """Scan document.
  Args:
    opts.input: Image path or Data URL.
  Returns:
    Return the text detected from the document.
  """
  logging.debug('begin')

  # Initialize options.
  opts = dict(input = None) | opts
  opts = DotMap(opts)
  logging.debug(f'opts.input={opts.input[:50]}')

  # Validate options.
  validOptions(opts)

  # load an image.
  if utils.isDataURL(opts.input):
    img = utils.toNdarray(opts.input)
  else:
    img = cv2.imread(opts.input)

  # Detect text from image.
  texts = detectText(img, utils.getMime(opts.input))
  if not texts:
    # Could not find the text in the image.
    logging.debug('Text not found in image')
    return None

  # Find the rectangular point of the symbol from the result of document_text_detection.
  syms = findRectangleSymbol(texts, img)
  # logging.debug(f'syms={syms}')

  # Get annotations.
  annots = loadAnnotationXML()
  # logging.debug(f'annots={annots}')

  # Show annotation rectangle for debugging.
  showAnnotationRectangle(img, annots)

  # Find text that inscribes matches the field template rectangle.
  matches = matching(annots, syms)

  # Show detected text rectangles for debugging.
  showDetectedTextRectangle(img, matches)

  return matches

def validOptions(opts): 
  """Validate options.
  Args:
    opts.input: Image path or Data URL.
  Raises:
    ValueError: If there are invalid options
  """
  # input option required.
  if not opts.input:
    raise ValueError('input option required')

  # Input options only allow image path or data URL.
  if not utils.isDataURL(opts.input) and not os.path.exists(opts.input) and os.path.isfile(opts.input):
    raise ValueError(f'{opts.input} Image file not found')

def detectText(img, mime):
  """Detect text from image.
  Args:
    img: CV2 Image object.
  Returns
    Returns text detection result.
  """
  # Load .env.
  envPath = './.env';
  if not os.path.exists(envPath):
    raise RuntimeError(f'{envPath} not found')
  config = dotenv_values(envPath)

  # Find google cloud credentials from ".env".
  if 'GOOGLE_CREDS' not in config:
    raise RuntimeError('GOOGLE_CREDS not found in ".env"')
  creds = json.loads(config['GOOGLE_CREDS'])
  
  # Instantiates a client.
  client = vision.ImageAnnotatorClient(credentials = service_account.Credentials.from_service_account_info(creds))

  # Detect text.
  content = cv2.imencode(f'.{mime}', img)[1].tostring()
  res = client.document_text_detection(
    image = vision.Image(content=content),
    image_context = vision.ImageContext(language_hints =['ja']))

  # Write OCR results to a file for debugging.
  now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  utils.writeJson(f'output/text_detection_{now}.json', vision.AnnotateImageResponse.to_dict(res))

  # Returns None if the text cannot be found.
  if not res:
    return None

  # Returns the text detection result of the first image.
  return res.full_text_annotation.pages[0]

def findRectangleSymbol(texts, img, ndigits = 3):
  """Find the rectangular point of the symbol from the result of document_text_detection.
  Args:
    texts: Text detection result of document_text_detection.
    img: CV2 Image object.
    ndigits: Number of decimal places in the ratio of rectangular points.
  Returns:
    Returns a symbol rectangle point.
  """
  # Find the rectangular points of all the symbols.
  height, width, _ = img.shape
  syms = []
  for block in texts.blocks:
    for par in block.paragraphs:
      for word in par.words:
        for sym in word.symbols:
          # Convert the rectangular point of a symbol from px to ratio.
          syms.append(DotMap(dict(
            text = sym.text,
            rect = np.array([[round(pt.x / width, ndigits), round(pt.y / height, ndigits)] for pt in sym.bounding_box.vertices])
          )))  

  # Sort the symbol rectangles from top left to bottom right.
  return sorted(syms, key=lambda sym: np.linalg.norm(np.array((sym.rect[0][0], sym.rect[0][1])) - np.array([0,0])))

def loadAnnotationXML(ndigits = 3):
  """Returns the rectangular point of the OCR field.
  Args:
    ndigits: Number of decimal places in the ratio of rectangular points.
  Returns:
    Returns a list where the key is the field name and the value is a rectangular point.
    The points of the rectangle are in the order of upper left, upper right, lower right, lower left.
  """
  # Parse XML.
  tree = ET.parse('./ocr/annotations/license.xml')
  root = tree.getroot()

  # Overall width and height of the image.
  size = root.find('size')
  width = float(size.find('width').text)
  height = float(size.find('height').text)

  # Coordinates for each field.
  annots = []
  for obj in root.findall('object'):
    # Convert points from px to ratios.
    bb = obj.find('bndbox')
    xmin = round(float(bb.find('xmin').text) / width, ndigits)
    ymin = round(float(bb.find('ymin').text) / height, ndigits)
    xmax = round(float(bb.find('xmax').text) / width, ndigits)
    ymax = round(float(bb.find('ymax').text) / height, ndigits)

    # To rectangular four points.
    annots.append(DotMap(dict(
      name = obj.find('name').text,
      rect = np.array(((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)))
    )))
  return annots

def matching(annots, syms):
  """Find text that inscribes matches the field template rectangle.
  Args:
    annots: Template annotation.
    syms: Rectangle point of symbol.
  Returns:
    Returns the found text.
  """
  # Initialize the return value. (Key is field name, value is rectangular point and text).
  matches = dict.fromkeys([annot.get('name') for annot in annots], None)
  for name in matches:
    matches[name] = DotMap(dict(
      text = '',
      rect = dict(xmin = None, ymin = None, xmax = None, ymax = None)
    ))

  # Read the field coordinates of the template.
  for annot in annots:
    # Template field rectangle.
    annotXmin = annot.rect[0][0]
    annotYmin = annot.rect[0][1]
    annotXmax = annot.rect[2][0]
    annotYmax = annot.rect[2][1]
    for sym in syms:
      # Detected text symbol rectangle.
      symXmin = sym.rect[0][0]
      symYmin = sym.rect[0][1]
      symXmax = sym.rect[2][0]
      symYmax = sym.rect[2][1]

      # Skip if template and symbol do not intersect.
      iou, interArea, _, symArea = utils.calcIoU(
        (annotXmin, annotYmin, annotXmax, annotYmax),
        (symXmin, symYmin, symXmax, symYmax))
      if iou == 0:
        continue

      # Calculate the overlap between the template field and the detected text symbol.
      ratio = round(interArea / symArea, 3)
      logging.debug(f'{annot.name} -> {sym.text} (iou={iou}, ratio={ratio})')

      # If the template field and the detection text are inscribed, get that text.
      if ratio > .5:
        matches[annot.name].text += sym.text
        matches[annot.name].rect.xmin = symXmin if matches[annot.name].rect.xmin is None or symXmin < matches[annot.name].rect.xmin else matches[annot.name].rect.xmin
        matches[annot.name].rect.ymin = symYmin if matches[annot.name].rect.ymin is None or symYmin < matches[annot.name].rect.ymin else matches[annot.name].rect.ymin
        matches[annot.name].rect.xmax = symXmax if matches[annot.name].rect.xmax is None or symXmax > matches[annot.name].rect.xmax else matches[annot.name].rect.xmax
        matches[annot.name].rect.ymax = symYmax if matches[annot.name].rect.ymax is None or symYmax > matches[annot.name].rect.ymax else matches[annot.name].rect.ymax
  return matches

def showAnnotationRectangle(img, annots):
  """Show annotation rectangle.
  Args:
    img: CV2 Image object.
    annots: Template annotation.
  """
  tmpImg = img.copy()
  height, width, _ = tmpImg.shape
  for annot in annots:
    pt1, _, pt2, _ = annot.rect
    cv2.rectangle(tmpImg,
      [round(pt1[0] * width), round(pt1[1] * height)],
      [round(pt2[0] * width), round(pt2[1] * height)],
      (0,0,255), 2)
  utils.show('Annotation rectangle', tmpImg)

def showDetectedTextRectangle(img, matches):
  """Show detected text rectangle.
  Args:
    img: CV2 Image object.
    matches: Detected text rectangle.
  """
  tmpImg = img.copy()
  height, width, _ = tmpImg.shape
  for key, match in matches.items():
    cv2.rectangle(tmpImg,
      [round(match.rect.xmin * width), round(match.rect.ymin * height)],
      [round(match.rect.xmax * width), round(match.rect.ymax * height)],
      (0,0,255), 2)
  utils.show('Detected text rectangle', tmpImg)
