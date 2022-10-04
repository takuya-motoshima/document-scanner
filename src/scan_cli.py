def main():
  args = _get_args()
  debug_img_callback = None
  if args.debug:
    debug_img_callback = lambda label, img: utils.display_img(label, img)
  if args.fields:
    args.fields = args.fields.split(',')
  matches = scan(args.img, args.type, args.fields, debug_img_callback)
  matched_texts = extract_only_text_from_scan_results(matches)
  matched_json = json.dumps(matched_texts, ensure_ascii=False, indent = 4)
  # matched_json = json.dumps({key: (item.text if item.text else item) for key, item in matches.items()}, ensure_ascii=False, indent = 4)
  # matched_json = json.dumps({key: item.text for key, item in matches.items()}, ensure_ascii=False, indent = 4)
  utils.logging.debug(matched_json)
  print(matched_json)

def _get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--img', type=str, required=True, help='Image path or Data URL')
  parser.add_argument('-t', '--type', choices=['driverslicense', 'mynumber'], required=True, help='OCR document type')
  parser.add_argument('-d', '--debug', action='store_true', help='Display debug image on display', default=False)
  parser.add_argument('-f', '--fields', type=str, help='Fields to be scanned, default is all fields', default=None)
  return DotMap(vars(parser.parse_args()))

def extract_only_text_from_scan_results(matches):
  matched_texts = dict()
  for i, item in matches.items():
    if not i == 'normalizedAddress':
      matched_texts[i] = item.text
    else:
      matched_texts[i] = dict()
      for j, item in item.items():
        matched_texts[i][j] = item.text
  return matched_texts

if __name__ == '__main__':
  import argparse
  import json
  from dotmap import DotMap
  from scan import scan
  import utils
  main()