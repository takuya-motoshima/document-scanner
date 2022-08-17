import cv2
import numpy as np
from .contourToRect import contourToRect

def fourPointTransform(contour, img):
  """Return a Keystone correction image (ndarray) of a rectangle on the image.
  Args:
      contour (numpy.ndarray): Contour points (x, y).
      img (numpy.ndarray): CV2 Image.
  Returns:
      numpy.ndarray: Return a Keystone correction image.
  """
  # Contour quadrilateral coordinates.
  rect = contourToRect(contour)

  # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left x-coordiates or the top-right and top-left x-coordinates
  (topLeft, topRight, bottomRight, bottomLeft) = rect
  aWidth = np.sqrt(((bottomRight.x - bottomLeft.x) ** 2) + ((bottomRight.y - bottomLeft.y) ** 2))
  bWidth = np.sqrt(((topRight.x - topLeft.x) ** 2) + ((topRight.y - topLeft.y) ** 2))
  maxWidth = max(int(aWidth), int(bWidth))

  # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates
  aHeight = np.sqrt(((topRight.x - bottomRight.x) ** 2) + ((topRight.y - bottomRight.y) ** 2))
  bHeight = np.sqrt(((topLeft.x - bottomLeft.x) ** 2) + ((topLeft.y - bottomLeft.y) ** 2))
  maxHeight = max(int(aHeight), int(bHeight))

  # Now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order.
  dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]
  ], dtype = 'float32')

  # Compute the perspective transform matrix and then apply it.
  M = cv2.getPerspectiveTransform(np.array(list([item.x, item.y] for item in rect)), dst)
  return cv2.warpPerspective(img, M, (maxWidth, maxHeight))