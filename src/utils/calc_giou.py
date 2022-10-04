from .calc_iou import calc_iou

def calc_giou(a_rect, b_rect):
  """Calculate GIoU for two rectangles.
  Args:
      a_rect (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
      b_rect (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
      tuple: Returns GIoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  a_xmin, a_ymin, a_xmax, a_ymax = a_rect

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  b_xmin, b_ymin, b_xmax, b_ymax = b_rect

  # Calculate IoU.
  iou, inter_area, a_area, b_area = calc_iou(a_rect, b_rect)

  # Calculate the area of convex shape C.
  inter_xmin = min(a_xmin, b_xmin)
  inter_ymin = min(a_ymin, b_ymin)
  inter_xmax = max(a_xmax, b_xmax)
  inter_ymax = max(a_ymax, b_ymax)
  c_area = (inter_xmax - inter_xmin) * (inter_ymax - inter_ymin)

  # Area obtained by subtracting the overlapping partial area (Intersect) from the total area of rectangles a and b.
  union_area = inter_area / iou

  # Calculate GIoU.
  giou = iou - (c_area - union_area) / c_area
  return round(giou, 3), inter_area, a_area, b_area