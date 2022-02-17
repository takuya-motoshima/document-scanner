# document-scanner
Detect documents from images.

## Getting Started
Install dependent packages.
```sh
pip3 install opencv-python
pip3 install opencv-contrib-python
pip3 install matplotlib
pip3 install google-cloud-vision
pip3 install python-dotenv
pip3 install dotmap
```

## Usage
Use scan.py to scan the document in Python.

scan.py help.
```sh
python scan.py --help
# usage: scan.py [-h] -i INPUT [-o OUTPUT] [-p] -t {driverslicense,mynumber}
# 
# optional arguments:
#   -h, --help            show this help message and exit
#   -i INPUT, --input INPUT
#                         Image path or Data URL
#   -o OUTPUT, --output OUTPUT
#                         Output image path of the found document
#   -p, --print-data-url  Print the Dat URL of the document
#   -t {driverslicense,mynumber}, --type {driverslicense,mynumber}
#                         OCR document type
```

Scan Japanese driver's license card.
```sh
python scan.py -i img/license.png -t driverslicense
```

Scan Japanese My Number Card.
```sh
python scan.py -i img/mynumber.png -t mynumber
```

## Unit test
```sh
python -m unittest discover -v tests
# test_right_for_detect_data_url (test_utils.TestUtils) ... ok
# test_right_for_to_data_url (test_utils.TestUtils) ... ok
# test_wrong_for_detect_data_url (test_utils.TestUtils) ... ok
# 
# ----------------------------------------------------------------------
# Ran 3 tests in 0.004s
# 
# OK
```

## Others
**Driver's license card size:**  
ID-1 format. 85.60 x 53.98 mm.

**My number card size:**  
ID-1 format. 85.60 x 53.98 mm.

## Author
**Takuya Motoshima**

* [github/takuya-motoshima](https://github.com/takuya-motoshima)
* [twitter/TakuyaMotoshima](https://twitter.com/TakuyaMotoshima)
* [facebook/takuya.motoshima.7](https://www.facebook.com/takuya.motoshima.7)

## License

[MIT](LICENSE)