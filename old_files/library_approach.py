"""
    
    Library approach uses OpenCV as the primary method to analyze data

"""


import cv2 as cv
import numpy as np
import scipy as sp
import functions as func
from PIL import Image
from old_files.gaussian_filter import gaussian_kernal


import matplotlib.pyplot as plt

import tracemalloc

# Your code herec

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3
#test image == 11

kernel = gaussian_kernal(3,np.sqrt(3))
#Thresholding for 
low_thresh: int = 13
high_thresh: int = 50

input = r"/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_test.tif" 
img = cv.imread(input, cv.IMREAD_GRAYSCALE)
image = cv.filter2D(img,-1,kernel)
ret,thresh = cv.threshold(image,low_thresh,high_thresh,cv.THRESH_BINARY)
contours,hierarchy = cv.findContours(thresh, 1, 2)
test = cv.drawContours(image, contours, -5, (0, 255, 0), 1) 
plt.imshow(test)
plt.show()