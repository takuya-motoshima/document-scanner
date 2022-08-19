# document-scanner
Scan the text of a document.

Scan Japanese driver's license card:  
![driverslicense.png](screencaps/driverslicense.png)

If it is rotating in the roll direction.
![driverslicense2.png](screencaps/driverslicense2.png)

If it is rotating in the pitch direction:  
![driverslicense3.png](screencaps/driverslicense3.png)

Scan Japanese My Number Card:  
![mynumber.png](screencaps/mynumber.png)

## Documentation
* [Changelog](CHANGELOG.md)

## Requirements
- Python 3.9 (tested under Python 3.9.10)
- numpy==1.22.1
- opencv-python 4.5.5.62
- opencv-contrib-python 4.5.5.62
- google-cloud-vision 2.6.3
- python-dotenv 0.19.2
- dotmap 1.3.30
- namedivider-python 0.1.0

The following is used for address normalization.
- kanjize 1.0.0
- requests 2.25.1
- pandas 1.2.4
- cachetools 4.2.2

## Installation
Install dependent packages.  
```sh
python -m pip install --no-cache-dir -r requirements.txt
# python3.9 -m pip install --no-cache-dir -r requirements.txt
```

Create an .env file and write your Google Vision credentials as follows.
```text
GOOGLE_APPLICATION_CREDENTIALS={"type": "service_account","project_id": "XXX","private_key_id": "XXX","private_key": "-----BEGIN PRIVATE KEY-----\nXXX","client_email": "XXX","client_id": "XXX","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/XXX"}
```

## Usage
Use scan_cli.py to scan the document in Python.  

Aspect ratio of the scanned object:
|Type|ISO/IEC 7810|Size|
|--|--|--|
|Driver's license card|ID-1|85.60 × 53.98 mm|
|My number card size|ID-1|85.60 × 53.98 mm|

### Scan Help
```sh
python src/scan_cli.py --help
# optional arguments:
#   -h, --help            show this help message and exit
#   -i INPUT, --input INPUT
#                         Image path or Data URL
#   -t {driverslicense,mynumber}, --type {driverslicense,mynumber}
#                         OCR document type
#   -d, --debug           Display debug image on display
```

### Scan Japanese driver's license card.
```sh
python src/scan_cli.py -i img/driverslicense.png -t driverslicense --debug
# Result:
# {
#     "fullName": "日本花子",
#     "birthday": "昭和61年5月1日生",
#     "address": "東京都千代田区霞が関2-1-2",
#     "expiryDate": "2024年(令和06年)06月01日まで有効",
#     "licenseNumber": "012345678900",
#     "firstName": "花子",
#     "lastName": "日本",
#     "normalizedAddress": {
#         "pref": "東京都",
#         "city": "千代田区",
#         "town": "霞が関二丁目",
#         "addr": "1-2"
#     }
# }
```

### Scan Japanese My Number Card.
```sh
python src/scan_cli.py -i img/mynumber.png -t mynumber --debug
# Result:
# {
#     "fullName": "番号花子",
#     "address": "東京都千代田区霞が関2-1-2",
#     "birthday": "平成元年3月31日生",
#     "cardExpiryDate": "2025年3月31日まで有効",
#     "digiExpiryDate": "2020年3月31日",
#     "gender": "女",
#     "firstName": "花子",
#     "lastName": "番号",
#     "normalizedAddress": {
#         "pref": "東京都",
#         "city": "千代田区",
#         "town": "霞が関二丁目",
#         "addr": "1-2"
#     }
# }
```

## Unit test
```sh
python -m unittest discover -v tests
```

## Author
**Takuya Motoshima**

* [github/takuya-motoshima](https://github.com/takuya-motoshima)
* [twitter/TakuyaMotoshima](https://twitter.com/TakuyaMotoshima)
* [facebook/takuya.motoshima.7](https://www.facebook.com/takuya.motoshima.7)

## License
[MIT](LICENSE)