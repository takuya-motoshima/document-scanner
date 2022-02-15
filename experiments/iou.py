def calcIou(a, b):
  aXmin, aYmin, aXmax, aYmax = a[0], a[1], a[2], a[3]
  bXmin, bYmin, bMax, bYmx = b[0], b[1], b[2], b[3]
  aArea = (aXmax - aXmin + 1) * (aYmax - aYmin + 1)
  bArea = (bMax - bXmin + 1) * (bYmx - bYmin + 1)
  interXmin = max(aXmin, bXmin)
  interYmin = max(aYmin, bYmin)
  interXmax = min(aXmax, bMax)
  interYmax = min(aYmax, bYmx)
  intersectWd = max(0, interXmax - interXmin + 1)
  intersectHt = max(0, interYmax - interYmin + 1)
  intersectArea = intersectWd * intersectHt
  iou = intersectArea / (aArea + bArea - intersectArea)
  return iou
iou = calcIou((27, 47, 130, 90), (30, 68, 150, 110))
print(f'iou={iou}')