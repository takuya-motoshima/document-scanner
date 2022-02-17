import cv2
import numpy as np
import base64
import ocr.utils as utils

def toBase64(img, mime = None):
  """Image to base64. 
  Args:
    img: CV2 Image object or image path.
    mime: The media type of the Data URL. Required if the image is an CV2 Image object.
  Returns:
    Return base64 and MIME type.
  Raises:
    ValueError: Image types other than png, jpg, jpeg.
  """
  if isinstance(img, np.ndarray):
    # For CV2 Image object.
    # Return an error if the required parameter MIME type is missing.
    if not mime:
      raise ValueError('Requires media type (png or jpeg)')

    # CV2 Image object to base64.
    _, encoded = cv2.imencode(f'.{mime}', img)

    # Return base64.
    return base64.b64encode(encoded).decode('ascii'), mime
  elif isinstance(img, str):
    # For image path.
    # Get MIME type.
    mime = utils.getMime(img)

    # Image bytes object.
    with open(img, 'rb') as f:
      bytes = f.read()
    
    # Bytes object to base64.
    return base64.b64encode(bytes).decode('ascii'), mime
  else:
    # Return an error if the input is not an CV2 Image object or image path.
    raise ValueError('Image parameters should be file path or CV2 Image object')
