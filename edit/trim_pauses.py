from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt

def detect_silence(audio, silence_threshold=-40, min_silence_duration=900):
    silent_segments = []
    start_time = None

    for i, sample in enumerate(audio):
        if sample.dBFS < silence_threshold:
            if start_time is None:
                start_time = i
        elif start_time is not None:
            end_time = i
            if end_time - start_time >= min_silence_duration:
                start_time+=700
                silent_segments.append((start_time, end_time))
            start_time = None
    if start_time is not None:
        silent_segments.append((start_time, len(audio)))

    return silent_segments

# Read the Audiofile
audio_file = r"C:\Users\seren\OneDrive\Documents\Business\edit\output_audio.wav"
audio = AudioSegment.from_file(audio_file, format="wav")

# Detect silent segments
silent_segments = detect_silence(audio)
print("Detected Silent Segments:", silent_segments)

# Calculate time array
duration = len(audio) / audio.frame_rate
time = np.linspace(0, duration, len(audio.get_array_of_samples()))  # Corrected time array

# Plotting the Graph using Matplotlib
plt.plot(time, audio.get_array_of_samples())
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('audio_file')
#plt.show()
audio_parts = []
def cut_segments(audio, segments):
    audio_parts = []


    # Cut the audio based on segments
    start = 0
    for segment in segments:
        end = segment[0]
        if end > start:
            audio_parts.append(audio[start:end])
        start = segment[1]

    # Add the last segment if needed
    if start < len(audio):
        audio_parts.append(audio[start:])

    # Concatenate the audio segments
    final_audio = audio_parts[0]
    for segment in audio_parts[1:]:
        final_audio = final_audio + segment

    return final_audio

# Cut silent segments from the audio
final_audio = cut_segments(audio, silent_segments)


# Export the final audio to a new file
#final_audio.export("without_silence.wav", format="wav")
print("Silent segments removed and new audio saved.")

#-----------------------------------------------------




from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips

def main():
    input_file = r"C:\Users\seren\OneDrive\Documents\Business\raw\video\concatenated_video.mp4"
    output_file = r"C:\Users\seren\OneDrive\Documents\Business\final\FULL_video.mp4"


    # Convert time ranges from milliseconds to seconds
    cut_segments = [(start / 1000, end / 1000) for start, end in silent_segments]

    video_clip = VideoFileClip(input_file)
    remaining_segments = []

    # Create video segments without silent segments
    previous_end = 0
    duration = video_clip.duration
    tolerance = 0.1  # Adjust this value based on your needs
    for start, end in cut_segments:
        if start > previous_end + tolerance:
            remaining_segments.append(video_clip.subclip(previous_end, start))
        previous_end = end

    if previous_end < duration:
        remaining_segments.append(video_clip.subclip(previous_end, duration))

    # Concatenate the remaining segments
    final_clip = concatenate_videoclips(remaining_segments)

    # Write the final video file
    final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

if __name__ == "__main__":
    main()
