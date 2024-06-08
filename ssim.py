from skimage.metrics import structural_similarity as ssim
import cv2
import os

def calculate_ssim(img1, img2):
    # Convert the images to grayscale (SSIM is often computed on grayscale images)
    gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM
    score, _ = ssim(gray_img1, gray_img2, full=True)
    return score
    
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

def calculate_video_ssim(video_path1, video_path2):
    frames1 = get_video_frames(video_path1)
    frames2 = get_video_frames(video_path2)
    
    if len(frames1) != len(frames2):
        raise ValueError("Videos do not have the same number of frames")

    total_ssim = 0
    frame_count = len(frames1)
    
    for frame1, frame2 in zip(frames1, frames2):
        ssim_score = calculate_ssim(frame1, frame2)
        total_ssim += ssim_score
    
    avg_ssim = total_ssim / frame_count
    return avg_ssim

def calculate_average_ssim_for_folders(base_path):
    folder_names = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
    ssim_values = []
    
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

        if len(video_files) != 2:
            raise ValueError(f"Folder {folder} does not contain exactly two video files.")
        
        video_path1 = os.path.join(folder_path, video_files[0])
        video_path2 = os.path.join(folder_path, video_files[1])
        
        ssim_value = calculate_video_ssim(video_path1, video_path2)
        ssim_values.append(ssim_value)
    
    average_ssim = sum(ssim_values) / len(ssim_values)
    return average_ssim



# Define the base path to the folder containing 50 subfolders
base_path = '/home/sysadm/Downloads/emotalkingface/video_result_compare/'

# Calculate the average SSIM across all folders
average_ssim = calculate_average_ssim_for_folders(base_path)
print(f"Average SSIM for all folders: {average_ssim}")
