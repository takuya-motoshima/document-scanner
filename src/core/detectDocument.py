from turtle import width
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

  # Input options only allow image path or data URL.]
  if not utils.isDataUrl(options.input) and not os.path.exists(options.input) and os.path.isfile(options.input):
    raise ValueError(f'{options.input} Image file not found')

  # load an image.
  if utils.isDataUrl(options.input):
    origImg = utils.toNdarray(options.input)
  else:
    origImg = cv2.imread(options.input)
  if options.debug:
    utils.showImage('Original', origImg)

  # Resize the image.
  resizeImg, resizeRatio = utils.resizeImage(origImg, height=600)

  # Detect document contour points.
  contour = _detectDocumentContourPoints(resizeImg, options.debug)
  if contour is None:
    return None

  # Draw a contour.
  if options.debug:
    tmpImg = resizeImg.copy()
    cv2.drawContours(tmpImg, [contour], -1, (0,255,0), 2)
    utils.showImage('Drawing contour', tmpImg)

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = utils.fourPointTransform(contour/resizeRatio, origImg)
  warpImg, _ = utils.resizeImage(warpImg, height=800)
  if options.debug:
    utils.showImage('Warped', warpImg)

  # Resize in the specified ratio.
  width, height = warpImg.shape[:2]
  widthRatio, heightRatio = [8.56, 5.4]
  resizeWidth = width
  resizeHeight = height
  if (height / width) < (heightRatio / widthRatio):
    resizeHeight = round(width * (heightRatio / widthRatio))
  else:
    resizeWidth = round(height / (heightRatio / widthRatio))
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
    debug: Display debug image on display.
  Returns:
    Return a list (ndarray) of the points (x, y) found on the contour.
  """
  # Add a margin inside the image so that the target document is not adjacent to the image frame.
  padding = 10
  if padding > 0:
    img = cv2.copyMakeBorder(img.copy(), padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0,0,0))

    # The image rendering area excluding the margins.
    height, width = img.shape[:2]
    clientTopLeft = DotMap(dict(x = padding, y = padding))
    clientTopRight = DotMap(dict(x = width - padding, y = padding))
    clientBottomRight = DotMap(dict(x = width - padding, y = height - padding))
    clientBottomLeft = DotMap(dict(x = padding, y = height - padding))
    if debug:
      utils.showImage('Add margins', cv2.rectangle(img.copy(), (padding, padding), (width - padding, height - padding), (255,255,0), 2))

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
    approx = cv2.approxPolyDP(contour, epsilon=0.1 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.02 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.005 * peri, closed=True)

    # Skip if the contour found is not rectangle.
    if not len(approx) == 4:
      continue

    # Skip if the rectangle is adjacent to a margin created in the image.
    if padding > 0:
      (topLeft, topRight, bottomRight, bottomLeft) = utils.contourToRect(approx)
      if (not(
        topLeft.x >= clientTopLeft.x - 5 and
        topLeft.y >= clientTopLeft.y - 5 and
        topRight.x <= clientTopRight.x - 5 and
        topRight.y >= clientTopRight.y - 5 and
        bottomRight.x <= clientBottomRight.x - 5 and
        bottomRight.y <= clientBottomRight.y - 5 and
        bottomLeft.x >= clientBottomLeft.x - 5 and
        bottomLeft.y <= clientBottomLeft.y - 5
      )):
        continue

    # Subtract the length of the padding from the found contour coordinates.
    approx = np.array(approx) - padding
    return approx

  # If you can't find the rectangle contour.
  return None