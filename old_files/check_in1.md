## Addressing Prior Feedback
Ensure to update the readme as the project progresses. 
I currently need to update the readme with current progression. It is a bit out of date. 

## Project Progress

The initial steps of this analysis involves writing an edge detection script utilizing Canny Edge Detection. (https://en.wikipedia.org/wiki/Canny_edge_detector)

This method has 5 main steps:
#### Apply an Gaussian Filter to smooth the image
This process is done through a "kernel" which effectively smoothes the signal using a Gaussian function. The kernal must be odd, so 3,5,9 etc.  This was manually implemented in `gaussian_filter.py`. This method is computationally draining. Normal method depends on polynomial multiplication for a total of O(n^2) calculations which was extremely slow(5-10 seconds for the test image). However, upon implementation of the fast fourier transform function from the numpy library, this calculation is below 0.5 seconds for the test image. 
#### Intensity Gradients, Thresholding, Double Threshold
This part involves some vector calculus due to the calculation of the gradients of the intensities. It was completeted pretty quickly as the definition of  the gradient is straightforward, this was done in the grad_mag function in `edge_detection.py`.  Thresholding and Double threshold is simply finding intensity values above or below your designated thresholds and reassinging the values. As we are working with numpy arrays, this was done en mass with the > or < operators. We have learned that this is where a large majority of optimization must be done. 
#### Edge Detection
This was one of the more harder sections to complete and computationally expensive. This is the second half of the thresholding section as we now must the gradients during thresholding to identify edges. Its a bit hard to explain, but the wikipedia section on the above linked page explains it well. This was implemented in `edge_detection.py` under the function interpolate_magnitudes. 

## Current Steps

The manual implementation is too computationally intensive across the board. Each of the manual implementations in pythons add up, to where a 2304x2304 test image takes 4-5 minutes.  While this isn't the same as our 256x256 images we will implement this on, the time it takes to run through that stack will take too long.  With this, we dediced to do a library implementation using OpenCV(https://opencv.org/). The benefit of this is that opencv is written in C++ and interfaced with python, resulting in significantly increased speeds. For instanstance, the manual canny implementation takes around 4-5 minutes for the 2304x2304 test image, while OpenCvs canny function takes 1-2 seconds. 

#### Hough Transform
The Hough transform is a shape recognition algorithm that we will use to identify blobs within our dataset. This can be implemented with OpenCV

#### Blob Measurement
Once blobs have been measured, we will be able to take the area of the closed blob and measure it using pixel width.  We can then track the blob area over time and measure the intensity within on the original image. This will be our final quantification of the image and we can work on other aspects yet to be explored. 

## Current Challenges.

### Optimization.
Optimizing the OpenCV canny operation is currently the biggest struggle.  Our images contain a large amount of noise which influences the edge detection process. Its possible we will migrate away from Canny however we need to have that discussion and look for other options within OpenCV. 

## Project Organization
Manual implementation files have been archived in the manual_implementation folder.  Currently the active file will be library_approach.py. Subsequent quantification file will be added later. 

## Questions

None at this moment. Suggestions as an alternative to Canny would be welcomed.
