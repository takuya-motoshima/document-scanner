import cv2
from importlib import import_module
import importlib

def show(title, img):
# def show(title, img, scaleWidth = 500):
  """Show image on display.
  Args:
    title: Display title.
    img: CV2 Image object.
  """
  # Create a window.
  cv2.namedWindow(title) 

  height, width = img.shape[:2]

  # Image magnification.
  multiplier = 1

  # Check if the GUI tool tkinter is installed.
  dstImg = img
  if importlib.util.find_spec('tkinter'):
    # Get the terminal window size.
    tk = import_module('tkinter')
    root = tk.Tk()
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    root.destroy()
    # print(f'Screen size: {screenWidth}/{screenHeight}')

    # Calculates the size and position of the image displayed in the center of the terminal window.
    if height > screenHeight or width > screenWidth:
      if height / screenHeight >= width / screenWidth:
        multiplier = screenHeight / height
      else:
        multiplier = screenWidth / width
  
      # Resize image.
      dstImg = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)
      # scaleHeight = round(height * (scaleWidth / width))
      # dstImg = cv2.resize(img, dsize=(scaleWidth, scaleHeight))

    x = round(screenWidth / 2 - (width * multiplier) / 2)
    y = round(screenHeight / 2 - (height * multiplier) / 2)
    # print(f'Image position: {x}/{y}')
    cv2.moveWindow(title, x, y)

  # Show image.
  cv2.imshow(title, dstImg)

  # Destroy the window.
  cv2.waitKey(0)
  cv2.destroyAllWindows()