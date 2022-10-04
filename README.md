# document-scanner
Scan the text of a document.

- Scan Japanese driver's license card:  
    ![driverslicense.png](screencaps/driverslicense.png)
- If it is rotating in the roll direction.
    ![driverslicense2.png](screencaps/driverslicense2.png)
- If it is rotating in the pitch direction:  
    ![driverslicense3.png](screencaps/driverslicense3.png)
- Scan Japanese My Number Card:  
    ![mynumber.png](screencaps/mynumber.png)

## Documentation
* [Changelog](CHANGELOG.md)
* [How to use the template](HOW_TO_TEMPLATE.md)

## Requirements
Python is 3.9.  
See [requirements.txt](requirements.txt) for dependencies.

## Installation
1. Create a virtual environment.  
    This is necessary to avoid dependency package conflicts with other projects using the same dependency package.
    ```sh
    python -m venv document-scanner-env
    ```
1. Start the virtual environment.
    After this is done, execute the pip command to add the library to the virtual environment.  
    Also, executing the python command will use only the libraries registered in the virtual environment.  

    Windows:  
    ```sh
    document-scanner-env\Scripts\activate
    ```

    Linux or Mac:  
    ```sh
    source document-scanner-env/bin/activate
    ```

    If the execution is successful, the environment name is added to the beginning of the command line as follows.  
    ```sh
    PS C:\workspaces\document-scanner>
    ```
1. Install dependent packages.  
    ```sh
    python -m pip install --no-cache-dir -r requirements.txt
    # python3.9 -m pip install --no-cache-dir -r requirements.txt
    ```
1. Create an .env file and write your Google Vision credentials as follows.
    ```text
    GOOGLE_APPLICATION_CREDENTIALS={"type": "service_account","project_id": "XXX","private_key_id": "XXX","private_key": "-----BEGIN PRIVATE KEY-----\nXXX","client_email": "XXX","client_id": "XXX","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/XXX"}
    ```

## Usage
- Aspect ratio of the scanned object:
    |Type|ISO/IEC 7810|Size|
    |--|--|--|
    |Driver's license card|ID-1|85.60 × 53.98 mm|
    |My number card size|ID-1|85.60 × 53.98 mm|
- Scan Help
    ```sh
    python src/scan_cli.py --help
    # optional arguments:
    #   -h, --help            show this help message and exit
    #   -i IMG, --input IMG
    #                         Image path or Data URL
    #   -t {driverslicense,mynumber}, --type {driverslicense,mynumber}
    #                         OCR document type
    #   -d, --debug           Display debug image on display
    ```
- Scan Japanese driver's license card.
    ```sh
    python src/scan_cli.py -i img/driverslicense.png -t driverslicense --debug
    # {
    #     "fullName": "日本本花子",
    #     "firstName": "花子",
    #     "lastName": "日本",
    #     "age": 36,
    #     "birthday": "昭和61年5月1日",
    #     "wrnBirthday": "1986-05-01",
    #     "expiryDate": "2024年06月01日",
    #     "licenseNumber": "012345678900",
    #     "address": "東京都千代田区霞が関2-1-2",
    #     "normalizedAddress": {
    #         "pref": "東京都",
    #         "city": "千代田区",
    #         "town": "霞が関二丁目",
    #         "addr": "1-2"
    #     }
    # }
    ```
- Scan Japanese My Number Card.
    ```sh
    python src/scan_cli.py -i img/mynumber.png -t mynumber --debug
    # {
    #     "fullName": "番号花子",
    #     "firstName": "花子",
    #     "lastName": "番号",
    #     "age": 33,
    #     "gender": "女",
    #     "birthday": "平成元年3月31日",
    #     "wrnBirthday": "1989-03-31",
    #     "cardExpiryDate": "2025年03月31日",
    #     "digiExpiryDate": "2020年03月31日",
    #     "address": "東京都千代田区霞が関2-1-2",
    #     "normalizedAddress": {
    #         "pref": "東京都",
    #         "city": "千代田区",
    #         "town": "霞が関二丁目",
    #         "addr": "1-2"
    #     }
    # }
    ```
- Normalized name.
    ```sh
    python src/name_normalization_cli.py  --name "山田花子"
    # {
    #   "firstName": "花子",
    #   "lastName": "山田",
    #   "score": 0.4338249661652486
    # }
    ```
- Normalized address.
    ```sh
    python src/address_normalization_cli.py  --address "東京都千代田区霞ヶ関2-1-2"
    # {
    #   "pref": "東京都",
    #   "city": "千代田区",
    #   "town": "霞が関二丁目",
    #   "addr": "1-2",
    #   "lat": 35.675551,
    #   "lng": 139.750413,
    #   "level": 3
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