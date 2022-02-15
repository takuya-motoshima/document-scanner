import cv2
import numpy as np
import os
import re
import re
from dotmap import DotMap
import ocr.utils as utils
from ocr.logger import logging

def main(opts = dict()):
  """Detect document from image.
  Args:
    opts.input: Image path or Data URL.
    opts.output: Output image path of the found document.
    opts.input: Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).
  Returns:
    Return detected document image.
  """
  logging.debug('begin')

  # Initialize options.
  opts = dict(input = None, output = None, aspect = None) | opts
  opts = DotMap(opts)
  print(f'opts.input={opts.input[:50]}')
  print(f'opts.output={opts.output}')
  print(f'opts.aspect={opts.aspect}')

  # Validate options.
  validOptions(opts)

  # load an image.
  if utils.isDataURL(opts.input):
    img = utils.toNdarray(opts.input)
  else:
    img = cv2.imread(opts.input)

  # Resize the image.
  resizedImg, resizeRatio = utils.resizeImage(img, height=600)
  utils.show('original', resizedImg)

  # Make a copy.
  copyImg = resizedImg.copy()

  # Find the contour of the rectangle with the largest area.
  maxCnt = findRectangleContour(resizedImg)

  # Rectangle contour not found.
  if maxCnt is None:
    logging.debug('Rectangle contour not found')
    return None

  # Draw a contour.
  cv2.drawContours(copyImg, [maxCnt], -1, (0,255,0), 2)
  utils.show('marked', copyImg)

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = fourPointTransform(maxCnt/resizeRatio, img)
  warpImg, _ = utils.resizeImage(warpImg, height=800)
  utils.show('warped', warpImg)

  # Resizes the document image with the specified aspect ratio.
  if opts.aspect:
    width, height, _ = warpImg.shape
    widthRatio, heightRatio = list(map(float, opts.aspect.split(':')))
    resizeWidth = width
    resizeHeight = height
    # Resize so that the width and height after resizing are not smaller than before resizing.
    if (height / width) < (heightRatio / widthRatio):
      resizeHeight = round(width * (heightRatio / widthRatio))
    else:
      resizeWidth = round(height / (heightRatio / widthRatio))
    logging.debug(f'resize={resizeWidth}/{resizeHeight}')
    warpImg = cv2.resize(warpImg, (resizeWidth, resizeHeight), cv2.INTER_AREA)
    utils.show(f'resize to {widthRatio}:{heightRatio} ratio', warpImg)

  # Write the image to a file if you have the output option.
  if opts.output:
    cv2.imwrite(opts.output, warpImg)
    logging.debug(f'Output {opts.output}')

  # Print the image Data URL if you have a print option.
  dataURL, _ = utils.toDataURL(warpImg, utils.getMime(opts.input))
  return dataURL
  # b64, _ = utils.toBase64(warpImg, utils.getMime(opts.input))
  # return b64

def validOptions(opts): 
  """Validate options.
  Args:
    opts.input: Image path or Data URL.
    opts.output: Output image path of the found document.
    opts.input: Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).
  Raises:
    ValueError: If there are invalid options
  """
  # input option required.
  if not opts.input:
    raise ValueError('input option required')

  # Input options only allow image path or data URLs.
  if not utils.isDataURL(opts.input) and not os.path.exists(opts.input) and os.path.isfile(opts.input):
    raise ValueError(f'{opts.input} Image file not found')

  # The aspect ratio option allows the "width: height" format.
  if opts.aspect:
    matches = re.match(r'^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$', opts.aspect)
    if not matches:
      raise ValueError('Aspect ratio option is invalid')
    widthRatio = matches.group(1)
    htRatio = matches.group(2)
    if float(widthRatio) == 0 or float(htRatio) == 0:
      raise ValueError('ZERO cannot be used for aspect ratio width and height')

def findRectangleContour(img):
  """Find the contour of the rectangle with the largest area.
  Args:
    img: CV2 Image object.
  Returns:
    Return a list (ndarray) of the points (x, y) found on the contour.
  """
  # Grayscale.
  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  utils.show('grayscale', grayImg)

  # Remove image noise.
  grayImg = cv2.medianBlur(grayImg, 5)
  grayImg = cv2.erode(grayImg, kernel=np.ones((5,5),np.uint8), iterations=1)
  grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  utils.show('noise reduction', grayImg)
  edgedImg = cv2.Canny(grayImg, 30, 400)
  # edgedImg = cv2.Canny(grayImg, 100, 200, apertureSize=3)
  utils.show('edged', edgedImg)

  # Find the contour.
  cnts, _ = cv2.findContours(edgedImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  logging.debug(f'length of countours {len(cnts)}')

  # If you can't find the contour.
  if not cnts:
    return None

  # Find the rectangular contour with the largest area from the found contours.
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
  for cnt in cnts:
    # Approximate the contour.
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
    # approx = cv2.approxPolyDP(cnt, 0.1 * peri, True)
    # approx = cv2.approxPolyDP(cnt, 0.005 * peri, True)

    # if our approximated contour has four points, we can assume it is rectangle.
    if len(approx) == 4:
      return approx

  # If you can't find the rectangle contour.
  return None
  # cnt = max(cnts, key = cv2.contourArea)
  # return cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

def convertContourToRect(cnt):
  """Convert contour points (x, y) to four external rectangle points (x, y).
  Args:
    cnt: Contour points (x, y).
  Returns:
    Return a rectangular list of points (4 rows 2 columns).
  """
  # Initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left, the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left.
  pts = cnt.reshape(4, 2)
  rect = np.zeros((4, 2), dtype = 'float32')

  # The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum.
  sum = pts.sum(axis = 1)
  rect[0] = pts[np.argmin(sum)] # top-left
  rect[2] = pts[np.argmax(sum)] # bottom-right

  # Now, compute the difference between the points, the top-right point will have the smallest difference, whereas the bottom-left will have the largest difference.
  diff = np.diff(pts, axis=1)
  rect[1] = pts[np.argmin(diff)] # top-right
  rect[3] = pts[np.argmax(diff)] # bottom-left

  # Return the rectangle coordinates of the contour.
  # logging.debug(f'rect={rect}')
  return rect

def fourPointTransform(cnt, origImg):
  """Return a Keystone correction image (ndarray) of a rectangle on the image.
  Args:
    cnt: Contour points (x, y).
    origImg: Original image of ndarray type.
  Returns:
    Return a Keystone correction image (ndarray).
  """
  # Contour quadrilateral coordinates.
  rect = convertContourToRect(cnt)

  # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left x-coordiates or the top-right and top-left x-coordinates
  (tl, tr, br, bl) = rect
  aWidth = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  bWidth = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWidth = max(int(aWidth), int(bWidth))

  # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates
  aHeight = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  bHeight = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHeight = max(int(aHeight), int(bHeight))

  # Now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order.
  dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype = 'float32')

  # Compute the perspective transform matrix and then apply it.
  M = cv2.getPerspectiveTransform(rect, dst)
  return cv2.warpPerspective(origImg, M, (maxWidth, maxHeight))