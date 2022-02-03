import sys

name = sys.argv[1] if len(sys.argv) > 1 else 'unknown'
print(f'Hello, {name}')