import os
import random
import h5py
import numpy as np
import shutil

# Define the folder containing HDF files
folder_path = '/home/sysadm/Downloads/hdf5_folder'
train_hdf_folder_path = '/home/sysadm/Downloads/train_hdf5_folder'
val_hdf_folder_path = '/home/sysadm/Downloads/val_hdf5_folder'

# Create the directories if they don't exist
os.makedirs(train_hdf_folder_path, exist_ok=True)
os.makedirs(val_hdf_folder_path, exist_ok=True)

# Get a list of all HDF files in the folder
hdf_files = [filename for filename in os.listdir(folder_path) if filename.endswith('.hdf5')]

# Define intensity_dict
intensity_dict = {'XX': 0, 'LO': 1, 'MD': 2, 'HI': 3}

# Copy HDF files to appropriate folders
for hdf_file in hdf_files:
    # Extract labels from file name
    labels = os.path.splitext(hdf_file)[0].split('_')
    emotion_intensity = intensity_dict.get(labels[3], -1)  # Get intensity, default to -1 if not found
    
    # Set destination path based on intensity
    dest_folder = val_hdf_folder_path if emotion_intensity == 3 else train_hdf_folder_path
    
    # Copy file to appropriate folder
    src_path = os.path.join(folder_path, hdf_file)
    dest_path = os.path.join(dest_folder, hdf_file)
    shutil.copy(src_path, dest_path)
    
    print(f"File {hdf_file} copied successfully to {dest_folder}.")
print("\nall HDF files copied to their respective folders.")
