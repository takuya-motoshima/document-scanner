from .calcIoU import calcIoU

def calcGIoU(rectA, rectB):
  """Calculate GIoU for two rectangles.
  Args:
      rectA (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
      rectB (list): Rectangular bounding box ([top left X, top left Y, bottom right X, bottom right Y]).
  Returns:
      tuple: Returns GIoU, intersection area, rectangle A area, and rectangle B area.
  """
  # Top left X, top left Y, bottom right X, bottom right Y of rectangle A.
  aXmin, aYmin, aXmax, aYmax = rectA

  # Top left X, top left Y, bottom right X, bottom right Y of rectangle B.
  bXmin, bYmin, bXmax, bYmax = rectB

  # Calculate IoU.
  iou, interArea, aArea, bArea = calcIoU(rectA, rectB)

  # Calculate the area of convex shape C.
  interXmin = min(aXmin, bXmin)
  interYmin = min(aYmin, bYmin)
  interXmax = max(aXmax, bXmax)
  interYmax = max(aYmax, bYmax)
  cArea = (interXmax - interXmin) * (interYmax - interYmin)

  # Area obtained by subtracting the overlapping partial area (Intersect) from the total area of rectangles a and b.
  unionArea = interArea / iou

  # Calculate GIoU.
  giou = iou - (cArea - unionArea) / cArea
  return round(giou, 3), interArea, aArea, bArea