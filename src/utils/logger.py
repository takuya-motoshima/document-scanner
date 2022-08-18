import logging
import datetime

# Log file name. It is the current date.
now = datetime.datetime.now().strftime('%Y%m%d')

# Initialize the logger.
logging.basicConfig(
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s(%(lineno)s): %(message)s',
  encoding = 'utf-8',
  handlers=[
    logging.FileHandler(f'logs/{now}.log')
    # Output to console window.
    # ,logging.StreamHandler()
  ]
)