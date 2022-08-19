import re
from datetime import datetime
from japanera import Japanera
from .validateDate import validateDate

def toWesternCalendarDate(text):
  """Convert a date in Japanese calendar format to Western calendar format.
  Args:
      text (str): Date in Japanese calendar format. e.g. 昭和61年5月1日
  Returns:
      str: Date in Western calendar format. e.g. 1986-05-01
  """
  if not (matches := re.match(r'(?:明治|大正|昭和|平成|令和)(?:\d{1,2}|元)年\d{1,2}月\d{1,2}日?', text)):
    return ''

  # If there is no era name between the year and month. e.g. 昭和61年5月1日
  date = matches.group(0)

  # If there are no day units at the end of the text, add them.
  if not date.endswith('日'):
    date += '日'

  # Convert from Japanese calendar to Western calendar.
  janera = Japanera()
  if not (japaneseCalendar := janera.strptime(date, '%-E%-kO年%-km月%-kd日')):
    return ''
  return japaneseCalendar[0].strftime('%Y-%m-%d')