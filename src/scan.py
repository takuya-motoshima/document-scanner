import os
from dotmap import DotMap
import core
import utils

def scan(input, type, fields = None, transformCallback = None):
  """Scan text from a document.
  Args:
      input (str): Image path or DataURL.
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      fields (list, optional): Fields to be scanned. Defaults to None(all fields).
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
      return DotMap()

    # Scanning text.
    return core.scanText(dataUrl, type, fields, transformCallback)
  except:
    utils.logging.exception('')
    raise