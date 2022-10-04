def main():
  args = _get_args();
  divide_name = NameDivider().divide_name(args.name)
  print(json.dumps(dict(
    firstName = divide_name.given,
    lastName = divide_name.family,
    score = divide_name.score
  ), ensure_ascii=False, indent = 4))

def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('--name', type=str, required=True, help='Person\'s Name')
  return DotMap(vars(parser.parse_args()))

if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from namedivider import NameDivider
  main()