import argparse
import ocr

def main():
  # Parse arguments.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  parser.add_argument('-r', '--aspect', type=str, help='Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).')
  # parser.add_argument('-r', '--aspect', dest='aspect', type=str, help='Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).')
  parser.add_argument('-p', '--print-base64', dest='printBase64', action='store_true', help='Print the base64 of the document')
  opts = vars(parser.parse_args())

  # Detect document from image.
  dataURL = ocr.detectDocument(opts)
  print(f'dataURL={dataURL[:50]}')

  # OCR.
  matches = ocr.scanDriverlicense(dict(input = dataURL))
  print(f'matches={matches}')

if __name__ == '__main__':
  main()