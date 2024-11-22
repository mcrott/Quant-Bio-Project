## Updated Read-Me 20NOV2024

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


Current Steps

1)  Shape Recognition
    - 

    ### Goal
    Shape recognition by OpenCV2 library with findContours.
    ##### Progress      **[COMPLETED 19NOV2024]**
    This has been successfully implemented on a single frame. Look at cells 1-5 in ```current_working.ipynb```. 
    ##### Future Work
    None needed for this step.


2) Area Determination
    - 
    ### Goal
    Determine the area of individual blobs identified in step 1. 
    ##### Progress **[COMPLETED 20NOV2024]**
    This is successfully outputed by findContours.
    ##### Future Work       
    Quantification of each blob. This can be done with area and fluorescent intensity. 
3) Stack Implementation
    - 
    ### Goal
    The goal is to implement steps 1 and 2 into a full tiff stack. 
    ##### Progress [Completed 21NOV2024]
    Able to successfully upload a tiff stack and iterate through each timepoint and analyze with opencv. 
4) Normalization
    - 
    Must normalize the images to be relatively the same as each other. 
    ##### Considerations
    Will have to first implement the analysis and attempt to introduce some sort of normalization to each image for pixel intensity. 
    1) What would normalization look like?  Take the histogram of intensity values and threshold/normalize it?
    2) What threshold values will we use? Threshold on 1/178 could severely impact thresholding at 100/178 or 160/178 for example.  
    3) Is there an algorithm that can be used to determine best normalization?
5) Blob Tracking
    - 
    ## Tracking
    This will be done by observing the center of mass for each blob(area) and tracking it. Will compare n-1, n, n+1 with a certain error of 3x3 or 5x5 around the center of mass.  Pathfinding algorithm may be implemented as well. 
    #### Progress [Updated 21NOV2024]
    Actively working on this step
6) Quantification
    - 
    Figuring out exactly what we want to calculate still. 
    1) Rate of change of the area of individual blobs
    2) velocity, acceleration of the blobs?(diffusion)
    3) recruitment rate? thats related to 2)
    4) calculate the number of fluorophores in each blob?

    #### Progress [Updated 21NOV2024]
    Havent started, still brainstorming. I have previous code that calculates the MSD + Diffusion rate. 