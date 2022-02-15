from google.cloud import vision
from google.oauth2 import service_account
from dotenv import dotenv_values
import json
import os
import io
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import datetime
from dotmap import DotMap
import ocr.utils as utils
from ocr.logger import logging

def main(opts = dict()):
  """Scan driver's license.
  Args:
    opts.input: Image path or Data URL.
  Returns:
    Return the text detected from the driver's license.
  """
  logging.debug('begin')

  # Initialize options.
  opts = dict(input = None) | opts
  opts = DotMap(opts)
  print(f'opts.input={opts.input[:50]}')

  # Validate options.
  validOptions(opts)

  # load an image.
  if utils.isDataURL(opts.input):
    img = utils.toNdarray(opts.input)
  else:
    img = cv2.imread(opts.input)

  # Detect text from image.
  texts = detectText(img, utils.getMime(opts.input))
  exit()

  # Could not find the text in the image.
  if not texts:
    print('Text not found in image')
    return None

  # Find the rectangular point of the symbol from the result of document_text_detection.
  syms = findSymbolRectangle(texts, img)
  print('Sorted syms:')
  for sym in syms:
    print('\t', *sym.vertices, f':{sym.text}')

  # Get annotations.
  annots = loadAnnotationXML()
  print('annots:')
  for annot in annots:
    print('\t', *annot.rect, f':{annot.name}')

  # Draw annotation rectangle.
  ht, wd, _ = img.shape
  for annot in annots:
    pt1, _, pt2, _ = annot.rect
    cv2.rectangle(img,
      [round(pt1[0] * wd), round(pt1[1] * ht)],
      [round(pt2[0] * wd), round(pt2[1] * ht)],
      (0,0,255), 2)
  utils.show('symbol', img)

  # Template Matching.
  output = templateMatch(annots, syms)

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
  print('>>>>>>>>>>>>>>>>mime=', mime)
  exit()


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
  res = client.document_text_detection(image = vision.Image(content=content),
                                        image_context = vision.ImageContext(language_hints =['ja']))

  # Write OCR results to a file for debugging.
  now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  utils.writeJson(f'output/{now}.json', vision.AnnotateImageResponse.to_dict(res))

  # Returns None if the text cannot be found.
  if not res:
    return None

  # Returns the text detection result of the first image.
  return res.full_text_annotation.pages[0]

def findSymbolRectangle(texts, img, ndigits = 3):
  """Find the rectangular point of the symbol from the result of document_text_detection.
  Args:
    texts: Text detection result of document_text_detection.
    img: CV2 Image object.
    ndigits: Number of decimal places in the ratio of rectangular points.
  Returns:
    Returns a symbol rectangle point.
  """
  # Find the rectangular points of all the symbols.
  ht, wd, _ = img.shape
  syms = []
  for block in texts.blocks:
    for par in block.paragraphs:
      for word in par.words:
        for sym in word.symbols:
          # Convert the rectangular point of a symbol from px to ratio.
          syms.append(DotMap(dict(
            text = sym.text,
            rect = np.array([[round(pt.x / wd, ndigits), round(pt.y / ht, ndigits)] for pt in sym.bounding_box.vertices])
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
  tree = ET.parse('annotations/license.xml')
  root = tree.getroot()

  # Overall width and height of the image.
  size = root.find('size')
  wd = float(size.find('width').text)
  ht = float(size.find('height').text)

  # Coordinates for each field.
  annots = []
  for obj in root.findall('object'):
    # Convert points from px to ratios.
    bb = obj.find('bndbox')
    xmin = round(float(bb.find('xmin').text) / wd, ndigits)
    ymin = round(float(bb.find('ymin').text) / ht, ndigits)
    xmax = round(float(bb.find('xmax').text) / wd, ndigits)
    ymax = round(float(bb.find('ymax').text) / ht, ndigits)

    # To rectangular four points.
    annots.append(DotMap(dict(
      name = obj.find('name').text,
      rect = np.array(((xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)))
    )))
  return annots

def templateMatch(annots, syms, wd, ht):
  """Find the text rectangle adjacent to the template field rectangle and group the found text symbols as the field string.
  Args:
    annots: Template annotation.
    syms: Rectangle point of symbol.
    wd: Image width.
    ht: Image height.
  Returns:
    Text that matches the fields in the template.
  """
  # OCR results. The key is the field name and the value is the rectangular point and text..
  output = dict.fromkeys([annot.get('name') for annot in annots], None)
  for name in output:
    output[name] = DotMap(dict(text = '', rect = dict(xmin = .0, ymin = .0, xmax = .0, ymax = .0)))
  print(f'output={output}')

  # Loop annotation rectangle.
  for annot in annots:
    # Annotation rectangle point.
    annotRect = (annot.rect[0][0], annot.rect[0][1], annot.rect[2][0], annot.rect[2][1])
    for sym in syms:
      # Symbol rectangle point.
      symRect = (sym.rect[0][0], sym.rect[0][1], sym.rect[2][0], sym.rect[2][1])

      # Calculate IoU for annotation rectangles and symbol rectangles.
      iou, interArea, _, symArea = utils.calcIoU(annotRect, symRect)

      # Skip if template and symbol do not intersect.
      if iou == 0:
        continue

      # Intersection area / symbol rectangular area.
      overlapRatio = round(interArea / symArea, 3)
      print(f'{annot.name} -> {sym.text} (iou={iou}, overlapRatio={overlapRatio})')

      # When the area where the symbol rectangle and the annotation rectangle overlap is greater than or equal to the threshold value.
      if (overlapRatio) > .5:
        output[annot.name].text += sym.text
        rect = output[annot.name].rect
        rect.xmin = min(rect.xmin, symRect[0])
        rect.ymin
        rect.xmax
        rect.ymax

  print('Output:')
  for outpu in output.items():
    print('\t', outpu)