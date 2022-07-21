import json

def main():
  # Convert unnested dict to json.
  # Output: json1=(<class 'str'>){"name": "sathiyajith", "rollno": 56, "cgpa": 8.6, "phonenumber": "9976770500"}
  dic1 = dict(
    name = 'sathiyajith',
    rollno = 56,
    cgpa = 8.6,
    phonenumber = '9976770500'
  )
  json1 = json.dumps(dic1)
  print(f'json1=({type(json1)}){json1}')

  # Convert nested dict to json.
  # Output: json2=(<class 'str'>){"Laptop": {"sony": 1, "apple": 2, "asus": 5}, "Camera": {"sony": 2, "sumsung": 1, "nikon": 4}}
  dic2 = dict(
    Laptop = dict(sony = 1, apple = 2, asus = 5),
    Camera = dict(sony = 2, sumsung = 1, nikon  = 4)
  )
  json2 = json.dumps(dic2)
  print(f'json2=({type(json2)}){json2}')

if __name__ == '__main__':
  main()