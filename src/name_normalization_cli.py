def main():
  # Get command options.
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input', type=str, required=True, help='Person\'s Name')
  options = DotMap(vars(parser.parse_args()))

  # Normalized name.
  divideName = NameDivider().divide_name(options.input)

  # Output the normalization result as JSON.
  print(json.dumps(dict(
    firstName = divideName.given,
    lastName = divideName.family,
    score = divideName.score
  ), ensure_ascii=False, indent = 4))
if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from namedivider import NameDivider
  main()