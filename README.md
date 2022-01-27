# document-scanner
Detect documents from images.

## Getting Started
sInstalling OpenCV for Python3
```sh
pip3 install opencv-python
pip3 install opencv-contrib-python
pip3 install matplotlib
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
#   -i IMAGE, --image IMAGE
#                         increase output verbosity
#   -r ASPECTRATIO, --aspect-ratio ASPECTRATIO
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

## Unit test
Run all test cases in the tests directory.
```sh
python -m unittest discover -v tests
# test_right_for_detect_data_url (test_utils.TestUtils) ... ok
# test_wrong_for_detect_data_url (test_utils.TestUtils) ... ok
# ----------------------------------------------------------------------
# Ran 2 tests in 0.001s
# OK
```

Run only one test case.
```sh
python -m unittest -v tests.test_utils
# test_right_for_detect_data_url (tests.test_utils.TestUtils) ... ok
# test_wrong_for_detect_data_url (tests.test_utils.TestUtils) ... ok
# ----------------------------------------------------------------------
# Ran 2 tests in 0.001s
# OK
```

## Author

**Takuya Motoshima**

* [github/takuya-motoshima](https://github.com/takuya-motoshima)
* [twitter/TakuyaMotoshima](https://twitter.com/TakuyaMotoshima)
* [facebook/takuya.motoshima.7](https://www.facebook.com/takuya.motoshima.7)

## License

[MIT](LICENSE)