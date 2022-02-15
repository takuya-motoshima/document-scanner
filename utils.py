import cv2
import numpy as np
import base64
import os.path
import re
from importlib import import_module
import json
# tkinter changed to read dynamically in show function.
# import tkinter as tk
import colorsys
import random

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
  matches = re.match(r'^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  # matches = re.match(r'^\s*data:(\w+\/\w+(?:;[\w\-]+\=[\w\-]+)?)?(?:;base64)?,([\w\d!$&\',()*+,;=\-._~:@\/?%\s]*)\s*$', str)
  if not matches:
    return None
  mime = matches.group(1)
  b64 = matches.group(2)
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

def writeJson(path, data):
  """Write the data to a file as JSON.
  Args:
    path: File Path.
    data: Data written to the file as JSON.
  """
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))

def drawRect(img, pt1, pt2, color, label, drawTextBackground = True):
  """Draw rectangle with text.
  Args:
    img: ndarray type image.
    pt1: The upper left point of the rectangle.
    pt2: The bottom right dot of the rectangle.
    color: Rectangle background color.
    label: text.
    drawTextBackground: Whether to draw a text background.
  """
  # Rectangle.
  cv2.rectangle(img, pt1, pt2, color, thickness=1)

  # Text boundaries.
  font = cv2.FONT_HERSHEY_SIMPLEX
  scale = .5
  thk = 1
  (wd, ht), _ = cv2.getTextSize(label, font, scale, thk)
  x, y = pt1

  # Text background.
  margin = 10
  labelColor = color
  if drawTextBackground:
    cv2.rectangle(img, (x, y - ht - margin), (x + wd + margin, y), color, thickness=-1)
    labelColor = (0, 0, 0)

  # Draw text.
  cv2.putText(img, label, (x + int(margin / 2), y - int(margin / 2)), font, scale, labelColor, thk)

def randColor(bright=1):
  """Generate random colors.
  Args:
    bright: brightness.
  Returns:
    Returns BGR format colors.
  """
  hue = random.random()
  sat = random.random()
  val = bright
  return tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(hue, sat, val))

def calcIoU(rectA, rectB):
  """Calculate IoU for two rectangles.
  Args:
    rectA: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
    rectB: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
    Returns IoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  aXmin, aYmin, aXmax, aYmax = rectA

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  bXmin, bYmin, bXmax, bYmax = rectB

  # Calculate the area of rectangle A.
  aArea = (aXmax - aXmin) * (aYmax - aYmin)
  # aArea = (aXmax - aXmin + 1) * (aYmax - aYmin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of rectangle B.
  bArea = (bXmax - bXmin) * (bYmax - bYmin)
  # bArea = (bXmax - bXmin + 1) * (bYmax - bYmin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of intersection.
  interXmin = max(aXmin, bXmin)
  interYmin = max(aYmin, bYmin)
  interXmax = min(aXmax, bXmax)
  interYmax = min(aYmax, bYmax)
  interWd = max(0, interXmax - interXmin)
  # interWd = max(0, interXmax - interXmin + 1)# The reason for adding 1 is to avoid division by zero.
  interHt = max(0, interYmax - interYmin)
  # interHt = max(0, interYmax - interYmin + 1)# The reason for adding 1 is to avoid division by zero.
  interArea = interWd * interHt

  # Calculate the area of union.
  unionArea = aArea + bArea - interArea

  # Calculate IoU.
  iou = interArea / unionArea
  return round(iou, 3), interArea, aArea, bArea

def calcGIoU(rectA, rectB):
  """Calculate GIoU for two rectangles.
  Args:
    rectA: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
    rectB: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
    Returns GIoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  aXmin, aYmin, aXmax, aYmax = rectA

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  bXmin, bYmin, bXmax, bYmax = rectB

  # Calculate IoU.
  iou, interArea, aArea, bArea = calcIoU(rectA, rectB)

  # Calculate the area of convex shape C.
  interXmin = min(aXmin, bXmin)
  interYmin = min(aYmin, bYmin)
  interXmax = max(aXmax, bXmax)
  interYmax = max(aYmax, bYmax)
  cArea = (interXmax - interXmin) * (interYmax - interYmin)

  # Area obtained by subtracting the overlapping partial area (Intersect) from the total area of rectangles a and b.
  unionArea = interArea / iou

  # Calculate GIoU.
  giou = iou - (cArea - unionArea) / cArea
  return round(giou, 3), interArea, aArea, bArea

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

  # Destroy the window.
  cv2.destroyAllWindows()
