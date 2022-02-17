import re

def isDataURL(str):
  """Check if it is a Data URL.
  Args:
    str: Character to check.
  Returns:
    Returns True if the string is a DataURL, False if not.
  """
  matches = re.match(r'^\s*data:(?:(\w+\/[\w\d\-+.]+)(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  return True if matches else False