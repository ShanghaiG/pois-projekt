import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('zdj6-edit.png',0)
img = cv.medianBlur(img,5)

th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
th1 = th3
titles = ['Original Image',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

images = [img, th2, th3]
rows = img.shape[0]



for i in range(3):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.gcf().set_size_inches(30, 30)
    plt.xticks([]),plt.yticks([])
plt.show()