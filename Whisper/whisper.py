import whisper
from whisper import load_model


model = whisper.load_model("small")
result = model.transcribe(r'C:\Users\seren\OneDrive\Documents\Business\raw\s.mp4')

with open('S_transcript.txt', "w") as f:
    f.write(result['text'])