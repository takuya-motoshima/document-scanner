import re

def cleanupJapaneseCalendarBirthday(text):
  """Clean up the Japanese calendar birthdays.
  Args:
      text (str): Birthday of the Japanese calendar. e.g. 昭和61年5月1日
  Returns:
      str: Japanese calendar birthdays with extra characters removed.
  """
  # If the text is empty.
  if not text:
    return ''

  # Check the text format.
  matches = re.match(r'(?:明治|大正|昭和|平成|令和)(?:\d{1,2}|元)年\d{1,2}月\d{1,2}日?', text)
  if not matches:
    # If the format does not match.
    return ''

  # Matched text.
  date = matches.group(0)

  # If there are no day units at the end of the text, add them.
  if not date.endswith('日'):
    date += '日'
  return date
