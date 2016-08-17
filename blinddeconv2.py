# -*- coding: utf-8 -*-

import cv2
import numpy as np

image = cv2.imread("out.png",0)

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
psf = np.ones((V,H),np.float32)/(V * H)
es = np.copy(img)
rat = np.zeros((dx,dy),np.float)

num = 0
while num < 1:

	#make error
	nimg = cv2.filter2D(es,-1,psf)

	print nimg

	for j in range(0,dy):
		for i in range(0,dx):
			if(nimg[i,j] > 1.0):
				rat[i,j] = img[i,j]
			elif(nimg[i,j] < 0.001):
				rat[i,j] = img[i,j] / 0.001
			else:
				rat[i,j] = img[i,j] / nimg[i,j]
	print rat

	#make estimate image and psf
	#lucy

	m1 = np.ones((V,H),np.float32)/(V * H)


	for j in range(0,dy):
		for i in range(0,dx):
			a = 0
			e = es[i,j]
			for l in range(-U,U-1):
				for k in range(-M,M-1):
					if (j + l >= U & j + l < dy - U & i + k >= M & i + k <dx - M):
						a += rat[i+k,j+l] * psf[k+M,l+U]
						m1[k+M,l+U] += e*(rat[i+k,j+l]-1)*psf[k+M,l+U]
			es[i,j] *= a 
	num += 1

cv2.waitKey(0)