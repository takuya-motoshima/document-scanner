import re

def detectDataUrl(str):
  """Detecting Data URL.
      data URI - MDN https://developer.mozilla.org/en-US/docs/data_URIs
      The "data" URL scheme: http://tools.ietf.org/html/rfc2397
      Valid URL Characters: http://tools.ietf.org/html/rfc2396#section2
  Args:
    str: String
  Returns:
    If the string is a DataURL, it returns the media type and base64. Otherwise returns None.
  """
  matches = re.match(r'^\s*data:(?:(?:\w+\/([\w\d\-+.]+))(?:;[\w-]+=[\w\d-]+)?)?(?:;base64)?,([\w\d!$&\',()*+;=\-._~:@\/?%\s]*)\s*$', str)
  if not matches:
    return None
  mime = matches.group(1)
  b64 = matches.group(2)
  return mime, b64