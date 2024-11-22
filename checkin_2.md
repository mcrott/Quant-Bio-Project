
## Check In 2
I wanted to keep the previous check-in information within so I can address changes to the project structure. Changes from check-in 1 will be in blockquotes. 


## Previous Checkin

##### Addressing Prior Feedback
```Ensure to update the readme as the project progresses. 
I currently need to update the readme with current progression. It is a bit out of date. 
```

Readme was updated. 
### Project Progress

```
The initial steps of this analysis involves writing an edge detection script utilizing Canny Edge Detection. (https://en.wikipedia.org/wiki/Canny_edge_detector)

This method has 5 main steps:
#### Apply an Gaussian Filter to smooth the image
This process is done through a "kernel" which effectively smoothes the signal using a Gaussian function. The kernal must be odd, so 3,5,9 etc.  This was manually implemented in `gaussian_filter.py`. This method is computationally draining. Normal method depends on polynomial multiplication for a total of O(n^2) calculations which was extremely slow(5-10 seconds for the test image). However, upon implementation of the fast fourier transform function from the numpy library, this calculation is below 0.5 seconds for the test image. 
#### Intensity Gradients, Thresholding, Double Threshold
This part involves some vector calculus due to the calculation of the gradients of the intensities. It was completeted pretty quickly as the definition of  the gradient is straightforward, this was done in the grad_mag function in `edge_detection.py`.  Thresholding and Double threshold is simply finding intensity values above or below your designated thresholds and reassinging the values. As we are working with numpy arrays, this was done en mass with the > or < operators. We have learned that this is where a large majority of optimization must be done. 
#### Edge Detection
This was one of the more harder sections to complete and computationally expensive. This is the second half of the thresholding section as we now must the gradients during thresholding to identify edges. Its a bit hard to explain, but the wikipedia section on the above linked page explains it well. This was implemented in `edge_detection.py` under the function interpolate_magnitudes. 
```

Yeah. Bad news right off the bat.  Canny Edge detection wasn't efficient enough to identify shapes. Our canny output was consistently curved lines with no closure to them, so we were unable to calculate area at or observe any growth.  This was likely as there was not a uniform intensity across the puncta. With this, we needed to implement a new method.

Luckily not all of the code that was written will be tossed/unused. I might need to apply the thresholding function and ive already found a use for gaussian kernal generation. 



## Shape Detection with findContours OpenCV
With the issues of Canny identified, we moved onto a findContours function with the openCV library. This works really well with puncta identification and was easy enough to implement with proper thresholding. The function also outputs each shape as an array, allowing for easy drawing as well as area calculations.

I will try to implement a manual implementation of this function once we get caught up. 

## Current Steps

```
The manual implementation is too computationally intensive across the board. Each of the manual implementations in pythons add up, to where a 2304x2304 test image takes 4-5 minutes.  While this isn't the same as our 256x256 images we will implement this on, the time it takes to run through that stack will take too long.  With this, we dediced to do a library implementation using OpenCV(https://opencv.org/). The benefit of this is that opencv is written in C++ and interfaced with python, resulting in significantly increased speeds. For instanstance, the manual canny implementation takes around 4-5 minutes for the 2304x2304 test image, while OpenCvs canny function takes 1-2 seconds. 
```

Unfortunately the canny implementation was canned. 

#### Hough Transform
```
The Hough transform is a shape recognition algorithm that we will use to identify blobs within our dataset. This can be implemented with OpenCV
```

Using an alternative method for shape detection. 
#### Working on the entire tif stack
Currently, we are able to cycle through an entire tif stack. 
#### Blob Measurement
```
Once blobs have been measured, we will be able to take the area of the closed blob and measure it using pixel width.  We can then track the blob area over time and measure the intensity within on the original image. This will be our final quantification of the image and we can work on other aspects yet to be explored. 
```

Area of the closed blob is already calculated with findContours. We will need to work on calculating intensity values within the blob but as we know the boundaries of the blob, that should be trival. 



#### Normalization
Self explanatory and addressed in ```readme.md``` for the project. 



## Current Challenges.

### Optimization.
```
Optimizing the OpenCV canny operation is currently the biggest struggle.  Our images contain a large amount of noise which influences the edge detection process. Its possible we will migrate away from Canny however we need to have that discussion and look for other options within OpenCV. 
```
Funny enough. This is the same issue for the findContours.  I was able to reduce the noise through filter2D function and the previous implementation of a gaussian kernel generation. This was able to reduce the noise. 

### Normalization

Normalization will be the hardest part moving forward. This will be the key step after implementing the analysis across the tif stack. This is needed because the fluorescence at timepoint 1/178 may be different than timepoint 100/178 or 160/178, which can effect our analysis and blob detection.  Its unknown whether it will but we need to think of methods to address this prior to finding out we have to address it to avoid scrambling at the last moment. 

## Project Organization
```
Manual implementation files have been archived in the manual_implementation folder.  Currently the active file will be library_approach.py. Subsequent quantification file will be added later. 
```

We reorganized it again to where the ```old_files``` folder contains all the old manual implementation files as well as others. We are currently using jupyter notebooks for testing with the full implementation in ```library_approach.py``` as well as ```current_working.ipynb```. 

## Questions

Do you know of any good normalization methods for the full stack? The only idea I has was
```
max = np.max(stack)
min = np.min(stack)

normalization = {stack-min}/{max-min}

```