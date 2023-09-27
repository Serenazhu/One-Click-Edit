import ffmpeg

def extract_audio(input_video_path, output_audio_path):
    ffmpeg.input(input_video_path).output(output_audio_path, format='wav').run()

if __name__ == "__main__":
    input_video_path = r"C:\Users\seren\OneDrive\Documents\Business\final\FULL_video.mp4"   # Path to your input video file
    output_audio_path = r"C:\Users\seren\OneDrive\Documents\Business\final\full_output_audio.wav"  # Path to the output audio file
    
    extract_audio(input_video_path, output_audio_path)