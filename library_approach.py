"""
    
    Library approach uses OpenCV as the primary method to analyze data

"""


import cv2 as cv
import numpy as np
import scipy as sp
import functions as func
from PIL import Image

import matplotlib.pyplot as plt

import tracemalloc

tracemalloc.start()

# Your code herec

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3

input = r"/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_image.tif" 
img = cv.imread(input, cv.IMREAD_GRAYSCALE)
clahe = cv.createCLAHE(clipLimit=20)
image = clahe.apply(img) +50 
input_image = cv.Canny(image, 100,250)

outpt = Image.fromarray(np.array(input_image,dtype=np.uint8))
outpt.save('outpt5.tif')