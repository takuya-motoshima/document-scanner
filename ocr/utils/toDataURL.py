import ocr.utils as utils

def toDataURL(img, mime = None):
  """Image to Data URL.
  Args:
    img: CV2 Image object or image path.
    mime: The media type of the Data URL. Required if the image is an CV2 Image object.
  Returns:
    Return Data URL and MIME type.
  Raises:
    ValueError: Image types other than png, jpg, jpeg.
  """
  # to base64.
  b64, mime = utils.toBase64(img, mime)

  # Generates and returns a Data URL string based on base64.
  return f'data:image/{mime};base64,{b64}', mime