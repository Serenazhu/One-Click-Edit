import cv2
import subprocess
from moviepy.editor import VideoFileClip

overlay_info = []
count = 0
video_path = r"C:\Users\seren\OneDrive\Documents\Business\final\FULL_video.mp4"
img_folder = "C:/Users/seren/OneDrive/Documents/Business/picture/imgs/"
output_video_path = 'output_video.mp4'

# Open the original video to extract information
original_cap = cv2.VideoCapture(video_path)
original_width = int(original_cap.get(3))
original_height = int(original_cap.get(4))
original_frame_rate = original_cap.get(cv2.CAP_PROP_FPS)
original_codec = original_cap.get(cv2.CAP_PROP_FOURCC)

t = r"C:\Users\seren\OneDrive\Documents\Business\picture\keyword_with_timestamps.txt"
with open(t, "r") as file:
    lines = file.readlines()
    for line in lines:
        count += 1
        parts = line.split(',')
        word = parts[0].split(":")[1].strip()
        start_time = float(parts[1].split(":")[1].strip())
        end_time = float(parts[2].split(":")[1].strip())+1
        name = count
        name = img_folder + word + "_image.png"
        new = {'image_path': name, 'start_time': start_time, 'end_time': end_time}
        overlay_info.append(new)

print(overlay_info)

# Create a VideoWriter object using FFmpeg with the same settings as the original video
ffmpeg_command = [
    'ffmpeg',
    '-y',  # Overwrite output file if it exists
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{original_width}x{original_height}',
    '-pix_fmt', 'bgr24',
    '-r', str(original_frame_rate),  # Use the original frame rate
    '-i', '-',  # Input from pipe
    '-an',  # Disable audio
    '-vcodec', 'libx264',  # Use H.264 codec
    '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
    output_video_path
]

ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Initialize variables
current_time = 0
current_overlay = 0

while True:
    ret, frame = original_cap.read()
    if not ret:
        break

    current_time += 1 / original_frame_rate  # Update current time based on frame rate

    if current_overlay < len(overlay_info):
        overlay_start_time = overlay_info[current_overlay]['start_time']
        overlay_end_time = overlay_info[current_overlay]['end_time']

        if overlay_start_time <= current_time <= overlay_end_time:
            overlay_image = cv2.imread(overlay_info[current_overlay]['image_path'])

            # Resize the overlay image to a smaller size while maintaining aspect ratio
            scale_percent = 30  # Adjust this percentage as needed
            width = int(overlay_image.shape[1] * scale_percent / 100)
            height = int(overlay_image.shape[0] * scale_percent / 100)
            overlay_image = cv2.resize(overlay_image, (width, height))

            # Overlay the resized image onto the video frame
            overlay_height, overlay_width, _ = overlay_image.shape

            # Calculate the position (x, y) for the bottom-right corner
            x = original_width - overlay_width
            y = original_height - overlay_height
            frame[y:y + overlay_height, x:x + overlay_width] = overlay_image

        if current_time > overlay_end_time:
            current_overlay += 1

    # Write the frame to the FFmpeg process
    ffmpeg_process.stdin.write(frame.tobytes())

# Close the FFmpeg process when finished
ffmpeg_process.stdin.close()
ffmpeg_process.wait()

original_cap.release()

# Combine the video with audio using moviepy
video_without_audio = VideoFileClip(output_video_path)
original_audio = VideoFileClip(video_path).audio

video_with_audio = video_without_audio.set_audio(original_audio)

# Write the final video with audio
output_video_with_audio_path = 'output_video_with_audio.mp4'
video_with_audio.write_videofile(output_video_with_audio_path, codec='libx264', audio_codec='aac')

# Close the video file objects
video_without_audio.close()
video_with_audio.close()

