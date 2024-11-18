"""
    
    Library approach uses OpenCV as the primary method to analyze data

"""


import cv2 as cv
import numpy as np
import scipy as sp
import functions as func
from PIL import Image
from gaussian_filter import convolution

import matplotlib.pyplot as plt

import tracemalloc

# Your code herec

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3
#test image == 11
input = r"/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_test.tif" 
img = cv.imread(input, cv.IMREAD_GRAYSCALE)



img = cv.imread(input, cv.IMREAD_GRAYSCALE)
clahe = cv.createCLAHE(clipLimit=40)
image = clahe.apply(img)
input_image = cv.Canny(img, 25,40,apertureSize=3, L2gradient=True)

outpt = Image.fromarray(np.array(input_image,dtype=np.uint8))
outpt.save('outpt5.tif')

# cv.imshow('test',input_image)
# cv.waitKey()
# cv.destroyAlldWindows()
