from .isDataUrl import isDataUrl
from .detectDataUrl import detectDataUrl
from .getExtension import getExtension

def getMime(str):
  """Get MIME type.
  Args:
    str: Image Data URL or file path.
  Returns:
    MIME type (e.g. png, jpg).
  """
  if isDataUrl(str):
    mime, _ = detectDataUrl(str)
    return mime
  else:
    extension = getExtension(str)
    if not extension:
      raise ValueError('Invalid file path')

    # Return MIME type.
    if extension == 'jpg':
      return 'jpeg'
    else:
      return extension
