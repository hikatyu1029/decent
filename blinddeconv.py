# -*- coding: utf-8 -*-

import cv2
import numpy as np

#imput image
image = cv2.imread("out.png",0)
cv2.imshow("in",image)

#image size
dy = len(image[0,:])
dx = len(image[:,0])

#PSF size
H = 12
V = 8

#define VSEP
M = 2/H
U = 2/V

#process image cuffer size
PX = dx + H + 1
PY = dy + V + 1

img = np.copy(image)

psf = np.ones((V,H),np.double)/(V * H)
es = np.ones((dx,dy),np.double) * 0.5
rat = np.zeros((dx,dy),np.double)
err = np.zeros((dx,dy),np.double)

num = 0
while num < 1:

	#make error
	nimg = cv2.filter2D(es,-1,psf)

	for j in range(0,dy):
		for i in range(0,dx):

			if(nimg[i,j] > 1.0):
				rat[i,j] = img[i,j]
			elif(nimg[i,j] < 0.001):
				rat[i,j] = img[i,j] / 0.001
			else:
				rat[i,j] = img[i,j] / nimg[i,j]

	#make estimate image
	es_pas = cv2.filter2D(rat,-1,psf)
	es2 = es_pas * es
	
	for j in range(5,dy - 5):
		for i in range(5,dx - 5):
	es2 = (es2 / (es2.max() - es2.min())) * 255
	es2_out = es2.astype(np.uint8)
	print es2_out.max()
	print es2_out.min()
	cv2.imshow("out",es2_out)
	es = es2

	num += 1

cv2.waitKey(0)