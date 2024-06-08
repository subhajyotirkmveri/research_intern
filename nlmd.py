import dlib
import cv2
import numpy as np

# Load pre-trained face detector and landmark predictor from dlib
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')  # You need to download this file

def extract_landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        return None  # No faces detected
    landmarks = predictor(gray, faces[0])
    landmarks = [(p.x, p.y) for p in landmarks.parts()]
    return np.array(landmarks)

def calculate_nlmd(landmarks1, landmarks2):
    if landmarks1 is None or landmarks2 is None or len(landmarks1) != len(landmarks2):
        return None  # Landmarks not detected or different numbers of landmarks

    distances = np.linalg.norm(landmarks1 - landmarks2, axis=1)
    mean_distance = np.mean(distances)
    inter_ocular_distance = np.linalg.norm(landmarks1[36] - landmarks1[45])  # Distance between the eyes

    nlmd = mean_distance / inter_ocular_distance
    return nlmd

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

def calculate_video_nlmd(video_path1, video_path2):
    frames1 = get_video_frames(video_path1)
    frames2 = get_video_frames(video_path2)
    
    if len(frames1) != len(frames2):
        raise ValueError("Videos do not have the same number of frames")

    total_nlmd = 0
    frame_count = 0
    
    for frame1, frame2 in zip(frames1, frames2):
        landmarks1 = extract_landmarks(frame1)
        landmarks2 = extract_landmarks(frame2)
        nlmd = calculate_nlmd(landmarks1, landmarks2)
        if nlmd is not None:
            total_nlmd += nlmd
            frame_count += 1
    
    if frame_count == 0:
        return None  # No valid frames with detected landmarks

    avg_nlmd = total_nlmd / frame_count
    return avg_nlmd

def calculate_average_nlmd_for_folders(base_path):
    folder_names = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
    nlmd_values = []
    
    for folder in folder_names:
        folder_path = os.path.join(base_path, folder)
        video_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]

        if len(video_files) != 2:
            raise ValueError(f"Folder {folder} does not contain exactly two video files.")
        
        video_path1 = os.path.join(folder_path, video_files[0])
        video_path2 = os.path.join(folder_path, video_files[1])
        
        nlmd_value = calculate_video_nlmd(video_path1, video_path2)
        nlmd_values.append(nlmd_value)
    
    average_nlmd = sum(nlmd_values) / len(nlmd_values)
    return average_nlmd
    
# Define the base path to the folder containing 50 subfolders
base_path = '/home/sysadm/Downloads/emotalkingface/video_result_compare/'

# Calculate the average NLMD across all folders
average_ssim = calculate_average_nlmd_for_folders(base_path)
print(f"Average NLMD for all folders: {average_ssim}")
