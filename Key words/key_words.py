import cv2
import numpy as np
import subprocess

# Input and output video paths
input_video = r"C:\Users\seren\OneDrive\Documents\Business\final\FULL_video.mp4"
output_video = "output_video.mp4"
output_audio = "output_audio.mp3"  # Temporary audio file

# OpenCV video capture
cap = cv2.VideoCapture(input_video)

# Get the video's frame width, height, and frames per second (fps)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = int(cap.get(5))

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height), isColor=True)

t = r"C:\Users\seren\OneDrive\Documents\Business\picture\keyword_with_timestamps.txt"
with open(t, "r") as file:
    lines = file.readlines()
    active_texts = []  # List to store active text elements

    for line in lines:
        parts = line.split(',')
        word = parts[0].split(":")[1].strip()
        start_time = float(parts[1].split(":")[1].strip())
        end_time = float(parts[2].split(":")[1].strip()) + 1

        # Check for overlapping time ranges and adjust if necessary
        for active_text in active_texts:
            _, active_start, active_end = active_text
            if active_start <= start_time < active_end:
                start_time = active_end

        text_start_frame = int(start_time * fps)
        text_end_frame = int(end_time * fps)
        active_texts.append((word, start_time, end_time))

    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Iterate through active text elements and draw them on the frame
        for text_element in active_texts:
            word, text_start_time, text_end_time = text_element

            # Check if the current frame is within the desired range to show text
            text_start_frame = int(text_start_time * fps)
            text_end_frame = int(text_end_time * fps)

            if text_start_frame <= frame_number <= text_end_frame:
                text = word
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 7
                font_color = (0, 0, 0)
                font_thickness = 7

                cv2.putText(frame, text, (200, 200), font, font_scale, font_color, font_thickness)

        # Write the frame to the output video
        out.write(frame)

        # Update the active text elements
        active_texts = [(word, start_time, end_time) for word, start_time, end_time in active_texts if frame_number < int(end_time * fps)]

        frame_number += 1

# Release the video objects
cap.release()
out.release()
cv2.destroyAllWindows()

# Extract audio from the input video and save it as a temporary audio file
subprocess.run(['ffmpeg', '-i', input_video, '-vn', '-acodec', 'libmp3lame', output_audio])

# Combine the audio with the text-added video
subprocess.run(['ffmpeg', '-i', output_video, '-i', output_audio, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-strict', 'experimental', 'output_video_with_audio.mp4'])

# Remove the temporary audio file
import os
os.remove(output_audio)

