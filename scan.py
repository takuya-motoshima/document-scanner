import cv2
import numpy as np
import utils
import argparse
import os
import re
import logging

def main():
  # Logging Into A File.
  logging.basicConfig(filename='scan.log', level=logging.DEBUG, format="%(asctime)s -> %(levelname)s: %(message)s")
  logging.debug('begin')

  # Parse arguments.
  opts = parseArguments()
  logging.debug(f'opts={opts}')

  # load an image.
  img = cv2.imread(opts.input)

  # Resize the image.
  resizedImg, resizeRatio = resizeImg(img, ht=600)
  # logging.debug(f'resizeRatio={resizeRatio}')
  utils.show('Original image', resizedImg)

  # Make a copy.
  copyResizedImg = resizedImg.copy()

  # Find the contour of the rectangle with the largest area.
  maxCnt = findRectangleContour(resizedImg)

  # Rectangle contour not found.
  if maxCnt is None:
    logging.debug('Rectangle contour not found')
    return None

  # Draw a contour.
  cv2.drawContours(copyResizedImg, [maxCnt], -1, (0,255,0), 3)
  utils.show('Marked', copyResizedImg)

  # Apply the four point tranform to obtain a "birds eye view" of the image.
  warpImg = fourPointTransform(maxCnt/resizeRatio, img)
  warpImg, _ = resizeImg(warpImg, ht=800)
  utils.show('Warped', warpImg)

  # Resizes the document image with the specified aspect ratio.
  if opts.aspectRatio:
    wd, ht, _ = warpImg.shape
    wdRatio, htRatio = list(map(float, opts.aspectRatio.split(':')))
    resizeWd = wd
    resizeHt = ht
    # Resize so that the width and height after resizing are not smaller than before resizing.
    if (ht / wd) < (htRatio / wdRatio):
      resizeHt = round(wd * (htRatio / wdRatio))
    else:
      resizeWd = round(ht / (htRatio / wdRatio))
    logging.debug(f'resize={resizeWd}/{resizeHt}')
    warpImg = cv2.resize(warpImg, (resizeWd, resizeHt), cv2.INTER_AREA)
    utils.show(f'Resize to {wdRatio}:{htRatio} ratio', warpImg)

  # Write the image to a file if you have the output option.
  if opts.output:
    cv2.imwrite(opts.output, warpImg)
    logging.debug(f'Output {opts.output}')

def parseArguments():
  """Parses and returns command arguments.
  Returns:
    Returns the parsed result in the format (image = <string>, aspectRatio = <string>).
  """
  # Parse.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-o', '--output', type=str, help='Output image path of the found document')
  parser.add_argument('-r', '--aspect', dest='aspectRatio', type=str, help='Resize the scanned document to the specified aspect ratio. Typing as a width:height ratio (like 4:5 or 1.618:1).')
  parser.add_argument('-p', '--print-data-url', type=str, help='Print the data URL of the document')
  opts = parser.parse_args()

  # Image option validation.
  res = utils.detectDataURL(opts.input)
  if res:
    # For data URL.
    mediaType = res[0]
    if mediaType != 'image/png' and mediaType != 'image/jpeg':
      raise ValueError('Unsupported media type, Images can process PNG or JPG')
  else:
    # If it is not a data URL, treat it as an image path.
    if not os.path.exists(opts.input):
      raise ValueError('File path not found')
    elif not os.path.isfile(opts.input):
      raise ValueError('It\'s not a file path')

  # Aspect ratio option validation.
  if opts.aspectRatio is not None:
    found = re.match(r'^((?!0\d)\d*(?:\.\d+)?):((?!0\d)\d*(?:\.\d+)?)$', opts.aspectRatio)
    if not found:
      raise ValueError('Invalid format, typing as a width:height ratio (like 4:5 or 1.618:1)')
    wdRatio = found.group(1)
    htRatio = found.group(2)
    if float(wdRatio) == 0 or float(htRatio) == 0:
      raise ValueError('Zero cannot be used for height or width ratio')
  return opts

def findRectangleContour(img):
  """Find the contour of the rectangle with the largest area.
  Args:
    img: ndarray type image.
  Returns:
    Returns a list (ndarray) of the points (x, y) found on the contour.
  """
  # Grayscale.
  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  utils.show('Grayscale', grayImg)

  # Remove image noise.
  grayImg = cv2.medianBlur(grayImg, 5)
  grayImg = cv2.erode(grayImg, kernel=np.ones((5,5),np.uint8), iterations=1)
  grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  utils.show('grayImg', grayImg)
  edgedImg = cv2.Canny(grayImg, 30, 400)
  # edgedImg = cv2.Canny(grayImg, 100, 200, apertureSize=3)
  utils.show('Edged', edgedImg)

  # # Blur the image to remove noise.
  # blurImg = cv2.GaussianBlur(grayImg, (5, 5), 0)
  # utils.show('Blurred', blurImg)

  # # Convert to a white and black image (binarized image).
  # _, threshImg = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY)
  # utils.show('Binarized', threshImg)

  # Find the contour.
  cnts, _ = cv2.findContours(edgedImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  logging.debug(f'length of countours {len(cnts)}')

  # If you can't find the contour.
  if not cnts:
    return None

  # Find the rectangular contour with the largest area from the found contours.
  cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
  for cnt in cnts:
    approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
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
    Returns a rectangular list of points (4 rows 2 columns).
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

  # Returns the rectangle coordinates of the contour.
  # logging.debug(f'rect={rect}')
  return rect

def fourPointTransform(cnt, origImg):
  """Returns a Keystone correction image (ndarray) of a rectangle on the image.
  Args:
    cnt: Contour points (x, y).
    origImg: Original image of ndarray type.
  Returns:
    Returns a Keystone correction image (ndarray).
  """
  # Contour quadrilateral coordinates.
  rect = convertContourToRect(cnt)

  # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left x-coordiates or the top-right and top-left x-coordinates
  (tl, tr, br, bl) = rect
  wdA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
  wdB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
  maxWd = max(int(wdA), int(wdB))

  # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates
  htA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
  htB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
  maxHt = max(int(htA), int(htB))

  # Now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order.
  dst = np.array([[0, 0], [maxWd - 1, 0], [maxWd - 1, maxHt - 1], [0, maxHt - 1]], dtype = 'float32')

  # Compute the perspective transform matrix and then apply it.
  M = cv2.getPerspectiveTransform(rect, dst)
  return cv2.warpPerspective(origImg, M, (maxWd, maxHt))

def resizeImg(img, wd=None, ht=None, interpolation = cv2.INTER_AREA):
  """Resize the image.
  Args:
    img: ndarray type image.
    wd: Width after resizing.
    ht: Height after resizing.
    interpolation: Interpolation flag that takes one of the following methods.
                    cv2.INTER_NEAREST: nearest neighbor interpolation.
                    cv2.INTER_LINEAR: bilinear interpolation.
                    cv2.INTER_CUBIC: bicubic interpolation.
                    cv2.INTER_AREA: resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire'-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.
                    cv2.INTER_LANCZOS4: Lanczos interpolation over 8x8 neighborhood.
  Returns:
    Returns a resized ndarray image.
  """
  resizeRatio = 1
  origWd, origHt, _ = img.shape
  # logging.debug(f'origWd={origWd}, origHt={origHt}')
  if wd is None and ht is None:
    return img, resizeRatio
  elif wd is None:
    resizeRatio = ht / origHt
    wd = int(origWd * resizeRatio)
    # logging.debug(f'wd={wd}, ht={ht}')
    resizedImg = cv2.resize(img, (ht, wd), interpolation)
    return resizedImg, resizeRatio
  else:
    resizeRatio = wd / origWd
    ht = int(origHt * resizeRatio)
    # logging.debug(f'wd={wd}, ht={ht}')
    resizedImg = cv2.resize(img, (ht, wd), interpolation)
    return resizedImg, resizeRatio

if __name__ == "__main__":
  main()