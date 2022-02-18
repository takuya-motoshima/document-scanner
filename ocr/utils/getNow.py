import datetime

def getNow(format = None):
  """Returns the current date and time.
  Args:
    format: Date and time format. e.g. '%Y%m%d%H%M%S'
  Returns:
    Returns the current date and time.
  """
  now = datetime.datetime.now()
  if not format:
    return now
  return now.strftime(format)
