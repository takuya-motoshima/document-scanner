import re
from datetime import datetime
from japanera import Japanera
from .validate_date import validate_date

def cleanup_japanese_expiration_date(text):
  """Clean up the expiration date of the Japanese calendar.
  Args:
      text (str): Expiration date of the Japanese calendar. e.g. 2022年(令和4年)3月11日 or 令和4年3月11日
  Returns:
      str: Expiration date of the Japanese calendar with superfluous characters removed. e.g. 2022年03月11日
  """
  if not text:
    return ''
  if matches := re.match(r'(\d{4})年(?:\(..*?\))?(\d{1,2})月(\d{1,2})日?', text):
    # If there is an era name between the year and month. e.g. 2022年 (令和4年)3月11日
    (year, month, day) = matches.groups()

    # If it is not correct as a date.
    date = f'{year}-{month}-{day}'
    if not validate_date(date, '%Y-%m-%d'):
      return ''
    return datetime.strptime(date,'%Y-%m-%d').strftime('%Y年%m月%d日')
  elif matches := re.match(r'(?:明治|大正|昭和|平成|令和)(?:\d{1,2}|元)年\d{1,2}月\d{1,2}日?', text):
    # If there is no era name between the year and month. e.g. 令和4年3月11日
    date = matches.group(0)

    # If there are no day units at the end of the text, add them.
    if not date.endswith('日'):
      date += '日'

    # Convert from Japanese calendar to Western calendar.
    janera = Japanera()
    if not (japanese_calendar := janera.strptime(date, '%-E%-kO年%-km月%-kd日')):
      return ''
    return japanese_calendar[0].strftime('%Y年%m月%d日')
  else:
    return ''