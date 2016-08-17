# -*- coding: utf-8 -*-

import cv2
import numpy as np

#print array all
np.set_printoptions(threshold=np.inf)

#セットする項目
#LOOP_VOUNT ループの回数
#psf_X PSFの横幅
#psf_Y PSFの縦幅
#inputname 入力画像のファイル名

#----------SET------------------------
#SET Loop count
LOOP_COUNT = 100

#SET PSF size
psf_X = 5
psf_Y = 5

#SET input image
inputname = "gaussianlena.png"
#----------SET------------------------

#PSF relat
PSFsize = psf_X * psf_Y
h_psf_X = psf_X/2
h_psf_Y = psf_Y/2

#input image
img_A = cv2.imread(inputname, 0)

#make border(make use img)
img = cv2.copyMakeBorder(img_A,h_psf_Y,h_psf_Y,h_psf_X,h_psf_X,cv2.BORDER_REPLICATE)

#get img size
img_y = len(img[0,:])
img_x = len(img[:,0])

#make PSF
psf = np.ones((psf_X,psf_Y),np.float32)/(PSFsize)

#make estimate image
#est = np.ones((img_x,img_y),np.float32) * 128 #use heitan gazo
est = np.copy(img) #use img
est2 = np.copy(img)


#------------main algorithm------------------
num = 0
while num < LOOP_COUNT:

	print "{0}回目開始".format(num + 1)

	#make see image
	imgfirst = img
	nimg = cv2.filter2D(est,-1,psf)

	for j in range(0,img_y):
		for i in range(0,img_x):
			if(nimg[i,j] >= 255):
				nimg[i,j] = 255
			elif(nimg[i,j] <= 0):
				nimg[i,j] = 0

	#make error
	e = imgfirst.astype(np.float32) - nimg.astype(np.float32)

	# PSF estimate
	m1 = np.zeros((psf_X,psf_Y),np.float)

	for l in range(0,psf_Y):
		for k in range(0,psf_X):
			a = 0.0
			for j in range(h_psf_Y + 1,img_y - h_psf_Y):
				for i in range(h_psf_X + 1,img_x - h_psf_X):
					if e[i,j] > 0:
						m1[k,l] += est[i + k - h_psf_X, j + l - h_psf_Y] * e[i,j]
			m1[k,l] *= psf[k,l]

	# image estimate
	for j in range(h_psf_Y + 1,img_y - h_psf_Y):
		for i in range(h_psf_X + 1,img_x - h_psf_X):
			a = 0.0
			for l in range(0,psf_Y):
				for k in range(0,psf_X):
					a += e[i - k + h_psf_X, j - l + h_psf_Y] * psf[k,l]
			est2[i,j] = est[i, j] + a

	est2 = est2.astype(np.uint8)
	est = est2

	# psf normalize
	psf = m1/np.sum(m1)
	print psf
	num += 1
#------------end algorithm-----------------
cv2.imshow("in",img)
cv2.imshow("out",est)
cv2.waitKey(0)