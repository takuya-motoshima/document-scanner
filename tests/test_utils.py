import numpy as np
import unittest
import src.utils as utils

class TestUtils(unittest.TestCase):
  def test_right_detectDataUrl(self):
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
        self.assertIsNotNone(utils.detectDataUrl(case))
  def test_wrong_detectDataUrl(self):
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
        self.assertIsNone(utils.detectDataUrl(case))
  def test_right_toDataUrl(self):
    cases = [
      ['img/driverslicense.png', None],# Correct image path.
      [np.zeros((100, 100, 3)), 'png']# Image of correct ndarray type.
    ]
    for case in cases:
      with self.subTest(case):
        img, mime = case
        res = utils.toDataUrl(img, mime)
        self.assertRegex(res,  r'^data:..*$')
  def test_right_toDataUrl(self):
    cases = [
      ['img/driverslicense.png', None],# Correct image path.
      [np.zeros((100, 100, 3)), 'png']# Image of correct ndarray type.
    ]
    for case in cases:
      with self.subTest(case):
        img, mime = case
        b64, _ = utils.toDataUrl(img, mime)
        self.assertRegex(b64,  r'^data:..*$')
  def test_right_calcIoU(self):
    cases = [
      dict(input = [[0, 0, 10, 10], [0, 0, 10, 10]], expected = [1.0, 100]),
      dict(input = [[0, 0, 10, 10], [1, 1, 11, 11]], expected = [0.681, 81]),
      dict(input = [[0, 0, 10, 10], [0, 5, 10, 15]], expected = [0.333, 50]),
      dict(input = [[0, 0, 10, 10], [10, 0, 20, 10]], expected = [0.0, 0]),
    ]
    for case in cases:
      with self.subTest(case):
        input, expected = case.values()
        iou, interArea, aArea, bArea = utils.calcIoU(input[0], input[1])
        self.assertEqual([iou, interArea], expected)

if __name__ == '__main__':
  unittest.main()