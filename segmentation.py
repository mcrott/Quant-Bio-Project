import cv2 as cv
import numpy as np
import scipy as sp


input = "/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_image.tif"

img = cv.imread(input, cv.IMREAD_UNCHANGED)

corrected_img = cv.createCLAHE()

#shows an image
"""
    First step. 
    Auto correct contrast using homebrewed CLAHE function
        1) ensure the same correction is applied to every image!!!!
"""

"""
    First and half step

    Identify how to map memorize usage during script. 
"""
"""
    Second step.
    Compare two methods for speed, memory usage
    Method 1)
        figure out how to tile through your image
        Apply image segmentation to these individual tiles
        filter out overlapped identified objects
        compile
        output graph 
    Method 2)
        Apply image segmentation to entire image
        output graph
"""



cv.imshow('test',img)
cv.waitKey()
cv.destroyAlldWindows()