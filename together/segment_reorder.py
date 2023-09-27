import os
import shutil

# Path to the transcript containing the words you want to match
transcript_path = r"C:\Users\seren\OneDrive\Documents\Business\together\ordered_transcript.txt"
with open(transcript_path, "r") as file:
    goal = file.read().split()

# Path to the directory containing the text and video files to check against
seg_transcript_path = r"c:\Users\seren\OneDrive\Documents\Business\raw\transcript"
video_transcript_path = r"c:\Users\seren\OneDrive\Documents\Business\raw\video"
text_extensions = ['.txt']
video_extensions = ['.mp4']  # Replace with the appropriate video extensions
all_files = [os.path.join(seg_transcript_path, file) for file in os.listdir(seg_transcript_path)
             if os.path.splitext(file)[1].lower() in text_extensions]

file_count = len(all_files)
print('FILE COUNT:', file_count)

file_contents = []

# Read and concatenate the content of all text files
for path in all_files:
    with open(path, "r") as file:
        content = file.read()
        file_contents.append(content)

combined_content = " ".join(file_contents)
current = combined_content.split()

# Divide the goal into parts based on the number of files
num_words_per_part = len(goal) // file_count
goal_parts = [goal[i:i + num_words_per_part] for i in range(0, len(goal), num_words_per_part)]

min_percentage = 0.6
p = r"C:\Users\seren\OneDrive\Documents\Business\together"
v = r"C:\Users\seren\OneDrive\Documents\Business\raw\video"

check_count = 0
updated_files = all_files.copy()
processed_files = set()  # Keep track of processed files

for part_num, part in enumerate(goal_parts, start=1):
    num_required_matches = int(len(part) * min_percentage)
    part_name = str(part_num)

    # Create a dictionary to store already processed files and their corresponding video file
    processed_files_dict = {}

    for f in updated_files:
        if f in processed_files:
            continue  # Skip already processed files

        with open(f, 'r') as file:
            con = file.read()
            matching_words = sum(1 for word in part if word in con)
            if matching_words >= num_required_matches:
                base_name = os.path.basename(f)
                file_name, file_extension = os.path.splitext(base_name)
                new_file_name = f"{file_name}{part_name}{file_extension}"

                # Check if the file has already been processed with this part_name
                if file_name in processed_files_dict:
                    # Rename the file with the existing part_name
                    existing_part_name = processed_files_dict[file_name]
                    new_file_name = f"{file_name}{existing_part_name}{file_extension}"

                new_file_path = os.path.join(p, new_file_name)
                shutil.copy2(f, new_file_path)
                print(f"Text File '{base_name}' has been renamed to '{new_file_name}'")
                check_count += 1
                updated_files.remove(f)  # Remove the processed file from the list
                processed_files.add(f)  # Mark the file as processed
                processed_files_dict[file_name] = part_name  # Update the processed files dictionary

                r = r"c:\Users\seren\OneDrive\Documents\Business\raw"
                # Rename the corresponding video file
                video_base_name = os.path.splitext(base_name)[0]  # Extract base name without extension
                video_file_path = os.path.join(r, f"{video_base_name}.mp4")
                new_video_file_name = f"{video_base_name}{part_name}.mp4"
                new_video_file_path = os.path.join(v, new_video_file_name)
                shutil.copy2(video_file_path, new_video_file_path)
                print(f"Video File '{video_base_name}.mp4' has been renamed to '{new_video_file_name}'")

    if check_count >= file_count:
        break

print("Process completed.")










