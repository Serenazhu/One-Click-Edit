import os
import subprocess
file_path = r"C:\Users\seren\OneDrive\Documents\Business\final\full_output_audio.wav"
output_folder_path = r"C:\Users\seren\OneDrive\Documents\Business\picture"
command = f'whisper "{file_path}" --output_dir "{output_folder_path}" --output_format txt'
subprocess.run(command, shell=True)