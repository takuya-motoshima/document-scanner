import os
from dotmap import DotMap
import core
import utils

def scan(img, type, scan_fields = None, debug_img_callback = None):
  """Scan text from a document.
  Args:
      img (str): Image path or DataURL.
      type (str): Document type. (driverslicense: Driver's license card, mynumber: My number card)
      scan_fields (list, optional): Fields to be scanned. Defaults to None(all fields).
      debug_img_callback (function, optional): Callback function for image transformation. Defaults to None.
  Raises:
      ValueError: The img parameter is incorrect.
      ValueError: The type parameter is incorrect.
  """
  try:
    _validate_params(img, type)
    if not debug_img_callback:
      debug_img_callback = lambda label, img: None
    data_url = core.detect_id_card(img, debug_img_callback)
    if not data_url:
      utils.logging.debug('The document could not be detected from the image')
      return DotMap()
    return core.scan_text(data_url, type, scan_fields, debug_img_callback)
  except:
    utils.logging.exception('')
    raise

def _validate_params(img, type):
  if (not utils.is_data_url(img) and not os.path.exists(img) and not os.path.isfile(img)):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')
  if type != 'driverslicense' and type != 'mynumber':
    raise ValueError('Incorrect type. Type can be "driverslicense" or "mynumber"')