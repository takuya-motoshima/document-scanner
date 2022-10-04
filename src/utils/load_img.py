import os
import cv2
from .is_data_url import is_data_url
from .to_ndarray import to_ndarray

def load_img(img):
  """Load image from path or DataURL as ndarray.
  Args:
      img (str): The path or DataURL of the image.
  Returns:
      numpy.ndarray: CV2 Image.
  Raises:
      ValueError: Parameter is not DataURL or file.
  """
  if is_data_url(img):
    return to_ndarray(img)
  elif os.path.isfile(img):
    return cv2.imread(img)
  else:
    raise ValueError('The parameter should be the DataURL or file of the image')