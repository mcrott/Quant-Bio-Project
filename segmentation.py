import cv2 as cv
import numpy as np
import scipy as sp
import functions as func


import tracemalloc

tracemalloc.start()

# Your code here

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3

input = "/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_image.tif"
img = cv.imread(input, cv.IMREAD_UNCHANGED)
clahe = cv.createCLAHE(clipLimit=100)
final_img = clahe.apply(img) +50

image1 = func.Image(final_img)
"""
clahe = cv2.createCLAHE(clipLimit=5)
final_img = clahe.apply(image_bw) + 30
"""

for i in range(0,2304,16):
    print(i*2)

#shows an images
"""
    First step. 
    Auto correct contrast using homebrewed CLAHE function
        1) ensure the same correction is applied to every image!!!!

        !!!COMPLETED!!!
            used CV2s module. Same clip limit will occur for each. 
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
            - Tile with a square 
                - 2304 pixels, 100x100 at 25 pixel gaps
                    - IE, 0-100x0-100, then 25-125x25-125, etc 

                    !!!COMPLETED TILING!!!


        Apply image segmentation to these individual tiles
        filter out overlapped identified objects
        compile
        output graph 


    Method 2)
        Apply image segmentation to entire image
        output graph
"""



# cv.imshow('test',final_img)
# cv.waitKey()
# cv.destroyAlldWindows()



snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:10]:
    print(stat)
