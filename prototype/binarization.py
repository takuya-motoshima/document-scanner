"""
python -m prototype.binarization -i img/tmp4.jpg
"""
import cv2
import argparse
from dotmap import DotMap
import numpy as np
import src.utils as utils

def getArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Image path or Data URL')
  return DotMap(vars(parser.parse_args()))

args = getArgs()
img = cv2.imread(args.input)

# Grayscale the image.
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
utils.display_img('Grayscale', grayImg)

# Blur the image and remove noise.
medianImg = cv2.medianBlur(grayImg, ksize=9)
utils.display_img('Median', medianImg)

# Remove white noise. Shrink the white part and dilate the black part.
erosionImg = cv2.erode(medianImg, kernel=np.ones((5,5), np.uint8), iterations=1)
utils.display_img('Erosion', erosionImg)

# Binarize the image (colors to black and white only).
threshImg = cv2.adaptiveThreshold(erosionImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
utils.display_img('Thresh', threshImg)

# Detect image edges.
edgeImg = cv2.Canny(threshImg, 30, 400)
# edgeImg = cv2.Canny(threshImg, 100, 200, apertureSize=3)
utils.display_img('Edged', edgeImg)