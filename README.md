# document-scanner
Detect documents from images.

Scan Japanese driver's license card:  
![driver's-license.png](screencaps/driver's-license.png)

If it is rotating in the roll direction.
![driver's-license2.png](screencaps/driver's-license2.png)

If it is rotating in the pitch direction:  
![driver's-license3.png](screencaps/driver's-license3.png)

Scan Japanese My Number Card:  
![my-number.png](screencaps/my-number.png)

## Documentation
* [Changelog](CHANGELOG.md)

## Requirements
- Python 3.9 (tested under Python 3.9.10)
- opencv-python 4.5.5.62
- opencv-contrib-python 4.5.5.62
- google-cloud-vision 2.6.3
- python-dotenv 0.19.2
- dotmap 1.3.30

## Installation
Install dependent packages.  
```sh
python -m pip install --no-cache-dir -r requirements.txt
# python3.9 -m pip install --no-cache-dir -r requirements.txt
```

Create an .env file and write your Google Vision credentials as follows.
```text
GOOGLE_APPLICATION_CREDENTIALS={"type": "service_account","project_id": "vision-api-288806","private_key_id": "XXX","private_key": "-----BEGIN PRIVATE KEY-----\nXXX","client_email": "XXX","client_id": "XXX","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/XXX"}
```

## Usage
Use scan.py to scan the document in Python.  

Aspect ratio of the scanned object:
|Type|ISO/IEC 7810|Size|
|--|--|--|
|Driver's license card|ID-1|85.60 × 53.98 mm|
|My number card size|ID-1|85.60 × 53.98 mm|

### Scan Help
```sh
python src/scan.py --help
# Output: usage: scan.py [-h] -i INPUT [-o OUTPUT] [-p] -t {driverslicense,mynumber} [-d]
#         optional arguments:
#           -h, --help            show this help message and exit
#           -i INPUT, --input INPUT
#                                 Image path or Data URL
#           -o OUTPUT, --output OUTPUT
#                                 Output image path of the found document
#           -p, --print           Print the Data URL of the detected document
#           -t {driverslicense,mynumber}, --type {driverslicense,mynumber}
#                                 OCR document type
#           -d, --debug           Display debug image on display
```

### Scan Japanese driver's license card.
```sh
python src/scan.py -i img/license.png -t driverslicense --debug
```

### Scan Japanese My Number Card.
```sh
python src/scan.py -i img/mynumber.png -t mynumber --debug
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