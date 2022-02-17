def calcIoU(rectA, rectB):
  """Calculate IoU for two rectangles.
  Args:
    rectA: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
    rectB: Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
    Returns IoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  aXmin, aYmin, aXmax, aYmax = rectA

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  bXmin, bYmin, bXmax, bYmax = rectB

  # Calculate the area of rectangle A.
  aArea = (aXmax - aXmin) * (aYmax - aYmin)
  # aArea = (aXmax - aXmin + 1) * (aYmax - aYmin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of rectangle B.
  bArea = (bXmax - bXmin) * (bYmax - bYmin)
  # bArea = (bXmax - bXmin + 1) * (bYmax - bYmin + 1)# The reason for adding 1 is to avoid division by zero.

  # Calculate the area of intersection.
  interXmin = max(aXmin, bXmin)
  interYmin = max(aYmin, bYmin)
  interXmax = min(aXmax, bXmax)
  interYmax = min(aYmax, bYmax)
  interWidth = max(0, interXmax - interXmin)
  # interWidth = max(0, interXmax - interXmin + 1)# The reason for adding 1 is to avoid division by zero.
  interHeight = max(0, interYmax - interYmin)
  # interHeight = max(0, interYmax - interYmin + 1)# The reason for adding 1 is to avoid division by zero.
  interArea = interWidth * interHeight

  # Calculate the area of union.
  unionArea = aArea + bArea - interArea

  # Calculate IoU.
  iou = interArea / unionArea
  return round(iou, 3), interArea, aArea, bArea