import logging
import datetime

now = datetime.datetime.now().strftime('%Y%m%d')
logging.basicConfig(
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s(%(lineno)s): %(message)s',
  encoding = 'utf-8',
  handlers=[
    logging.FileHandler(f'logs/{now}.log'),
    logging.StreamHandler()
  ]
)