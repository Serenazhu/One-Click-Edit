import os
import ffmpeg

folder_path = r'C:\Users\seren\OneDrive\Documents\Business\raw'
output_folder = r'C:\Users\seren\OneDrive\Documents\Business\raw\audio'

for file in os.listdir(folder_path):
    input_segment = os.path.join(folder_path, file)
    output_audio = os.path.join(output_folder, f'{os.path.splitext(file)[0]}.wav')

    try:
        (
            ffmpeg
            .input(input_segment)
            .output(output_audio, format='wav')
            .run()
        )
    except ffmpeg._run.Error as e:
        print(f"Error occurred while processing '{file}':")
        print(e.stderr)
