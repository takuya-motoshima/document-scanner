import cv2

def resizeImage(img, width=None, height=None, intrpl = cv2.INTER_AREA):
  """Resize the image.
  Args:
    img: CV2 Image object.
    width: Width after resizing.
    height: Height after resizing.
    intrpl: Interpolation flag that takes one of the following methods.
            cv2.INTER_NEAREST: nearest neighbor interpolation.
            cv2.INTER_LINEAR: bilinear interpolation.
            cv2.INTER_CUBIC: bicubic interpolation.
            cv2.INTER_AREA: resampling using pixel area relation. It may be a preferred method for image decimation, as it gives moire'-free results. But when the image is zoomed, it is similar to the INTER_NEAREST method.
            cv2.INTER_LANCZOS4: Lanczos interpolation over 8x8 neighborhood.
  Returns:
    Return a resized CV2 Image object.
  """
  resizeRatio = 1
  origWidth, origHeight, _ = img.shape
  if width is None and height is None:
    return img, resizeRatio
  elif width is None:
    resizeRatio = height / origHeight
    width = int(origWidth * resizeRatio)
    resizedImg = cv2.resize(img, (height, width), intrpl)
    return resizedImg, resizeRatio
  else:
    resizeRatio = width / origWidth
    height = int(origHeight * resizeRatio)
    resizedImg = cv2.resize(img, (height, width), intrpl)
    return resizedImg, resizeRatio
