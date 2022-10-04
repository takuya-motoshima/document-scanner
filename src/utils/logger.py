import os
import logging
import datetime

log_file = f"{datetime.datetime.now().strftime('%Y%m%d')}.log"
log_dir = 'logs'
if not os.path.exists(log_dir):
  os.makedirs(log_dir)
logging.basicConfig(
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s(%(lineno)s): %(message)s',
  encoding = 'utf-8',
  handlers=[
    logging.FileHandler(f'{log_dir}/{log_file}')
    # ,logging.StreamHandler()
  ]
)