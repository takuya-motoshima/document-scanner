import re

def isDataUrl(str):
  """Check if it is a Data URL.
  Args:
      str (str): Character to check.
  Returns:
      bool: Returns True if the string is a DataURL, False if not.
  """
  matches = re.match(r'^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  return True if matches else False