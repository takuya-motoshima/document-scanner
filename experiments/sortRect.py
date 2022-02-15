import numpy as np
import cv2
import random
import colorsys

def drawRect(img, pt1, pt2, color, label, drawTextBackground = True):
  """Draw rectangle with text.
  Args:
    img: CV2 Image object.
    pt1: The upper left point of the rectangle.
    pt2: The bottom right dot of the rectangle.
    color: Rectangle background color.
    label: text.
    drawTextBackground: Whether to draw a text background.
  """
  # Rectangle.
  cv2.rectangle(img, pt1, pt2, color, thickness=1)

  # Text boundaries.
  font = cv2.FONT_HERSHEY_SIMPLEX
  scale = .5
  thk = 1
  (width, height), _ = cv2.getTextSize(label, font, scale, thk)
  x, y = pt1

  # Text background.
  margin = 10
  labelColor = color
  if drawTextBackground:
    cv2.rectangle(img, (x, y - height - margin), (x + width + margin, y), color, thickness=-1)
    labelColor = (0, 0, 0)

  # Draw text.
  cv2.putText(img, label, (x + int(margin / 2), y - int(margin / 2)), font, scale, labelColor, thk)

def randRect(maxWidth, maxHeight, minX = None, minY = None):
  """Generate random rectangular points.
  Args:
    maxWidth: Maximum width of the rectangle.
    maxHeight: Maximum height of the rectangle.
  """
  width = random.randint(100, 200)
  height = random.randint(100, 200)
  x = random.randint(0, maxWidth - width)
  y = random.randint(0, maxHeight - height)
  return np.array(((x, y), (x + width, y), (x + width, y + height), (x, y + height)))

def randColor(bright=1):
  """Generate random colors.
  Args:
    bright: brightness.
  Returns:
    Returns BGR format colors.
  """
  hue = random.random()
  sat = random.random()
  val = bright
  return tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(hue, sat, val))

# Create a Blank Image.
img = np.zeros((500, 800, 3), np.uint8)

# Rectangle point list.
rects = [randRect(img.shape[1], img.shape[0]) for i in range(10)]

# Sort the rectangles from top left to bottom right. 
# Calculate the distance between the start point and the upper left point of the rectangle with np.linalg.norm.
rects = sorted(rects, key=lambda rect: np.linalg.norm(np.array((rect[0][0], rect[0][1])) - np.array([0,0])))

# debug. Print the coordinates of the rect and draw the rect on the image.
for i, rect in enumerate(rects):
  drawRect(img, rect[0], rect[2], randColor(), str(i), drawTextBackground = False)

cv2.imshow('sorted', img)
cv2.waitKey(0)
cv2.destroyAllWindows()