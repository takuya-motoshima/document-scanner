# python -m prototype.binarization
import cv2
import numpy as np
from pathlib import Path
import src.utils as utils

# Load the image.
imgDir = f'{Path(__file__).parents[1]}/img'
img = cv2.imread(f'{imgDir}/tmp.jpg')

# Grayscale the image.
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
utils.displayImage('Grayscale', grayImg)

# Blur the image and remove noise.
medianImg = cv2.medianBlur(grayImg, ksize=9)
utils.displayImage('Median', medianImg)

# Remove white noise. Shrink the white part and dilate the black part.
erosionImg = cv2.erode(medianImg, kernel=np.ones((5,5), np.uint8), iterations=1)
utils.displayImage('Erosion', erosionImg)

# Binarize the image (colors to black and white only).
threshImg = cv2.adaptiveThreshold(erosionImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
utils.displayImage('Thresh', threshImg)

# Detect image edges.
edgedImg = cv2.Canny(threshImg, 30, 400)
# edgedImg = cv2.Canny(threshImg, 100, 200, apertureSize=3)
utils.displayImage('Edged', edgedImg)