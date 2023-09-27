import os
import subprocess
script_directory = os.path.dirname(os.path.abspath(__file__))
folder_path = r'C:\Users\seren\OneDrive\Documents\Business\raw\audio'
output_folder_path = r'C:\Users\seren\OneDrive\Documents\Business\raw\transcript'
file_list = os.listdir(folder_path)
audio_extensions = ['.mp3', '.wav']

for file in file_list:
    file_extension = os.path.splitext(file)[1].lower()
    if file_extension in audio_extensions:
        file_path = os.path.join(folder_path, file)
        command = f'whisper "{file_path}" --output_dir "{output_folder_path}" --output_format txt'
        subprocess.run(command, shell=True)



