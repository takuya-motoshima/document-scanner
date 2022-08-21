def main():
  # Get command options.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Address')
  options = DotMap(vars(parser.parse_args()))

  # Normalized address.
  normalizedAddress = normalize(options.input)

  # Output the normalization result as JSON.
  print(json.dumps(normalizedAddress, ensure_ascii=False, indent = 4))
if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from normalize_japanese_addresses import normalize
  main()