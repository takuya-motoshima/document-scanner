import numpy as np
import os
import sys
sys.path.append(os.path.abspath('..'))
import utils
import random

def main():
  # Create a Blank Image.
  img = np.zeros((500, 800, 3), np.uint8)

  # Rectangle point list.
  rects = [randRect(img.shape[1], img.shape[0]) for i in range(10)]

  # Sort the rectangles from top left to bottom right. 
  # Calculate the distance between the start point and the upper left point of the rectangle with np.linalg.norm.
  rects = sorted(rects, key=lambda rect: np.linalg.norm(np.array((rect[0][0], rect[0][1])) - np.array([0,0])))

  # debug. Print the coordinates of the rect and draw the rect on the image.
  for i, rect in enumerate(rects):
    utils.drawRect(img, rect[0], rect[2], utils.randColor(), str(i), drawTextBackground = False)
  utils.show('sorted', img)

def randRect(maxWd, maxHt): 
  """Generate random rectangular points.
  Args:
    maxWd: Maximum width of the rectangle.
    maxHt: Maximum height of the rectangle.
  """
  wd = random.randint(100, 200)
  ht = random.randint(100, 200)
  x = random.randint(0, maxWd - wd)
  y = random.randint(0, maxHt - ht)
  return np.array(((x, y), (x + wd, y), (x + wd, y + ht), (x, y + ht)))

if __name__ == '__main__':
  main()