def main():
  # Get command options.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-t', '--type', choices=['driverslicense', 'mynumber'], required=True, help='OCR document type')
  parser.add_argument('-d', '--debug', action='store_true', help='Display debug image on display', default=False)
  # parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  # parser.add_argument('-p', '--print', action='store_true', help='Print the Data URL of the detected document', default=False)
  options = DotMap(vars(parser.parse_args()))
  # utils.logging.debug(f'options.input={options.input}')
  # utils.logging.debug(f'options.type={options.type}')
  # utils.logging.debug(f'options.debug={options.debug}')

  # When debug mode is on, the converted images are received sequentially and displayed on the screen.
  transformCallback = None
  if options.debug:
    transformCallback = lambda label, img: utils.displayImage(label, img)

  # Scan text from a document.
  matches = scan(options.input, options.type, transformCallback)

  # The detected text is returned as JSON.
  matchesJson = json.dumps({key: match.text for key, match in matches.items()}, ensure_ascii=False, indent = 4)
  utils.logging.debug(matchesJson)
  print(matchesJson)

if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from scan import scan
  import utils
  main()