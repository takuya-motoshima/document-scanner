import cv2
import os
import sys
sys.path.append(os.path.abspath('..'))
import ocr.utils as utils

def main():
  img = cv2.imread('../img/edge.jpg')
  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  _, binImg = cv2.threshold(grayImg, 20, 255, cv2.THRESH_BINARY)
  cnts, _ = cv2.findContours(binImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for cnt in cnts:
    # Calculate perimeter.
    peri = cv2.arcLength(cnt, True)

    # Approximate contour.
    approx = cv2.approxPolyDP(cnt, 0.005 * peri, True)
    print(f'number of sides={len(approx)}')
    if len(approx) == 4:
      # If it is a rectangle.
      cv2.drawContours(img, [approx], -1, (0, 255, 0), 3)
  utils.show('result', img)

if __name__ == '__main__':
  main()