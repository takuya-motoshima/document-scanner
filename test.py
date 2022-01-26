import base64
import os.path
import sys

# # Get an argument.
# if len(sys.argv) < 2:
#   raise Exception('Missing argument name')
# print(f'Hello {sys.argv[1]}')

# Image to data URI.
def imgToDataURL(path):
  # Find the image extension.
  name = os.path.basename(path).split('.')
  ext = name[1].lower() if len(name) > 1 else None
  print(f'ext={ext}')

  # base64 media type.
  mediaType = None
  if ext == 'jpg' or ext == 'jpeg':
    mediaType = 'jpeg'
  elif ext=='png':
    mediaType = 'png'
  else:
    # Returns an error for images other than png and jpg.
    raise ValueError('Invalid image type')

  # Image bytes object.
  with open(path, 'rb') as f:
    bytes = f.read()
  
  # Bytes object to base64.
  b64 = base64.b64encode(bytes).decode('utf-8')

  # Convert base64 to DataURL and return.
  return 'data:image/' + mediaType + ';base64,' + b64

dataURL = imgToDataURL('img/license.png')
print(f'dataURL={dataURL[:100]}')