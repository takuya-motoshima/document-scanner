import cv2
import numpy as np
import os
from dotmap import DotMap
import utils

def detectDocument(input, output = None, debug = False):
  """Detect document from image.
  Args:
    input: Image path or DataURL.
    output: Output image path of the found document.
    debug: Display debug image on display.
  Returns:
    Return detected document image.
  """
  # Validate parameters
  if (utils.isDataUrl(input) and
      not os.path.exists(input) and
      not os.path.isfile(input)
  ):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')

  # Load the image.
  if utils.isDataUrl(input):
    img = utils.toNdarray(input)
  else:
    img = cv2.imread(input)
  if debug:
    utils.showImage('Original', img)

  # Resize the image.
  resizeImg, resizeRatio = utils.resizeImage(img, height=600)

  # Detect document contour points.
  contour = _detectDocumentContourPoints(resizeImg, debug)
  if contour is None:
    return None

  # Draw a contour.
  if debug:
    tmpImg = resizeImg.copy()
    cv2.drawContours(tmpImg, [contour], -1, (0,255,0), 2)
    utils.showImage('Drawing contour', tmpImg)

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = utils.fourPointTransform(contour/resizeRatio, img)
  warpImg, _ = utils.resizeImage(warpImg, height=800)
  if debug:
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
  if output:
    cv2.imwrite(output, warpImg)
    utils.logging.debug(f'Output {output}')

  # Returns the DataURL of the image.
  dataUrl, _ = utils.toDataUrl(warpImg, utils.getMime(input))
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
      utils.showImage('Add margins',
        cv2.rectangle(img.copy(),
        (padding, padding),
        (width - padding, height - padding),
        (0,255,0),
        2))

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