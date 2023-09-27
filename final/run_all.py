import subprocess
shared_done = False
scripts_to_run = [r"C:\Users\seren\OneDrive\Documents\Business\Re-sequence\re-sequence.py",
                  r"C:\Users\seren\OneDrive\Documents\Business\Re-sequence\test.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\raw\audio\cmd.py",
                  r"C:\Users\seren\OneDrive\Documents\Business\raw\transcript\gpt.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\together\segment_reorder.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\edit\concatenate.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\edit\extract_audio.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\edit\trim_pauses.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\full_audio.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\full_transcript.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\gpt_img.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\gpt2.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\time_stamp\gc.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\w.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\API_img.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\img_overlay.py", 
                  r"C:\Users\seren\OneDrive\Documents\Business\picture\last_trim.py" ]

for script in scripts_to_run:
    subprocess.call(["python", script])
    shared_done = True
