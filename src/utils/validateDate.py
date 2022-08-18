from datetime import datetime

def validateDate(text, format = '%Y-%m-%d'):
  """Check date format.
  Args:
      text (str): Date string.
      format (str, optional): Date format. Defaults to '%Y-%m-%d'.
  Returns:
      bool: True for dates, false otherwise.
  """
  try:
    datetime.strptime(text, format)
    return True
  except ValueError:
    raise False