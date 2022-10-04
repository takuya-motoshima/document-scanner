from .is_data_url import is_data_url
from .detect_data_url import detect_data_url
from .get_extension import get_extension

def get_mime_type(str):
  """Get MIME type.
  Args:
      str (str): Image Data URL or file path.
  Returns:
      str: MIME type (e.g. png, jpg).
  Raises:
      ValueError: A string without extension was specified.
  """
  if is_data_url(str):
    mime, _ = detect_data_url(str)
    return mime
  else:
    extension = get_extension(str)
    if not extension:
      raise ValueError('Invalid file path')
    if extension == 'jpg':
      return 'jpeg'
    else:
      return extension