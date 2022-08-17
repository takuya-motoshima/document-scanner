import os
import sys
import core
import utils

def scan(input, type, transformCallback = None):
  """Scan text from a document.
  Args:
      input (str): Image path or DataURL.
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      transformCallback (function, optional): Callback function for image transformation. Defaults to None.
  Raises:
      ValueError: The input parameter is incorrect.
      ValueError: The type parameter is incorrect.
  """
  try: 
    # Validate parameters
    if (not utils.isDataUrl(input) and
        not os.path.exists(input) and
        not os.path.isfile(input)
      ):
      raise ValueError('Input is incorrect. Input can be an image path, or DataURL')
    if type != 'driverslicense' and type != 'mynumber':
      raise ValueError('Incorrect type. Type can be "driverslicense" or "mynumber"')

    # Initialize transformation callbacks.
    if not transformCallback:
      transformCallback = lambda label, img: None

    # Detect document from image.
    dataUrl = core.detectDocument(input, transformCallback)
    if not dataUrl:
      utils.logging.debug('The document could not be detected from the image')
      sys.exit()

    # Scanning text.
    return core.scanText(dataUrl, type, transformCallback)
  except:
    utils.logging.exception('')
    raise