import streamlit as st
import subprocess
import os

# Streamlit UI
st.title('Emotion Video Generator')
st.write('Upload an image and a speech file to generate a video with neutral emotion.')

# Function to save uploaded files
def save_uploaded_file(uploaded_file, folder_path):
    filepath = os.path.join(folder_path, uploaded_file.name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.sidebar.success(f"{uploaded_file.name} uploaded successfully!")
    return filepath

# Upload image
img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if img_file:
    img_file_path = save_uploaded_file(img_file, "./data/image_samples/")

# Upload speech
speech_file = st.file_uploader("Upload a speech file", type=["wav"])
if speech_file:
    speech_file_path = save_uploaded_file(speech_file, "./data/speech_samples/")

# Output directory
output_dir = st.text_input("Output Directory (within research_intern folder)", value="streamlit_result_neu/")

# Generate video
if st.button('Generate Video') and img_file and speech_file and output_dir:
    # Create output directory if it doesn't exist
    output_dir_path = f"./streamlit_result/{output_dir}"
    os.makedirs(output_dir_path, exist_ok=True)
    
    # Execute the command to generate the video
    cmd = f"python3 generate.py -im {img_file_path} -is {speech_file_path} -m ./model/ -o {output_dir_path}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    st.write(output.decode("utf-8"))

    # Check for video files in the output directory
    video_files = [f for f in os.listdir(output_dir_path) if f.endswith('.mp4')]
    if video_files:
        st.session_state.video_files = video_files
        st.success("Video generated successfully!")
 
    else:
        st.error("Video generation failed.")
        
output_dir_path = f"./streamlit_result/{output_dir}"

# Show result button
if 'video_files' in st.session_state:
    selected_video = st.selectbox('Select a video to view:', st.session_state.video_files)

    if st.button('Show Result'):
        video_path = os.path.join(output_dir_path, selected_video)
        st.write(f"Trying to load video from: {video_path}")
        if os.path.exists(video_path):
            video_file = open(video_path, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
        else:
            st.error("Video file not found.")

