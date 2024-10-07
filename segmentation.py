import cv2 as cv
import numpy as np
import scipy as sp
import functions as func
from PIL import Image

from gaussian_filter import convolution
from gaussian_filter import find_edges

import tracemalloc

tracemalloc.start()

# Your code herec

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3

input = r"C:\Users\test\School\Quant Bio\Quant-Bio-Project\segmentation_image.tif"
img = cv.imread(input, cv.IMREAD_UNCHANGED)
clahe = cv.createCLAHE(clipLimit=20)
image = clahe.apply(img) +50
image1 = func.Image(image)

test_vert, test_horz = find_edges(image)

test_vert = Image.fromarray(np.array(test_vert,dtype=np.uint16))
test_vert.save('vert.tif')
test_horz = Image.fromarray(np.array(test_horz,dtype=np.uint16))
test_horz.save('horz.tif')


#smoothing
test_image= convolution(image,10,3)
test_image = np.array(test_image,dtype=np.uint16)
test_image = Image.fromarray(test_image)
test_image.save('output1.tif')




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



# cv.imshow('test',image)
# cv.waitKey()
# cv.destroyAlldWindows()



# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')

# for stat in top_stats[:10]:
#     print(stat)
1