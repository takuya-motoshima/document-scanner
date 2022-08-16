def main():
  try: 
    # Get command options.
    options = _getOptions()

    # Detect document from image.
    dataUrl = core.detectDocument(options.input, _transformCallback(options.debug))
    if not dataUrl:
      utils.logging.debug('The document could not be detected from the image')
      exit()

    # Scanning text.
    matches = core.scanText(dataUrl, options.type, _transformCallback(options.debug))
    if not matches:
      utils.logging.debug('The text could not be detected')
      exit()
    for key, match in matches.items():
      utils.logging.debug(f'{key} -> {match.text}')
  except:
    utils.logging.exception('')
    raise

def _transformCallback(debug):
  """Display image.
  Args:
      debug (bool): Debug Flag.
  Returns:
      function: Image transformation callback function.
  """
  if not debug:
    return None
  return lambda label, img: utils.showImage(label, img)

def _getOptions():
  """Get command options.
  Returns:
      dotmap.DotMap: Command line options.
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
  main()