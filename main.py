import cv2
import glob
import functions as func
import numpy as np 



user_directory = func.pull_file()


#convert to grayscale?
for input in glob.glob(user_directory):
        img = cv2.imread(input, cv2.IMREAD_UNCHANGED)
        print(f'dtype: {img.dtype}, shape: {img.shape}, min: {np.min(img)}, max: {np.max(img)}')
        break


#shows an image
# cv2.imshow('test',img)
# cv2.waitKey()
# cv2.destroyAllWindows()
