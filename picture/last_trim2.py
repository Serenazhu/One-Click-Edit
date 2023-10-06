from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

# Specify the input video file
input_video_path = r"C:\Users\seren\OneDrive\Documents\Business\output_video_with_audio2.mp4"

# Define the duration of the trimmed video
start_time = 0  # Start from the beginning of the video
end_time = VideoFileClip(input_video_path).duration - 0.1  # Trim the last half-second

# Specify the output file for the trimmed video
output_trimmed_video_path = 'FINAL.mp4'

# Trim the video using ffmpeg_extract_subclip
ffmpeg_extract_subclip(input_video_path, start_time, end_time, targetname=output_trimmed_video_path)

# Done! The trimmed video is now saved as 'trimmed_video.mp4'

