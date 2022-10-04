from datetime import datetime, date

def calc_age(birthday):
  """Calculate age.
  Args:
      birthday (str): Birthdays in %Y-%m-%d format.
  Returns:
      int: Age.
  """
  today = date.today()
  birthday = datetime.strptime(birthday, '%Y-%m-%d')
  return (int(today.strftime('%Y%m%d')) - int(birthday.strftime('%Y%m%d'))) // 10000