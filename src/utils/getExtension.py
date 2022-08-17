import os.path

def getExtension(path):
  """Return extension from file path.
  Args:
      path (str): File Path.
  Returns:
      str: File extension, e.g. png.
  """
  name = os.path.basename(path).split('.')
  if len(name) < 2:
    return None
  return name[1].lower()