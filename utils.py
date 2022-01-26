import cv2
import tkinter as tk

def show(title, img):
# def show(title, img, scaleWidth = 500):
  """Show image on display.
  Args:
    title: Display title
    img: ndarray type image.
  """
  height, width = img.shape[:2]
  root = tk.Tk()
  screenWidth = root.winfo_screenwidth()
  screenHeight = root.winfo_screenheight()
  # print(f'screen={screenWidth}/{screenHeight}')
  root.destroy()
  multiplier = 1
  if height > screenHeight or width > screenWidth:
    if height / screenHeight >= width / screenWidth:
      multiplier = screenHeight / height
    else:
      multiplier = screenWidth / width
  dst = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)
  # scaleHeight = round(height * (scaleWidth / width))
  # dst = cv2.resize(img, dsize=(scaleWidth, scaleHeight))
  x = round(screenWidth / 2 - (width * multiplier) / 2)
  y = round(screenHeight / 2 - (height * multiplier) / 2)
  cv2.namedWindow(title) 
  cv2.moveWindow(title, x, y)
  cv2.imshow(title, dst)
  cv2.waitKey(0)
  cv2.destroyAllWindows()
