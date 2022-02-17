import os.path

def getExtension(path):
  """Return extension from file path.
  Args:
    path: File Path.
  Returns:
    File extension, e.g. png.
  """
  # Get extension.
  name = os.path.basename(path).split('.')
  if len(name) < 2:
    return None
  return name[1].lower()