import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import os
import glob
import subprocess

#open designated folder, output path

import tracemalloc

tracemalloc.start()

# Your code here

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)




def pull_file():
        """
        this function captures the selected users input directory. 
        Returns:
            directory_path: selected directory
        """
        # Create the root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open a file dialog for selecting a file
        directory_path = filedialog.askdirectory(parent=root) + "/*"

        # Check if a file was selected
        
        if directory_path:  # Ensure the user selected a directory
            print(f"Selected Directory: {directory_path}")
        else:
            print("No directory selected.")
        return directory_path
# import subprocess

# # Call an R script
# subprocess.run(["Rscript", "path/to/script.R"])

def passtofile(data, filename):
    #assuming its a single 
    file = open(filename + ".txt",'w')
    file.write("Spacer\n")
    for i in data:
        file.write(str(i) + "\n")  
    file.close()   
def run_r_histogram(file, path, datafile):
     subprocess.run([file,path,datafile])
         

##Decided a custom class would have been the best method to properly analayze sets. Creation will probably be dynamic
##
class Image():
    def __init__(self,input_image):
        self.image = input_image
        self.tiles = self._tiling()
    def _tiling(self):
        tiling_dictionary = {}
        x,y = self.image.shape
        #Tiling at 16,32,64
        if x%16 != 0:
            return 
        tiles = [16,32,64,256]
        #tiles the image into 144 16x16 arrays.  -1 is added to avoid out of bound indexing
        """
        This for loop, loops through the tiles list. List comphrehension then outputs a dictionary with the given tiles
        with tilesize x tilesize as the key and stores it in the self.tiles class object. 
        """
        for j in tiles: 
            tiling_dictionary[str(j)+'x'+str(j)] = np.array([self.image[i:i+j,i:i+j] for i in range(0,x,j)])
        return(tiling_dictionary)
              
              
