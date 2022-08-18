import os
import logging
import datetime

# Log file name. It is the current date.
now = datetime.datetime.now().strftime('%Y%m%d')

# If there is no log output destination, create one.
logDir = 'logs'
if not os.path.exists(logDir):
  os.makedirs(logDir)

# Initialize the logger.
logging.basicConfig(
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s(%(lineno)s): %(message)s',
  encoding = 'utf-8',
  handlers=[
    logging.FileHandler(f'{logDir}/{now}.log')
    # Output to console window.
    # ,logging.StreamHandler()
  ]
)