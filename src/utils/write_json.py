import json

def write_json(path, data):
  """Write the data to a file as JSON.
  Args:
      path (str): File Path.
      data (dict): Data written to the file as JSON.
  """
  with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2, separators=(',', ': '))