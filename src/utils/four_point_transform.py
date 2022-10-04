import cv2
import numpy as np
from .contour_to_rect import contour_to_rect

def four_point_transform(contour, img):
  """Return a Keystone correction image (ndarray) of a rectangle on the image.
  Args:
      contour (numpy.ndarray): Contour points (x, y).
      img (numpy.ndarray): CV2 Image.
  Returns:
      numpy.ndarray: Return a Keystone correction image.
  """
  # Contour quadrilateral coordinates.
  rect = contour_to_rect(contour)

  # Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left x-coordiates or the top-right and top-left x-coordinates
  (top_left, top_right, bottom_right, bottom_left) = rect
  a_width = np.sqrt(((bottom_right.x - bottom_left.x) ** 2) + ((bottom_right.y - bottom_left.y) ** 2))
  b_width = np.sqrt(((top_right.x - top_left.x) ** 2) + ((top_right.y - top_left.y) ** 2))
  max_width = max(int(a_width), int(b_width))

  # Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates
  a_height = np.sqrt(((top_right.x - bottom_right.x) ** 2) + ((top_right.y - bottom_right.y) ** 2))
  b_height = np.sqrt(((top_left.x - bottom_left.x) ** 2) + ((top_left.y - bottom_left.y) ** 2))
  max_height = max(int(a_height), int(b_height))

  # Now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order.
  dst = np.array([
    [0, 0],
    [max_width - 1, 0],
    [max_width - 1, max_height - 1],
    [0, max_height - 1]
  ], dtype = 'float32')

  # Compute the perspective transform matrix and then apply it.
  M = cv2.getPerspectiveTransform(np.array(list([item.x, item.y] for item in rect)), dst)
  return cv2.warpPerspective(img, M, (max_width, max_height))