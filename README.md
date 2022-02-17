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

### Python
Use scan.py to scan the document in Python.

scan.py help.
```sh
python scan.py --help
# usage: scan.py [-h] -i IMAGE [-r ASPECTRATIO]
# 
# options:
#   -h, --help            show this help message and exit
#   -i IMAGE, --input IMAGE
#                         increase output verbosity
#   -r ASPECTRATIO, --aspect ASPECTRATIO
#                         Resize the scanned document to the specified aspect
#                         ratio. Typing as a width:height ratio (like 4:5 or
#                         1.618:1).
```

Find the document.
```sh
python scan.py -i img/license.png
```

Resize document to size Japanese driver's license.
```sh
python scan.py -i img/license.png -r 8.56:5.4
```

Find a document from an image Data URL.
```sh
python scan.py -r 8.56:5.4 -i "data:image/png;base64,iVB..."
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

## Author
**Takuya Motoshima**

* [github/takuya-motoshima](https://github.com/takuya-motoshima)
* [twitter/TakuyaMotoshima](https://twitter.com/TakuyaMotoshima)
* [facebook/takuya.motoshima.7](https://www.facebook.com/takuya.motoshima.7)

## License

[MIT](LICENSE)