def main():
  # Get command arguments.
  options = _getCommandOptions()

  # Detect document from image.
  dataUrl = core.detectDocument(options)
  utils.logging.debug(f'dataUrl={dataUrl[:50]}')
  if not dataUrl:
    utils.logging.debug('The document could not be detected from the image')
    exit()

  # OCR.
  matches = core.scanText(dict(input = dataUrl, type = options['type'], debug = options['debug']))
  if not matches:
    utils.logging.debug('The text could not be detected')
    exit()
  for key, match in matches.items():
    utils.logging.debug(f'{key} -> {match.text}')

def _getCommandOptions():
  """Get command options.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  parser.add_argument('-p', '--print', action='store_true', help='Print the Data URL of the detected document', default=False)
  parser.add_argument('-t', '--type', choices=['driverslicense', 'mynumber'], required=True, help='OCR document type')
  parser.add_argument('-d', '--debug', action='store_true', help='Display debug image on display', default=False)
  return DotMap(vars(parser.parse_args()))

if __name__ == '__main__':
  import argparse
  from dotmap import DotMap
  import core
  import utils

  # OCR for ID cards.
  main()