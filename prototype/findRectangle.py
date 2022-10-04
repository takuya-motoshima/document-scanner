"""
python -m prototype.findRectangle -i img/tmp4.jpg
python -m prototype.findRectangle -i img/edge.png
"""
import cv2
import argparse
from dotmap import DotMap
import src.utils as utils

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
args = DotMap(vars(parser.parse_args()))

img = cv2.imread(args.input)

grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
grayImg = cv2.GaussianBlur(grayImg, (1,1), 1000)
# grayImg = cv2.GaussianBlur(grayImg, (3, 3), 0)
# _, grayImg = cv2.threshold(grayImg, 20, 255, cv2.THRESH_BINARY)
utils.display_img('grayImg', grayImg)

_, grayImg = cv2.threshold(grayImg, 120, 255, cv2.THRESH_BINARY)
utils.display_img('grayImg', grayImg)

edgeImg = cv2.Canny(grayImg, 10, 250)
utils.display_img('edgeImg', edgeImg)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closedImg = cv2.morphologyEx(edgeImg, cv2.MORPH_CLOSE, kernel)
utils.display_img('closedImg', closedImg)

contours, _ = cv2.findContours(closedImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours, _ = cv2.findContours(grayImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
  peri = cv2.arcLength(contour, True)
  approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
  # approx = cv2.approxPolyDP(contour, 0.005 * peri, True)
  if len(approx) == 4:
    cv2.drawContours(img, [approx], -1, (0,255,0), 5)
utils.display_img('img', img)