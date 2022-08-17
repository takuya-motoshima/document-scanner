import cv2
from importlib import import_module
import importlib

def displayImage(title, img):
  """Display images on the screen.
  Args:
      title (str): Display title.
      img (numpy.ndarray): CV2 Image.
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

    # Calculates the size and position of the image displayed in the center of the terminal window.
    if height > screenHeight or width > screenWidth:
      if height / screenHeight >= width / screenWidth:
        multiplier = screenHeight / height
      else:
        multiplier = screenWidth / width
  
      # Resize image.
      dstImg = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)

    x = round(screenWidth / 2 - (width * multiplier) / 2)
    y = round(screenHeight / 2 - (height * multiplier) / 2)
    cv2.moveWindow(title, x, y)

  # Show image.
  cv2.imshow(title, dstImg)

  # Destroy the window.
  cv2.waitKey(0)
  cv2.destroyAllWindows()