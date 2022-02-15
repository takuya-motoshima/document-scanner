import logging

# Initialize the logger.
logging.basicConfig(
  filename='scan.log',
  level=logging.DEBUG,
  format="%(levelname)s - %(asctime)s -> %(filename)s: %(message)s")
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
#   print(*args)