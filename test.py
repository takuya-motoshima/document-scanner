import cv2
import matplotlib.pyplot as plt

img = cv2.imread('img/license.png')
plt.imshow(img)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()