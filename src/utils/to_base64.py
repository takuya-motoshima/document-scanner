import cv2
import numpy as np
import base64
from .get_mime_type import get_mime_type

def to_base64(img, mime = None):
  """Image to base64. 
  Args:
      img (numpy.ndarray|str): CV2 Image or image path.
      mime (str, optional): The media type of the Data URL. Required if the image is an CV2 Image. Defaults to None.
  Returns:
      str: Return base64 and MIME type.
  Raises:
      ValueError: MIME parameters are missing.
      ValueError: Image parameters are incorrect.
  """
  if isinstance(img, np.ndarray):
    # For CV2 Image.
    if not mime:
      raise ValueError('Requires media type (png or jpeg)')
    _, encoded = cv2.imencode(f'.{mime}', img)
    return base64.b64encode(encoded).decode('ascii'), mime
  elif isinstance(img, str):
    # For image path.
    mime = get_mime_type(img)
    with open(img, 'rb') as f:
      bytes = f.read()
    return base64.b64encode(bytes).decode('ascii'), mime
  else:
    raise ValueError('Image parameters should be file path or CV2 Image')
