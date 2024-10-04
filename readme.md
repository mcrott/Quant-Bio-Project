## Read-me

JHU CMDB Quantitative Biology Lab Project

Matt Crotteau
Ethan Yarberry
### Conda
**Check the conda-requirements.txt for dependencies!**


```
conda create --name quant-bio-lab --file conda-requirements.txt
conda activate quant-bio-lab
```

### Test Image Folder
```https://livejohnshopkins-my.sharepoint.com/:f:/g/personal/mcrotte1_jh_edu/Ei0Mryn3KxZCmKF506wvtxgB0_U25NWlUqveuG0z0LCFJQ?e=hld6Cv```
 
This is the folder for test input images. 

Check the conda-require.txt file for dependencies~
### Goal
The goal of our lab project is to generate a script that can effectively analyze a folder of time lapse fluorescent images. We will glob a folder of pre-screened time lapse images and subsequently extract the intensity data by pixel. With this data, we hope to quantify the rate of change as well as potential density of labeled probes as they are recruited. Output will include a single image which demonstrates where in the FOV change has occurred with a hopeful goal of selecting an area to quantify the rate within that ROI. 

Current steps
1) Find a dataset(Ethan)
2) Figure out how to read .nd2 files(Ethan) and tiff(Matt)
    - The .nd2 file prevents any heavy preprocessing just in case we want to explore this route
    - .tiffs are the main file format being read(Cv2 library in python)?
3) Image Segmentation analysis of individual microsporidia spores(Matt)
    - Goal is to learn segmentation techniques and perhaps take a slight detour to track polar tube firing in raw .nd2 files. (Example File in test_folder)