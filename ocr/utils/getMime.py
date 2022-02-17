import ocr.utils as utils

def getMime(str):
  """Returns the MIME type (e.g. png, jpg).
  Args:
    str: Image Data URL or file path.
  Returns:
    MIME type (e.g. png, jpg).
  """
  if utils.isDataURL(str):
    # For Data URL.
    mime, _ = utils.detectDataURL(str)
    return mime
  else:
    # For image path.
    # Get extension.
    ext = utils.getExtension(str)
    if not ext:
      raise ValueError('Invalid file path')

    # Return MIME type.
    if ext == 'jpg' or ext == 'jpeg':
      return 'jpeg'
    elif ext=='png':
      return 'png'
    else:
      return ext
