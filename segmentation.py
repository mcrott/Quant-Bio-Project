import cv2 as cv
import numpy as np
import scipy as sp
import functions as func
from PIL import Image

from gaussian_filter import convolution
from edge_detection import find_edges_fft
from edge_detection import grad_mag

import tracemalloc

tracemalloc.start()

# Your code herec

#USE EXPLICIT VARIABLE DECLARATION
#x: int = 3

input = r"/Users/cmdb/Quant_Bio_Project/Quant-Bio-Project/segmentation_image.tif"
img = cv.imread(input, cv.IMREAD_UNCHANGED)
clahe = cv.createCLAHE(clipLimit=20)
image = clahe.apply(img) +50
image1 = func.Image(image)
image = convolution(image,10,2)
vert, horz = find_edges_fft(image,sobel_scaling=4)

test_vert = Image.fromarray(np.array(vert,dtype=np.uint16))
test_vert.save('vert.tif')
test_horz = Image.fromarray(np.array(horz,dtype=np.uint16))
test_horz.save('horz.tif')
#
horz_vert_sobel = grad_mag(horz,vert)
#gradient directions
print(horz_vert_sobel)
horz_vert = Image.fromarray(np.array(horz_vert_sobel,dtype=np.uint16))
horz_vert.save('horz-vert.tif')

#smoothing
image = np.array(image, dtype=np.uint16)
test_image = Image.fromarray(image)
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