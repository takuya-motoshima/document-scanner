import cv2
import base64
import os.path
import re
from importlib import import_module
# tkinter changed to read dynamically in show function.
# import tkinter as tk

def imgToDataURL(path):
  """Image to data URI. This method supports images with png, jpg and jpeg extensions.
  Args:
    path: Image path.
  Returns:
    Returns the data URL.
  Raises:
    ValueError: Image types other than png, jpg, jpeg.
  """
  # Find the image extension.
  name = os.path.basename(path).split('.')
  ext = name[1].lower() if len(name) > 1 else None
  print(f'ext={ext}')

  # base64 media type.
  mediaType = None
  if ext == 'jpg' or ext == 'jpeg':
    mediaType = 'jpeg'
  elif ext=='png':
    mediaType = 'png'
  else:
    # Returns an error for images other than png and jpg.
    raise ValueError('Invalid image type')

  # Image bytes object.
  with open(path, 'rb') as f:
    bytes = f.read()
  
  # Bytes object to base64.
  b64 = base64.b64encode(bytes).decode('utf-8')

  # Convert base64 to DataURL and return.
  return 'data:image/' + mediaType + ';base64,' + b64

def detectDataURL(str):
  """Detecting data URLs.
      data URI - MDN https://developer.mozilla.org/en-US/docs/data_URIs
      The "data" URL scheme: http://tools.ietf.org/html/rfc2397
      Valid URL Characters: http://tools.ietf.org/html/rfc2396#section2
  Args:
    str: String
  Returns:
    If the string is a DataURL, it returns the media type and base64. Otherwise returns None.
  """
  m = re.match(r'^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  # m = re.match(r'^\s*data:(\w+\/\w+(?:;[\w\-]+\=[\w\-]+)?)?(?:;base64)?,([\w\d!$&\',()*+,;=\-._~:@\/?%\s]*)\s*$', str)
  if not m:
    return None
  mediaType = m.group(1)
  b64 = m.group(2)
  return mediaType, b64

def show(title, img):
# def show(title, img, scaleWidth = 500):
  """Show image on display.
  Args:
    title: Display title
    img: ndarray type image.
  """
  height, width = img.shape[:2]
  tk = import_module('tkinter')
  root = tk.Tk()
  screenWidth = root.winfo_screenwidth()
  screenHeight = root.winfo_screenheight()
  # print(f'screen={screenWidth}/{screenHeight}')
  root.destroy()
  multiplier = 1
  if height > screenHeight or width > screenWidth:
    if height / screenHeight >= width / screenWidth:
      multiplier = screenHeight / height
    else:
      multiplier = screenWidth / width
  dst = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)
  # scaleHeight = round(height * (scaleWidth / width))
  # dst = cv2.resize(img, dsize=(scaleWidth, scaleHeight))
  x = round(screenWidth / 2 - (width * multiplier) / 2)
  y = round(screenHeight / 2 - (height * multiplier) / 2)
  cv2.namedWindow(title) 
  cv2.moveWindow(title, x, y)
  cv2.imshow(title, dst)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
