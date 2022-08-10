import cv2
import numpy as np
import os
from dotmap import DotMap
import utils

def detectDocument(options):
  """Detect document from image.
  Args:
    options.input: Image path or Data URL.
    options.output: Output image path of the found document.
    options.debug: Display debug image on display.
  Returns:
    Return detected document image.
  """
  # Initialize options.
  options = DotMap(dict(
    input = None,
    output = None,
    debug = False
  ) | options.toDict())

  # input option required.
  if not options.input:
    raise ValueError('input option required')

  # Input options only allow image path or data URL.
  if not utils.isDataUrl(options.input) and not os.path.exists(options.input) and os.path.isfile(options.input):
    raise ValueError(f'{options.input} Image file not found')

  # load an image.
  if utils.isDataUrl(options.input):
    img = utils.toNdarray(options.input)
  else:
    img = cv2.imread(options.input)
  if options.debug:
    utils.showImage('Original', img)

  # Resize the image.
  resizeImg, resizeRatio = utils.resizeImage(img, height=600)

  # Detect document contour points.
  contour = _detectDocumentContourPoints(resizeImg, options.debug)
  if contour is None:
    return None

  # Draw a contour.
  if options.debug:
    tmpImg = resizeImg.copy()
    cv2.drawContours(tmpImg, [contour], -1, (0,255,0), 2)
    utils.showImage('Marked', tmpImg)

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = _fourPointTransform(contour/resizeRatio, img)
  warpImg, _ = utils.resizeImage(warpImg, height=800)
  if options.debug:
    utils.showImage('Warped', warpImg)

  # Resize in the specified ratio.
  width, height, _ = warpImg.shape
  widthRatio, heightRatio = [8.56, 5.4]
  resizeWidth = width
  resizeHeight = height
  if (height / width) < (heightRatio / widthRatio):
    resizeHeight = round(width * (heightRatio / widthRatio))
  else:
    resizeWidth = round(height / (heightRatio / widthRatio))
  utils.logging.debug(f'resize={resizeWidth}/{resizeHeight}')
  warpImg = cv2.resize(warpImg, (resizeWidth, resizeHeight), cv2.INTER_AREA)
  utils.showImage('Warped', warpImg)

  # Output the resulting image.
  if options.output:
    cv2.imwrite(options.output, warpImg)
    utils.logging.debug(f'Output {options.output}')

  # Returns the DataURL of the image.
  dataUrl, _ = utils.toDataUrl(warpImg, utils.getMime(options.input))
  return dataUrl
  
def _detectDocumentContourPoints(img, debug=False):
  """Detect document contour points.
  Args:
    img: CV2 Image.
  Returns:
    Return a list (ndarray) of the points (x, y) found on the contour.
  """
  # Grayscale the image.
  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  if debug:
    utils.showImage('Grayscale', grayImg)

  # Blur the image and remove noise.
  medianImg = cv2.medianBlur(grayImg, ksize=5)

  # Remove white noise. Shrink the white part and dilate the black part.
  erosionImg = cv2.erode(medianImg, kernel=np.ones((5,5), np.uint8), iterations=1)

  # Binarize the image (colors to black and white only).
  threshImg = cv2.adaptiveThreshold(erosionImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  if debug:
    utils.showImage('Thresh', threshImg)

  # Detect image edges.
  edgedImg = cv2.Canny(threshImg, 30, 400)
  # edgedImg = cv2.Canny(threshImg, 100, 200, apertureSize=3)
  if debug:
    utils.showImage('Edged', edgedImg)

  # Find the contour.
  contours, _ = cv2.findContours(edgedImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  # If you can't find the contour.
  if not contours:
    return None

  # Find the rectangular contour with the largest area from the found contours.
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  for contour in contours:
    # Approximate the contour.
    peri = cv2.arcLength(contour, True)
    # approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    approx = cv2.approxPolyDP(contour, 0.1 * peri, True)
    # approx = cv2.approxPolyDP(contour, 0.005 * peri, True)

    # if our approximated contour has four points, we can assume it is rectangle.
    if len(approx) == 4:
      return approx

  # If you can't find the rectangle contour.
  return None
  # contour = max(contours, key = cv2.contourArea)
  # return cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)

def _contourToRect(contour):
  """Convert contour points (x, y) to four external rectangle points (x, y).
  Args:
    contour: Contour points (x, y).
  Returns:
    Return a rectangular list of points (4 rows 2 columns).
  """
  # Initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left, the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left.
  pts = contour.reshape(4, 2)
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
  return rect

def _fourPointTransform(contour, img):
  """Return a Keystone correction image (ndarray) of a rectangle on the image.
  Args:
    contour: Contour points (x, y).
    img: Original image of ndarray type.
  Returns:
    Return a Keystone correction image (ndarray).
  """
  # Contour quadrilateral coordinates.
  rect = _contourToRect(contour)

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
  return cv2.warpPerspective(img, M, (maxWidth, maxHeight))