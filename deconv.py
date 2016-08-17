# -*- coding: utf-8 -*-

import cv2
import numpy as np

#print array all
np.set_printoptions(threshold=np.inf)

#set PSF size
psfX = 5
psfY = 5
psfsize = psfX * psfY

#input image
inputname = "gaussianlena.png"
img = cv2.imread(inputname, 0)

#get image size
dy = len(img[0,:])
dx = len(img[:,0])

#make estimate image
es2 = np.zeros((dx,dy),np,float)
es = np.copy(img)


psf = np.ones((psfX,psfY),np.float32)/(psfsize)

print img.dtype
print psf

cv2.imshow("in",img)

num = 0
while num < 1:

	nimg = cv2.filter2D(es,-1,psf)
	cv2.imshow("aftfilter",nimg)

	for j in range(0,dy):
		for i in range(0,dx):
			if(nimg[i,j] >= 255):
				nimg[i,j] = 255
			elif(nimg[i,j] <= 0):
				nimg[i,j] = 0

	e = img.astype(np.float32) - nimg.astype(np.float32)

	print e
	
	m1 = np.zeros((psfX,psfY),np.float)

	for l in range(0,5):
		for k in range(0,5):
			a = 0.0
			for j in range(5,dy - 5):
				for i in range(5,dx - 5):
					if e[i,j] > 0:
						m1[k,l] += es[i+k-2,j+l-2] * e[i,j]
			m1[k,l] *= psf[k,l]


	for j in range(5,dy - 5):
		for i in range(5,dx - 5):
			a = 0.0
			for l in range(0,5):
				for k in range(0,5):
					a += e[i-k+2,j-l+2] * psf[k,l]
			es2[i,j] = es[i,j] + a

	esmax = 0
	esmin = 9999999999
	for j in range(3,dy - 3):
		for i in range(3,dx - 3):
			es[i,j] = es2[j,j]
			if(es2[i,j] > esmax):
				esmax = es2[i,j]
			if(es2[i,j] < esmin):
				esmin = es2[i,j]
	for j in range(3,dy - 3):
		for i in range(3,dx - 3):
			es2[i,j] = (es2[i,j]/(esmax-esmin)) * 255 
			if(es2[i,j] > 255):
				es2[i,j] = 255

	es2 = es2.astype(np.uint8)
	es = es2

	psf = m1/np.sum(m1)
	print psf
	cv2.imshow("out",es)
	num += 1

cv2.waitKey(0)



