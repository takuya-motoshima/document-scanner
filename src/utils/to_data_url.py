from .to_base64 import to_base64

def to_data_url(img, mime = None):
  """Image to Data URL.
  Args:
      img (numpy.ndarray|str): CV2 Image or image path.
      mime (str, optional): The media type of the Data URL. Required if the image is an CV2 Image. Defaults to None.
  Returns:
      tuple: Return Data URL and MIME type.
  """
  b64, _ = to_base64(img, mime)
  return f'data:image/{mime};base64,{b64}'