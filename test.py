import sys
import utils
import matplotlib.pyplot as plt


# ------------------------------ Get an argument test. ------------------------------ #
# # Get an argument.
# if len(sys.argv) < 2:
#   raise Exception('Missing argument name')
# print(f'Hello {sys.argv[1]}')

# ------------------------------ Testing utils.detectDataURL ------------------------------ #
print('------------------------------ Valid cases:')
for str in [
  'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC',
  'data:image/svg+xml;charset=utf-8,.',
  'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIBAMAAAA2IaO4AAAAFVBMVEXk5OTn5+ft7e319fX29vb5+fn///++GUmVAAAALUlEQVQIHWNICnYLZnALTgpmMGYIFWYIZTA2ZFAzTTFlSDFVMwVyQhmAwsYMAKDaBy0axX/iAAAAAElFTkSuQmCC',
  '   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIBAMAAAA2IaO4AAAAFVBMVEXk5OTn5+ft7e319fX29vb5+fn///++GUmVAAAALUlEQVQIHWNICnYLZnALTgpmMGYIFWYIZTA2ZFAzTTFlSDFVMwVyQhmAwsYMAKDaBy0axX/iAAAAAElFTkSuQmCC   ',
  ' data:,Hello%2C%20World!',
  ' data:,Hello World!',
  ' data:text/plain;base64,SGVsbG8sIFdvcmxkIQ%3D%3D',
  ' data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E',
  'data:,A%20brief%20note',
  'data:text/html;charset=US-ASCII,%3Ch1%3EHello!%3C%2Fh1%3E',
  'data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22100%22%20height%3D%22100%22%3E%3Crect%20fill%3D%22%2300B1FF%22%20width%3D%22100%22%20height%3D%22100%22%2F%3E%3C%2Fsvg%3E',
  'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCBmaWxsPSIjMDBCMUZGIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIvPjwvc3ZnPg=='
]:
  res = utils.detectDataURL(str)
  if res:
    print(f'right: "{res[0]}" "{str[:50]}"')
  else:
    print(f'wrong: "{str[:50]}"')

print('------------------------------ Invalid case:')
for str in [
  'dataxbase64',
  'data:HelloWorld',
  'data:text/html;charset=,%3Ch1%3EHello!%3C%2Fh1%3E',
  'data:text/html;charset,%3Ch1%3EHello!%3C%2Fh1%3E',
  'data:base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC',
  '',
  'http://wikipedia.org',
  'base64',
  'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC'
]:
  res = utils.detectDataURL(str)
  if res:
    print(f'right: {res[0]} "{str[:50]}"')
  else:
    print(f'wrong: "{str[:50]}"')
