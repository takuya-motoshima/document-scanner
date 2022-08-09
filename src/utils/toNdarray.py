import cv2
import numpy as np
import base64
from urllib import request
from .isDataUrl import isDataUrl

def toNdarray(str): 
  """Image to Data URL.
  Args:
    img: Image Data URL or image base64.
  Returns:
    Return CV2 Image object.
  """
  if isDataUrl(str):
    # For Data URL.
    with request.urlopen(str) as res:
      data = res.read()
    return cv2.imdecode(np.array(bytearray(data), dtype=np.uint8), cv2.IMREAD_UNCHANGED)
  else:
    # For base64.
    return cv2.imdecode(np.fromstring(base64.b64decode(str), np.uint8),  cv2.IMREAD_UNCHANGED)