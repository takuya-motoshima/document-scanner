import os
import cv2
import numpy as np
from dotmap import DotMap
import utils

def detectDocument(input, transformCallback = None):
  """Detect document from image.
  Args:
      input (str): Image path or DataURL.
      transformCallback (function, optional): Callback function for image transformation. Defaults to None.
  Raises:
      ValueError: Parameters are incorrect.
  Returns:
      string: DataURL of the detected document image.
  """
  # Validate parameters
  if (not utils.isDataUrl(input) and
      not os.path.exists(input) and
      not os.path.isfile(input)
    ):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')

  # Initialize transformation callbacks.
  if not transformCallback:
    transformCallback = lambda label, img: None

  # Load the image.
  if utils.isDataUrl(input):
    img = utils.toNdarray(input)
  else:
    img = cv2.imread(input)
  transformCallback('Original', img)

  # Resize the image.
  heightThreshold = 600
  if img.shape[0] < heightThreshold:
    resizeImg, resizeRatio = utils.resizeImage(img, height=heightThreshold)
  else:
    resizeImg = img.copy()
    resizeRatio = 1.
  # resizeImg, resizeRatio = utils.resizeImage(img, height=600)

  # Add a margin inside the image so that the target document is not adjacent to the image frame.
  # padding = 0
  padding = 5
  borderedImg = cv2.copyMakeBorder(resizeImg.copy(), padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=(0,0,0))

  # The image rendering area excluding the margins.
  height, width = borderedImg.shape[:2]
  clientRect = [
    DotMap(x = padding, y = padding),
    DotMap(x = width - padding, y = padding),
    DotMap(x = width - padding, y = height - padding),
    DotMap(x = padding, y = height - padding)
  ]
  transformCallback('Bordered', cv2.rectangle(borderedImg.copy(), (clientRect[0].x, clientRect[0].y), (clientRect[2].x, clientRect[2].y), (0,255,0), 2))
    
  # Grayscale the image.
  grayImg = cv2.cvtColor(borderedImg, cv2.COLOR_BGR2GRAY)
  transformCallback('Grayscale', grayImg)

  # Blur the image and remove noise.
  medianImg = cv2.medianBlur(grayImg, ksize=5)

  # Remove white noise. Shrink the white part and dilate the black part.
  erosionImg = cv2.erode(medianImg, kernel=np.ones((5,5), np.uint8), iterations=1)

  # Binarize the image (colors to black and white only).
  threshImg = cv2.adaptiveThreshold(erosionImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  transformCallback('Thresh', threshImg)

  # Detect image edges.
  edgedImg = cv2.Canny(threshImg, 30, 400)
  # edgedImg = cv2.Canny(threshImg, 100, 200, apertureSize=3)
  transformCallback('Edged', edgedImg)

  # Find the contour.
  contours, _ = cv2.findContours(edgedImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  # If you can't find the contour.
  if not contours:
    return None
  
  # Find the rectangular contour with the largest area from the found contours.
  documentContour = None
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  for contour in contours:
    # Approximate the contour.
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon=0.02 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.1 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.005 * peri, closed=True)

    # Skip if the contour found is not rectangle.
    if not len(approx) == 4:
      continue

    # Skip if the rectangle is adjacent to a margin created in the image.
    if padding > 0:
      contourRect = utils.contourToRect(approx)
      correction = 5;
      if (not(
        contourRect[0].x >= clientRect[0].x - correction and
        contourRect[0].y >= clientRect[0].y - correction and
        contourRect[1].x <= clientRect[1].x - correction and
        contourRect[1].y >= clientRect[1].y - correction and
        contourRect[2].x <= clientRect[2].x - correction and
        contourRect[2].y <= clientRect[2].y - correction and
        contourRect[3].x >= clientRect[3].x - correction and
        contourRect[3].y <= clientRect[3].y - correction
      )):
        continue

      # Subtract the length of the padding from the found contour coordinates.
      approx = np.array(approx) - padding
    documentContour = approx
    break

  # If you can't find the rectangle contour.
  if documentContour is None:
    return None

  # Debugging by drawing contours.
  transformCallback('Drawing contour', cv2.drawContours(resizeImg.copy(), [documentContour], -1, (0,255,0), 2))

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = utils.fourPointTransform(documentContour/resizeRatio, img)
  warpImg, _ = utils.resizeImage(warpImg, height=800)
  transformCallback('Warped', warpImg)

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

  # Returns the DataURL of the image.
  dataUrl, _ = utils.toDataUrl(warpImg, utils.getMime(input))
  return dataUrl