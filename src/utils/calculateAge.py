from datetime import datetime, date

def calculateAge(birthday):
  """Calculate age.
  Args:
      birthday (str): Birthdays in %Y-%m-%d format.
  Returns:
      int: Age.
  """
  # Today.
  today = date.today()

  # Birthday string to datetime object.
  birthday = datetime.strptime(birthday, '%Y-%m-%d')

  # Calculate age.
  return (int(today.strftime('%Y%m%d')) - int(birthday.strftime('%Y%m%d'))) // 10000