import cv2
import numpy as np
import utils
import sys

# define variable for resize ratio
resizeRatio = 1

def findContourV2(img):
	# Grayscale.
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	utils.show('Grayscale', grayImg)

	# Remove image noise.
	grayImg = cv2.medianBlur(grayImg, 5)
	grayImg = cv2.erode(grayImg, kernel=np.ones((5,5),np.uint8), iterations=1)
	grayImg = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
	utils.show('grayImg', grayImg)
	edgedImg = cv2.Canny(grayImg, 30, 400)
	# edgedImg = cv2.Canny(grayImg, 100, 200, apertureSize=3)
	utils.show('Edged', edgedImg)

	# Find the contour of the maximum area.
	cnts, _ = cv2.findContours(edgedImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnt = max(cnts, key = cv2.contourArea)
	return cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

def findContourV1(img):
	# Grayscale.
	grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	utils.show('Grayscale', grayImg)

	# Blur the image to remove noise.
	blurImg = cv2.GaussianBlur(grayImg, (5, 5), 0)
	utils.show('Blurred', blurImg)

	# Convert to a white and black image (binarized image).
	_, threshImg = cv2.threshold(grayImg, 128, 255, cv2.THRESH_BINARY)
	utils.show('Binarized', threshImg)

	# Find the contour of the maximum area.
	cnts, _ = cv2.findContours(threshImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnt = max(cnts, key = cv2.contourArea)
	return cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)

def convertContourToRect(cnt):
	# Initialzie a list of coordinates that will be ordered such that the first entry in the list is the top-left, the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left.
	pts = cnt.reshape(4, 2)
	rect = np.zeros((4, 2), dtype = 'float32')

	# The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum.
	sum = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(sum)] # top-left
	rect[2] = pts[np.argmax(sum)] # bottom-right

	# Now, compute the difference between the points, the top-right point will have the smallest difference, whereas the bottom-left will have the largest difference.
	diff = np.diff(pts, axis=1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# Returns the rectangle coordinates of the contour.
	return rect

def fourPointTransform(cnt, origImg):
	# Contour quadrilateral coordinates.
	rect = convertContourToRect(cnt)

	# Compute the width of the new image, which will be the maximum distance between bottom-right and bottom-left x-coordiates or the top-right and top-left x-coordinates
	(tl, tr, br, bl) = rect
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# Compute the height of the new image, which will be the maximum distance between the top-right and bottom-right y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# Now that we have the dimensions of the new image, construct the set of destination points to obtain a "birds eye view", (i.e. top-down view) of the image, again specifying points in the top-left, top-right, bottom-right, and bottom-left order.
	dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype = 'float32')

	# Compute the perspective transform matrix and then apply it.
	M = cv2.getPerspectiveTransform(rect, dst)
	return cv2.warpPerspective(origImg, M, (maxWidth, maxHeight))

def resizeImg(img, width=None, height=None, interpolation = cv2.INTER_AREA):
	global resizeRatio
	orgiWidth, orgiHeight, _ = img.shape
	print(f'orgiWidth={orgiWidth}, orgiHeight={orgiHeight}')
	if width is None and height is None:
		return img
	elif width is None:
		resizeRatio = height/orgiHeight
		width = int(orgiWidth * resizeRatio)
		print(f'width={width}, height={height}')
		resizedImg = cv2.resize(img, (height, width), interpolation)
		return resizedImg
	else:
		resizeRatio = width/orgiWidth
		height = int(orgiHeight * resizeRatio)
		print(f'width={width}, height={height}')
		resizedImg = cv2.resize(img, (height, width), interpolation)
		return resizedImg

# load an image
if len(sys.argv) < 2:
	raise Exception('Image path is required')
img = cv2.imread(sys.argv[1])

# Resize the image.
resizedImg = resizeImg(img, height=600)
utils.show('Original image', resizedImg)

# Make a copy.
copyResizedImg = resizedImg.copy()

# Find the largest document contour.
maxCnt = findContourV2(resizedImg)
# maxCnt = findContourV1(resizedImg)

# Draw a contour.
cv2.drawContours(copyResizedImg, [maxCnt], -1, (0,255,0), 3)
utils.show('Marked', copyResizedImg)

# Apply the four point tranform to obtain a "birds eye view" of the image.
warpImg = fourPointTransform(maxCnt/resizeRatio, img)
warpImg = resizeImg(warpImg, height=800)
utils.show('Warped', warpImg)