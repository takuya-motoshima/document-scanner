import logging
import datetime

# Initialize the logger.
now = datetime.datetime.now().strftime('%Y%m%d')
logging.basicConfig(
  # filename = f'logs/{now}.log',
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s(%(lineno)s): %(message)s',
  encoding = 'utf-8',
  handlers=[
    logging.FileHandler(f'logs/{now}.log'),
    logging.StreamHandler()
  ]
)