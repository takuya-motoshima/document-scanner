import cv2

def resizeImage(img, width=None, height=None, intrpl = cv2.INTER_AREA):
  """Resize the image.
  Args:
      img (numpy.ndarray): CV2 Image.
      width (int, optional): Width after resizing. Defaults to None.
      height (int, optional): Height after resizing. Defaults to None.
      intrpl (int, optional): Interpolation flag that takes one of the following methods. Defaults to cv2.INTER_AREA.
        cv2.INTER_NEAREST: nearest neighbor interpolation.
        cv2.INTER_LINEAR: bilinear interpolation.
        cv2.INTER_CUBIC: bicubic interpolation.
        cv2.INTER_AREA: resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire'-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.
        cv2.INTER_LANCZOS4: Lanczos interpolation over 8x8 neighborhood.
  Returns:
      numpy.ndarray: Resized image.
  """  
  ratio = 1
  origWidth, origHeight = img.shape[:2]
  if width is None and height is None:
    return img, ratio
  elif width is None:
    ratio = height / origHeight
    width = int(origWidth * ratio)
    resizeImg = cv2.resize(img, (height, width), intrpl)
    return resizeImg, ratio
  else:
    ratio = width / origWidth
    height = int(origHeight * ratio)
    resizeImg = cv2.resize(img, (height, width), intrpl)
    return resizeImg, ratio