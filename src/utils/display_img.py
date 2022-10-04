import cv2
from importlib import import_module
import importlib

def display_img(label, img):
  """Display images on the screen.
  Args:
      label (str): Display label.
      img (numpy.ndarray): CV2 Image.
  """
  cv2.namedWindow(label) 
  height, width = img.shape[:2]
  multiplier = 1
  dst_img = img
  if importlib.util.find_spec('tkinter'):
    tk = import_module('tkinter')
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    if height > screen_height or width > screen_width:
      if height / screen_height >= width / screen_width:
        multiplier = screen_height / height
      else:
        multiplier = screen_width / width
      dst_img = cv2.resize(img, (0, 0), fx=multiplier, fy=multiplier)
    x = round(screen_width / 2 - (width * multiplier) / 2)
    y = round(screen_height / 2 - (height * multiplier) / 2)
    cv2.moveWindow(label, x, y)
  cv2.imshow(label, dst_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()