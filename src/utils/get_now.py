import datetime

def get_now(format = None):
  """Returns the current date and time.
  Args:
      format (str, optional): Date and time format. e.g. '%Y%m%d%H%M%S'. Defaults to None.
  Returns:
      str: Returns the current date and time.
  """
  now = datetime.datetime.now()
  if not format:
    return now
  return now.strftime(format)
