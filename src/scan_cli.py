def main():
  # Get command options.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-t', '--type', choices=['driverslicense', 'mynumber'], required=True, help='OCR document type')
  parser.add_argument('-d', '--debug', action='store_true', help='Display debug image on display', default=False)
  # parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  # parser.add_argument('-p', '--print', action='store_true', help='Print the Data URL of the detected document', default=False)
  options = DotMap(vars(parser.parse_args()))

  # When debug mode is on, the converted images are received sequentially and displayed on the screen.
  transformCallback = None
  if options.debug:
    transformCallback = lambda label, img: utils.displayImage(label, img)

  # Scan text from a document.
  matches = scan(options.input, options.type, transformCallback)

  # Convert detection results to text-only data.
  textOnly = dict()
  for i, item in matches.items():
    if not i == 'normalizedAddress':
      textOnly[i] = item.text
    else:
      textOnly[i] = dict()
      for j, item in item.items():
        textOnly[i][j] = item.text

  # The detected text is returned as JSON.
  matchesJson = json.dumps(textOnly, ensure_ascii=False, indent = 4)
  # matchesJson = json.dumps({key: (item.text if item.text else item) for key, item in matches.items()}, ensure_ascii=False, indent = 4)
  # matchesJson = json.dumps({key: item.text for key, item in matches.items()}, ensure_ascii=False, indent = 4)
  utils.logging.debug(matchesJson)
  print(matchesJson)

if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from scan import scan
  import utils
  main()