from .toBase64 import toBase64

def toDataUrl(img, mime = None):
  """Image to Data URL.
  Args:
      img (numpy.ndarray|str): CV2 Image or image path.
      mime (str, optional): The media type of the Data URL. Required if the image is an CV2 Image. Defaults to None.
  Returns:
      tuple: Return Data URL and MIME type.
  """
  # to base64.
  b64, mime = toBase64(img, mime)

  # Generates and returns a Data URL string based on base64.
  return f'data:image/{mime};base64,{b64}', mime