import argparse
import ocr
from ocr.logger import logging

def main():
  # Parse arguments.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input',
                      type=str,
                      required=True,
                      help='Image path or Data URL')
  parser.add_argument('-o', '--output',
                      type=str,
                      help='Output image path of the found document')
  # parser.add_argument('-r', '--aspect', type=str, help='Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).')
  parser.add_argument('-p', '--print',
                      action='store_true',
                      help='Print the Data URL of the detected document',
                      default=False)
  parser.add_argument('-t', '--type',
                      choices=['driverslicense', 'mynumber'],
                      required=True,
                      help='OCR document type')
  parser.add_argument('-d', '--debug',
                      action='store_true',
                      help='Display debug image on display',
                      default=False)
  opts = vars(parser.parse_args())

  # ID-1 format (driver's license, mine bar card, etc.).
  aspect = '8.56:5.4'

  # Detect document from image.
  dataURL = ocr.detect(dict(
    input = opts['input'],
    output = opts['output'],
    aspect = aspect,
    debug = opts['debug']))

  logging.debug(f'dataURL={dataURL[:50]}')
  if not dataURL:
    logging.debug('The document could not be detected from the image')
    exit()

  # OCR.
  matches = ocr.scan(dict(
    input = dataURL,
    type = opts['type'],
    debug = opts['debug']))

  if not matches:
    logging.debug('The text could not be detected')
    exit()
  
  for key, match in matches.items():
    logging.debug(f'{key} -> {match.text}')

if __name__ == '__main__':
  main()