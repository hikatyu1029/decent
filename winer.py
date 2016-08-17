# -*- coding: utf-8 -*-

import cv2
import numpy as np


a = np.ones((10,10),np.float32)/100

A = np.zeros((1200,1200)) 

A[0:10,0:10] = a[0:10,0:10]
fa = np.fft.fft2(A)

image = cv2.imread("momo.jpg", 0)
cv2.imshow("in",image)
fimg =  np.fft.fft2(image)

fa = np.conj(fa) / (np.abs(fa) ** 2 + 0.05)

num = 0
while num < 4:
	fimg = fimg * fa
	num += 1
outimg = fimg

fout = np.fft.ifft2(outimg)
out = fout.real
out = np.clip(out,0,255)
out = out.astype(np.uint8)
cv2.imshow("outaft",out)
cv2.imwrite("winer2.png",out)

cv2.waitKey(0)
