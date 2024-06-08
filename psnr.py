import cv2
import numpy as np
import os

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return float('inf')
    psnr = 20 * np.log10(255.0 / np.sqrt(mse))
    return psnr

def get_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def calculate_video_psnr(video_path1, video_path2):
    frames1 = get_video_frames(video_path1)
    frames2 = get_video_frames(video_path2)
    
    if len(frames1) != len(frames2):
        raise ValueError("Videos do not have the same number of frames")

    total_psnr = 0
    frame_count = len(frames1)
    
    for frame1, frame2 in zip(frames1, frames2):
        psnr = calculate_psnr(frame1, frame2)
        total_psnr += psnr
    
    avg_psnr = total_psnr / frame_count
    return avg_psnr

def calculate_average_psnr_for_folders(base_path):
    folder_names = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
    psnr_values = []
    
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

        if len(video_files) != 2:
            raise ValueError(f"Folder {folder} does not contain exactly two video files.")
        
        video_path1 = os.path.join(folder_path, video_files[0])
        video_path2 = os.path.join(folder_path, video_files[1])
        
        psnr = calculate_video_psnr(video_path1, video_path2)
        psnr_values.append(psnr)
    
    average_psnr = sum(psnr_values) / len(psnr_values)
    return average_psnr

# Define the base path to the folder containing 50 subfolders
base_path = '/home/sysadm/Downloads/emotalkingface/video_result_compare/'

# Calculate the average PSNR across all folders
average_psnr = calculate_average_psnr_for_folders(base_path)
print(f"Average PSNR for all folders: {average_psnr}")
