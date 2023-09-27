from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

folder_path = r"C:\Users\seren\OneDrive\Documents\Business\raw"
extensions = (".mp4", ".mov", ".MOV")

video_list = []

for filename in os.listdir(folder_path):
    if filename.endswith(extensions):
        video_list.append(f'C:/Users/seren/OneDrive/Documents/Business/raw/{filename}')

vl = []
count = 0
for i in video_list:
    count+=1 
    n=str(count)
    n = VideoFileClip(rf'{i}')
    vl.append(n)


final_clip = concatenate_videoclips(vl, method="compose")

# # Export the concatenated video
final_clip.write_videofile('combined_video.mp4', codec='libx264')
