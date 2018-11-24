import cv2
import numpy as np
blur=((1,1),1)
erode_=(2,2)
dilate_=(1, 1)
cv2.imwrite('black2.png',cv2.dilate(cv2.erode(cv2.GaussianBlur(cv2.imread('image3.png',0)/255, blur[0], blur[1]), np.ones(erode_)), np.ones(dilate_))*255) 