## Read-me

JHU CMDB Quantitative Biology Lab Project

Matt Crotteau
Ethan Yarberry
### Conda
**Check the requirements.yml for dependencies!**


```
conda create --name quant-bio-lab --file requirements.yml
conda activate quant-bio-lab
```

### Test Image Folder
```https://livejohnshopkins-my.sharepoint.com/:f:/g/personal/mcrotte1_jh_edu/Ei0Mryn3KxZCmKF506wvtxgB0_U25NWlUqveuG0z0LCFJQ?e=hld6Cv```
 
This is the folder for test input images. 

Check the conda-require.txt file for dependencies~
### Goal
The goal of our lab project is to generate a script that can effectively analyze a folder of time lapse fluorescent images. We will glob a folder of pre-screened time lapse images and subsequently extract the intensity data by pixel. With this data, we hope to quantify the rate of change as well as potential density of labeled probes as they are recruited. Output will include a single image which demonstrates where in the FOV change has occurred with a hopeful goal of selecting an area to quantify the rate within that ROI. 

Current steps
1) ~~Find a dataset(Ethan)~~
    - completed, condensate dataset
2) Figure out how to read .nd2 files(Ethan) and tif(Matt)
    - The .nd2 file prevents any heavy preprocessing just in case we want to explore this route
    ~~- .tiffs are the main file format being read(Cv2 library in Python)~~
        - Completed. CV2 library
## Canny Edge Detection
We are going to try and implement the canny edge detector. 
https://en.wikipedia.org/wiki/Canny_edge_detector


3) Image Segmentation of Condensate Movie

    - ~~Create Gaussian Filter for edge detection/blob detection~~
        - Completed with both manual convolution(slow) and fft(Matt)
            - Manual convolution(for loops) = 3 seconds for cropped image
            - Scipy.convolve = 1.18 seconds
            - fft w/ numpy = 0.01 seconds

    - Identify Edges/Blob
    - Implement strategy to observe growth and other analysis
        - Changes in edge area over time?
    - Sidequest: Implement Tracking algorithm to observe recruitment rate in the movie
        - Calculate Diffusion rates using previous code(Matt)
            - No need to code anything, we just need tracking data
        - Tracking algorithm(ethan)

## Ignore
Side Quest-  Image Segmentation analysis of individual microsporidia spores(Matt)
    - Goal is to learn segmentation techniques and perhaps take a slight detour to track polar tube firing in raw .nd2 files. (Example File in test_folder)
