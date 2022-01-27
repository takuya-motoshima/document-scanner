import unittest
import utils
import numpy as np

class TestUtils(unittest.TestCase):
	def test_right_for_detect_data_url(self):
		cases = [
			'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC',
			'data:image/svg+xml;charset=utf-8,.',
			'data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIBAMAAAA2IaO4AAAAFVBMVEXk5OTn5+ft7e319fX29vb5+fn///++GUmVAAAALUlEQVQIHWNICnYLZnALTgpmMGYIFWYIZTA2ZFAzTTFlSDFVMwVyQhmAwsYMAKDaBy0axX/iAAAAAElFTkSuQmCC',
			'   data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIBAMAAAA2IaO4AAAAFVBMVEXk5OTn5+ft7e319fX29vb5+fn///++GUmVAAAALUlEQVQIHWNICnYLZnALTgpmMGYIFWYIZTA2ZFAzTTFlSDFVMwVyQhmAwsYMAKDaBy0axX/iAAAAAElFTkSuQmCC   ',
			' data:,Hello%2C%20World!',
			' data:,Hello World!',
			' data:text/plain;base64,SGVsbG8sIFdvcmxkIQ%3D%3D',
			' data:text/html,%3Ch1%3EHello%2C%20World!%3C%2Fh1%3E',
			'data:,A%20brief%20note',
			'data:text/html;charset=US-ASCII,%3Ch1%3EHello!%3C%2Fh1%3E',
			'data:image/svg+xml;charset=utf-8,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22100%22%20height%3D%22100%22%3E%3Crect%20fill%3D%22%2300B1FF%22%20width%3D%22100%22%20height%3D%22100%22%2F%3E%3C%2Fsvg%3E',
			'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMDAiIGhlaWdodD0iMTAwIj48cmVjdCBmaWxsPSIjMDBCMUZGIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIvPjwvc3ZnPg=='
		]
		for case in cases:
			with self.subTest(case):
				res = utils.detectDataURL(case)
				self.assertIsNotNone(res)

	def test_wrong_for_detect_data_url(self):
		cases = [
			'dataxbase64',
			'data:HelloWorld',
			'data:text/html;charset=,%3Ch1%3EHello!%3C%2Fh1%3E',
			'data:text/html;charset,%3Ch1%3EHello!%3C%2Fh1%3E',
			'data:base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC',
			'',
			'http://wikipedia.org',
			'base64',
			'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAAD///+l2Z/dAAAAM0lEQVR4nGP4/5/h/1+G/58ZDrAz3D/McH8yw83NDDeNGe4Ug9C9zwz3gVLMDA/A6P9/AFGGFyjOXZtQAAAAAElFTkSuQmCC'
		]
		for case in cases:
			with self.subTest(case):
				res = utils.detectDataURL(case)
				self.assertIsNone(res)

	def test_right_for_to_data_url(self):
		cases = [
			['img/license.png', None],
			[np.zeros((100, 100, 3)), 'png'] # 100x100 image
		]
		for case in cases:
			with self.subTest(case):
				img, mediaType = case
				res = utils.toDataURL(img, mediaType)
				self.assertRegex(res,  r'^data:..*$')

if __name__ == '__main__':
  unittest.main()