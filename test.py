import sys

if len(sys.argv) < 2:
  raise Exception('Missing argument name')

print(f'Hello {sys.argv[1]}')