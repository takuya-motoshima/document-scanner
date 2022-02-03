from pprint import pprint
from turtle import width
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import dotenv_values
import json
import os
import io
import pprint
import utils
import cv2
import numpy as np
import xml.etree.ElementTree as ET
import datetime
from dotmap import DotMap

def main(isDebug = True):
  # Number of decimal places in template and detection result rectangle.
  NDIGITS = 3

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

  # Loads the image into memory.
  imgPath = 'img/license_only_name_and_birthday.png'
  with io.open(imgPath, 'rb') as f:
    content = f.read()

  # OCR the image.
  res = client.document_text_detection(image = vision.Image(content=content),
                                        image_context = vision.ImageContext(language_hints =['ja']))

  # Could not find the text in the image.
  if not res:
    print('Text not found in image')
    return None
  if isDebug:
    print(f'Block count: {len(res.full_text_annotation.pages[0].blocks)}')

  # Write OCR results to a file for debugging.
  now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  utils.writeJson(f'output/{now}.json', vision.AnnotateImageResponse.to_dict(res))
  
  # Get annotations.
  annots = loadAnnotation(NDIGITS)
  if isDebug:
    print('annots:')
    for annot in annots:
      print('\t', *annot.rect, f':{annot.key}')

  # Find the rectangular points of all the symbols.
  img = cv2.imread(imgPath)
  ht, wd, _ = img.shape
  if isDebug:
    print(f'Image size: {wd}/{ht}')
  rects = []
  for block in res.full_text_annotation.pages[0].blocks:
    for par in block.paragraphs:
      for word in par.words:
        for symbol in word.symbols:
          # Convert the rectangular point of a symbol from px to ratio.
          rects.append(DotMap(dict(
            text = symbol.text,
            rect = np.array([[round(pt.x / wd, NDIGITS), round(pt.y / ht, NDIGITS)] for pt in symbol.bounding_box.vertices])
          )))  
  if isDebug:
    print('rects:')
    for rect in rects:
      print('\t', *rect.rect, f':{rect.text}')

  # Sort the symbol rectangles from top left to bottom right.
  rects = sorted(rects, key=lambda rect: np.linalg.norm(np.array((rect.rect[0][0], rect.rect[0][1])) - np.array([0,0])))
  if isDebug:
    print('Sorted rects:')
    for rect in rects:
      print('\t', *rect.rect, f':{rect.text}')
  
  # Template Matching.
  output = dict(name = [])
  loop = 0
  for annot in annots:
    for rect in rects:
      loop+=1
      pass
  print(f'loop={loop}')

def loadAnnotation(ndigits = 3):
  """Returns the rectangular point of the OCR field.
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
  # print(f'wd={wd}')
  # print(f'ht={ht}')

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
      key = obj.find('name').text,
      rect = np.array([
        [xmin, ymin],
        [xmax, ymin],
        [xmax, ymax],
        [xmin, ymax]
      ])
    )))
  return annots

if __name__ == '__main__':
  main()
