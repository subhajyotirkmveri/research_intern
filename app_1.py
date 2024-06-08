import streamlit as st
import subprocess
import os

# Streamlit UI
st.title('Emotion Video Generator')
st.write('Upload an image and a speech file to generate a video with neutral emotion.')

# Upload image
img_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if img_file:
    st.success("Image file uploaded successfully!")

# Upload speech
speech_file = st.file_uploader("Upload a speech file", type=["wav"])
if speech_file:
    st.success("Speech file uploaded successfully!")

# Output directory
output_dir = st.text_input("Output Directory (within research_intern folder)", value="streamlit_result_neu_kaggle_im01_check_stream/")

# Generate video
if st.button('Generate Video') and img_file and speech_file and output_dir:
    # Create output directory if it doesn't exist
    output_dir_path = f"./streamlit_result/{output_dir}"
    os.makedirs(output_dir_path, exist_ok=True)
    
    # Execute the command to generate the video
    cmd = f"python3 generate_1.py -im ./data/image_samples/{img_file.name} -is ./data/speech_samples/{speech_file.name} -m ./model/ -o {output_dir_path}"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    st.write(output.decode("utf-8"))

    st.write(f'Video saved to {output_dir_path}')

