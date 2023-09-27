import subprocess
import os
import re
import time

def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    return -1

def main():
    start_time = time.time()  # Record the start time

    video_folder_path = r"c:\Users\seren\OneDrive\Documents\Business\raw\video"
    output_path = os.path.join(video_folder_path, "concatenated_video.mp4")
    input_file_path = os.path.join(video_folder_path, "input.txt")

    video_extensions = ['.mp4', '.avi', '.mov', '.MOV']
    all_files = [file for file in os.listdir(video_folder_path)
                 if os.path.splitext(file)[1].lower() in video_extensions]

    sorted_files = sorted(all_files, key=extract_number)  # Sort based on numbering

    with open(input_file_path, 'w') as input_file:
        for video_file in sorted_files:
            input_file.write(f"file '{os.path.join(video_folder_path, video_file)}'\n")

    # Use FFmpeg to concatenate the videos
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', input_file_path,
        '-c', 'copy',
        output_path
    ]

    subprocess.run(cmd)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print("Concatenation complete. Concatenated video saved to:", output_path)
    print("Total time taken:", elapsed_time, "seconds")

if __name__ == "__main__":
    main()

