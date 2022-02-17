import logging
import datetime

# Initialize the logger.
now = datetime.datetime.now().strftime('%Y%m%d')
logging.basicConfig(
  filename = f'logs/{now}.log',
  level = logging.DEBUG,
  format = '%(levelname)s - %(asctime)s -> %(filename)s: %(message)s',
  encoding = 'utf-8')
# # Logger initialization flag.
# initialized = False
# def debug(*args):
#   # Initialize the logger.
#   global initialized
#   if not initialized:
#     logging.basicConfig(
#       filename='scan.log',
#       level=logging.DEBUG,
#       format="%(levelname)s - %(asctime)s -> %(filename)s: %(message)s")
#     initialized = True
#   # Join messages.
#   message = ' '.join(map(str, args))
#   logging.debug(message)