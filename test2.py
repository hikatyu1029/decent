# -*- coding: utf-8 -*-

import cv2
import numpy as np

image = cv2.imread("lena.png", 0)

print len(image[:,0])

cv2.waitKey(0)