import os.path

def get_extension(path):
  """Return extension from file path.
  Args:
      path (str): File Path.
  Returns:
      str: File extension, e.g. png.
  """
  basename = os.path.basename(path).split('.')
  if len(basename) < 2:
    return None
  return basename[1].lower()