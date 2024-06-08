import cv2
import os

def extract_frames(video_path, output_folder, interval=0.2):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # Calculate the interval in terms of frames
    frame_interval = int(fps * interval)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Initialize the frame count for the first frame
    frame_count = int(fps * 0.2)
    saved_frames = 0

    while cap.isOpened():
        # Set the frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame
        frame_time = frame_count / fps
        output_filename = f"{output_folder}/frame_{frame_time:.1f}.jpg"
        cv2.imwrite(output_filename, frame)
        saved_frames += 1

        # Increment the frame count
        frame_count += frame_interval

        # Stop if we reach the desired duration (2 seconds)
        if frame_time >= 2.0:
            break

    cap.release()
    print(f"Extracted {saved_frames} frames.")

# Example usage
video_path = '/home/sysadm/Downloads/neu_results_speech_kag_01/neutral_generated.mp4_.mp4'  # Path to your video file
output_folder = '/home/sysadm/Downloads/neu_results_speech_kag_01/extracted_frames_0.2'  # Folder to save the extracted frames
extract_frames(video_path, output_folder)
