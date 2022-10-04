def calc_iou(a_rect, b_rect):
  """Calculate IoU for two rectangles.
  Args:
      a_rect (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
      b_rect (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
      tuple: Returns IoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  a_xmin, a_ymin, a_xmax, a_ymax = a_rect

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  b_xmin, b_ymin, b_xmax, b_ymax = b_rect

  # Calculate the area of rectangle A.
  a_area = (a_xmax - a_xmin) * (a_ymax - a_ymin)
  # a_area = (a_xmax - a_xmin + 1) * (a_ymax - a_ymin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of rectangle B.
  b_area = (b_xmax - b_xmin) * (b_ymax - b_ymin)
  # b_area = (b_xmax - b_xmin + 1) * (b_ymax - b_ymin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of intersection.
  inter_xmin = max(a_xmin, b_xmin)
  inter_ymin = max(a_ymin, b_ymin)
  inter_xmax = min(a_xmax, b_xmax)
  inter_ymax = min(a_ymax, b_ymax)
  inter_width = max(0, inter_xmax - inter_xmin)
  # inter_width = max(0, inter_xmax - inter_xmin + 1)# The reason for adding 1 is to avoid division by zero.
  inter_height = max(0, inter_ymax - inter_ymin)
  # inter_height = max(0, inter_ymax - inter_ymin + 1)# The reason for adding 1 is to avoid division by zero.
  inter_area = inter_width * inter_height

  # Calculate the area of union.
  union_area = a_area + b_area - inter_area

  # Calculate IoU.
  iou = inter_area / union_area
  return round(iou, 3), inter_area, a_area, b_area