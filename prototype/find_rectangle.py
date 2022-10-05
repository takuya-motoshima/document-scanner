"""
python -m prototype.find_rectangle -i img/driverslicense.png
"""
import cv2
import argparse
from dotmap import DotMap
import src.utils as utils

def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--img', type=str, required=True, help='Image path or Data URL')
  return DotMap(vars(parser.parse_args()))

args = _get_args()
img = cv2.imread(args.img)
orig_img = img.copy()
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img, (1,1), 1000)
_, thresh_img = cv2.threshold(blur_img, 120, 255, cv2.THRESH_BINARY)
edge_img = cv2.Canny(thresh_img, 10, 250)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
close_img = cv2.morphologyEx(edge_img, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(close_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
  peri = cv2.arcLength(contour, True)
  approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
  if len(approx) == 4:
    cv2.drawContours(orig_img, [approx], -1, (0,255,0), 3)
utils.display_img('result', orig_img)