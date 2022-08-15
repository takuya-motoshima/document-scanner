import cv2

def main():
  # Load the image.
  img = cv2.imread('../img/edge.png')

  # Grayscale the image.
  grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  _, binImg = cv2.threshold(grayImg, 20, 255, cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(binImg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  for contour in contours:
    # Calculate perimeter.
    peri = cv2.arcLength(contour, True)

    # Approximate contour.
    approx = cv2.approxPolyDP(contour, 0.005 * peri, True)
    if len(approx) == 4:
      # If it is a rectangle.
      cv2.drawContours(img, [approx], -1, (0,255,0), 3)
  cv2.imshow('result', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()