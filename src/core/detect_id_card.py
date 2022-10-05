import os
import sys
import cv2
import numpy as np
from dotmap import DotMap
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import utils

def detect_id_card(img, debug_img_callback = None):
  """Detect document from image.
  Args:
      img (str): Image path or DataURL.
      debug_img_callback (function, optional): Callback function for image transformation. Defaults to None.
  Returns:
      string: DataURL of the detected document image.
  Raises:
      ValueError: Parameters are incorrect.
  """
  _validate_params(img)
  if not debug_img_callback:
    debug_img_callback = lambda label, img: None
  mime_type = utils.get_mime_type(img)
  img = utils.load_img(img)
  resize_img, ratio = _resize(img)

  # add a margin inside the image so that the target document is not adjacent to the image frame.
  margin = 5
  margin_img = _margins(resize_img, margin)
  orig_coordinates = _get_coordinates_without_margins(margin_img, margin)
  debug_img_callback('margin_img', cv2.rectangle(margin_img.copy(), (orig_coordinates[0].x, orig_coordinates[0].y), (orig_coordinates[2].x, orig_coordinates[2].y), (0,255,0), 2))
  edge_img = _detect_edges(margin_img, debug_img_callback)
  id_card_contour = _detect_id_card_contour(edge_img, margin, orig_coordinates)
  if id_card_contour is None:
    return None
  debug_img_callback('contour', cv2.drawContours(resize_img.copy(), [id_card_contour], -1, (0,255,0), 2))
  warped_img = _perspective_correction(img, id_card_contour, ratio);
  debug_img_callback('warped_img', warped_img)
  warped_img = _resize_to_id_card_ratio(warped_img)
  return utils.to_data_url(warped_img, mime_type)

def _validate_params(img):
  if (not utils.is_data_url(img) and not os.path.exists(img) and not os.path.isfile(img)):
    raise ValueError('Input is incorrect. Input can be an image path, or DataURL')

def _resize(img):
  min_height = 600
  if img.shape[0] < min_height:
    img, ratio = utils.resize_img(img, height = min_height)
  else:
    img = img.copy()
    ratio = 1
  return img, ratio

def _margins(img, margin):
  return cv2.copyMakeBorder(img.copy(), margin, margin, margin, margin, cv2.BORDER_CONSTANT, value=(0,0,0))

def _get_coordinates_without_margins(img, margin):
  height, width = img.shape[:2]
  return [
    DotMap(x = margin, y = margin),
    DotMap(x = width - margin, y = margin),
    DotMap(x = width - margin, y = height - margin),
    DotMap(x = margin, y = height - margin)
  ]

def _detect_edges(img, debug_img_callback):
  # grayscaling.
  gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  debug_img_callback('gray_img', gray_img)

  # remove noise.
  median_img = cv2.medianBlur(gray_img, ksize=5)
  debug_img_callback('median_img', median_img)

  # shrink the white areas and expand the black areas.
  erode_img = cv2.erode(median_img, kernel=np.ones((5,5), np.uint8), iterations=1)
  debug_img_callback('erode_img', img)

  # binarize.
  thresh_img = cv2.adaptiveThreshold(erode_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
  debug_img_callback('thresh_img', thresh_img)

  # detect edges.
  edge_img = cv2.Canny(thresh_img, 30, 400)
  debug_img_callback('edge_img', edge_img)
  return edge_img

def _detect_id_card_contour(img, margin, orig_coordinates):
  contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  if not contours:
    return None
  contours = sorted(contours, key=cv2.contourArea, reverse=True)
  for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon=0.02 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.1 * peri, closed=True)
    # approx = cv2.approxPolyDP(contour, epsilon=0.005 * peri, closed=True)
    if not len(approx) == 4:
      continue
    # skip if the rectangle is adjacent to a margin created in the image.
    if margin > 0:
      rect = utils.contour_to_rect(approx)
      correction = 5
      if (not(
        rect[0].x >= orig_coordinates[0].x - correction and
        rect[0].y >= orig_coordinates[0].y - correction and
        rect[1].x <= orig_coordinates[1].x - correction and
        rect[1].y >= orig_coordinates[1].y - correction and
        rect[2].x <= orig_coordinates[2].x - correction and
        rect[2].y <= orig_coordinates[2].y - correction and
        rect[3].x >= orig_coordinates[3].x - correction and
        rect[3].y <= orig_coordinates[3].y - correction
      )):
        continue
      # subtract the length of the margin from the found contour coordinates.
      approx = np.array(approx) - margin
    return approx
  return None

def _perspective_correction(img, id_card_contour, ratio):
  # apply the four point tranform to obtain a "birds eye view" of the image.
  warped_img = utils.four_point_transform(id_card_contour / ratio, img)
  warped_img, _ = utils.resize_img(warped_img, height = 800)
  return warped_img

def _resize_to_id_card_ratio(img):
  width, height = img.shape[:2]
  width_ratio, height_ratio = [8.56, 5.4]
  new_width = width
  new_height = height
  if (height / width) < (height_ratio / width_ratio):
    new_height = round(width * (height_ratio / width_ratio))
  else:
    new_width = round(height / (height_ratio / width_ratio))
  return cv2.resize(img, (new_width, new_height), cv2.INTER_AREA)