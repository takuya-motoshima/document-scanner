import cv2
import numpy as np
import base64
import os.path
import re
from importlib import import_module
# tkinter changed to read dynamically in show function.
# import tkinter as tk

def toDataURL(img, mime = None):
  """Image to Data URL. Supports png, jpg and jpeg.
  Args:
    img: Image path or CV2 ndarray image.
    mime: The media type of the Data URL. Required if the image is an ndarray image.
  Returns:
    Return Data URL and MIME type.
  Raises:
    ValueError: Image types other than png, jpg, jpeg.
  """
  # to base64.
  b64, mime = toBase64(img, mime)

  # Generates and returns a Data URL string based on base64.
  return f'data:image/{mime};base64,{b64}', mime

def toBase64(img, mime = None):
  """Image to base64. Supports png, jpg and jpeg.
  Args:
    img: Image path or CV2 ndarray image.
    mime: The media type of the Data URL. Required if the image is an ndarray image.
  Returns:
    Return base64 and MIME type.
  Raises:
    ValueError: Image types other than png, jpg, jpeg.
  """
  if isinstance(img, np.ndarray):
    # For ndarray images.
    # Return an error if the required parameter MIME type is missing.
    if not mime:
      raise ValueError('Requires media type (png or jpeg)')

    # ndarray image to base64.
    _, encoded = cv2.imencode(f'.{mime}', img)

    # Return base64.
    return base64.b64encode(encoded).decode('ascii'), mime
  elif isinstance(img, str):
    # For image paths.
    # Get MIME type.
    mime = getMime(img)

    # Image bytes object.
    with open(img, 'rb') as f:
      bytes = f.read()
    
    # Bytes object to base64.
    return base64.b64encode(bytes).decode('ascii'), mime
  else:
    # Return an error if the input is not an ndarray image or image path.
    raise ValueError('Image parameters should be file paths or ndarray images')

def detectDataURL(str):
  """Detecting Data URL.
      data URI - MDN https://developer.mozilla.org/en-US/docs/data_URIs
      The "data" URL scheme: http://tools.ietf.org/html/rfc2397
      Valid URL Characters: http://tools.ietf.org/html/rfc2396#section2
  Args:
    str: String
  Returns:
    If the string is a DataURL, it returns the media type and base64. Otherwise returns None.
  """
  found = re.match(r'^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  # found = re.match(r'^\s*data:(\w+\/\w+(?:;[\w\-]+\=[\w\-]+)?)?(?:;base64)?,([\w\d!$&\',()*+,;=\-._~:@\/?%\s]*)\s*$', str)
  if not found:
    return None
  mime = found.group(1)
  b64 = found.group(2)
  return mime, b64

def getExtension(path):
  """Return extension from file path.
  Args:
    path: File Path.
  Returns:
    File extension, e.g. png.
  """
  # Get extension.
  name = os.path.basename(path).split('.')
  if len(name) < 2:
    return None
  return name[1].lower()

def getMime(path):
  """Return MIME type from file path.
  Args:
    path: File Path.
  Returns:
    MIME type, e.g. png.
  """
  # Get extension.
  ext = getExtension(path)

  # Return MIME type.
  if ext == 'jpg' or ext == 'jpeg':
    return 'jpeg'
  elif ext=='png':
    return 'png'
  else:
    return ext

def show(title, img):
# def show(title, img, scaleWd = 500):
  """Show image on display.
  Args:
    title: Display title.
    img: ndarray type image.
  """
  ht, wd = img.shape[:2]
  tk = import_module('tkinter')
  root = tk.Tk()
  screenWd = root.winfo_screenwidth()
  screenHt = root.winfo_screenheight()
  root.destroy()
  multiplier = 1
  if ht > screenHt or wd > screenWd:
    if ht / screenHt >= wd / screenWd:
      multiplier = screenHt / ht
    else:
      multiplier = screenWd / wd
  dst = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)
  # scaleHt = round(ht * (scaleWd / wd))
  # dst = cv2.resize(img, dsize=(scaleWd, scaleHt))
  x = round(screenWd / 2 - (wd * multiplier) / 2)
  y = round(screenHt / 2 - (ht * multiplier) / 2)
  cv2.namedWindow(title) 
  cv2.moveWindow(title, x, y)
  cv2.imshow(title, dst)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
