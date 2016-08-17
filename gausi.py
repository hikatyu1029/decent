# -*- coding: utf-8 -*-

import cv2
import numpy as np

image = cv2.imread("lena.png",0)

blur = cv2.GaussianBlur(image,(5,5),0)

cv2.imwrite('gaussianlena.png',blur)