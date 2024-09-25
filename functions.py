import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog
import os
import glob


#open designated folder, output path


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
