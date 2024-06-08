import subprocess
import os

# Define the paths to the input and output audio files
input_audio_path = './test2.flac'
output_audio_path = './md_test2.flac'

# Ensure the output directory exists
output_dir = os.path.dirname(output_audio_path)
os.makedirs(output_dir, exist_ok=True)

# Command to downsample the audio to 8 kHz using ffmpeg
ffmpeg_command = f'ffmpeg -i "{input_audio_path}" -ar 8000 "{output_audio_path}"'

# Run the command
subprocess.run(ffmpeg_command, shell=True, check=True)

print(f"Audio has been downsampled and saved to {output_audio_path}")

