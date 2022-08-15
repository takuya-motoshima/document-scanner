import numpy as np
from dotmap import DotMap

def contourToRect(contour):
  """Convert contour points (x, y) to four external rectangle points (x, y).
  Args:
    contour: Contour points (x, y).
  Returns:
    List of vertex coordinates (x, y).
  """
  # Initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left, the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left.
  points = contour.reshape(4, 2)
  rect = np.zeros((4, 2), dtype = 'float32')

  # The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum.
  sum = points.sum(axis = 1)
  rect[0] = points[np.argmin(sum)]# Top left coordinates.
  rect[2] = points[np.argmax(sum)]# Bottom right coordinate.

  # Now, compute the difference between the points, the top-right point will have the smallest difference, whereas the bottom-left will have the largest difference.
  diff = np.diff(points, axis=1)
  rect[1] = points[np.argmin(diff)]# Top right coordinates.
  rect[3] = points[np.argmax(diff)]# Bottom left coordinates.a

  # Convert to dict ([n][0] as x, [n][1] as y).
  rect = list(map(lambda item: DotMap(dict(zip(['x', 'y'], item))), rect))

  # Return the rectangle coordinates of the contour.
  return rect