def main():
  args = _get_args()
  normalized_address = normalize(args.address)
  print(json.dumps(normalized_address, ensure_ascii=False, indent = 4))

def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--address', type=str, required=True, help='Address')
  return DotMap(vars(parser.parse_args()))

if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from normalize_japanese_addresses import normalize
  main()