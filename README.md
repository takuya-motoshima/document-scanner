# document-scanner

Detect documents from images.

## Installing OpenCV for Python3
```sh
pip3 install opencv-python
pip3 install opencv-contrib-python
```

## How to use the document scan command
Command help.
```sh
node scan.js --help
# Document detection OCR application
# Options:
#   -i, --image <image>  Image path or Data URL
#   -h, --help           display help for command
```
## Python module unit test
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
