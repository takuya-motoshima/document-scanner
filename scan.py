import argparse
import ocr
# from ocr.logger import logging
# from pprint import pprint

def main():
  # Parse arguments.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  # parser.add_argument('-r', '--aspect', type=str, help='Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).')
  parser.add_argument('-p', '--print-data-url', dest='printDataURL', action='store_true', help='Print the Dat URL of the document')
  parser.add_argument('-t', '--type', choices=['driverslicense', 'mynumber'], required=True, dest='type', help='OCR document type')
  opts = vars(parser.parse_args())

  # ID-1 format (driver's license, mine bar card, etc.).
  aspect = '8.56:5.4'

  # Detect document from image.
  dataURL = ocr.detect(dict(
    input = opts['input'],
    output = opts['output'],
    aspect = aspect))

  print(f'dataURL={dataURL[:50]}')
  if not dataURL:
    print('The document could not be detected from the image')
    exit()

  # OCR.
  matches = ocr.scan(dict(
    input = dataURL,
    type = opts['type']))

  if not matches:
    print('The text could not be detected')
    exit()
  
  for key, match in matches.items():
    print(f'{key} -> {match.text}')

if __name__ == '__main__':
  main()