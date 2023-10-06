import openai
import os

openai.api_key = "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"

# Open the file in read mode
with open(r'C:\Users\seren\OneDrive\Documents\Business\picture\full_output_audio.txt', 'r') as file:
    # Read the contents of the file
    transcript = file.read()

query="Read the transcript for a video and give me a list of individual important keywords. Do not select keywords that are a person's names. Also do not put a few relating keywords together as one keyword: "+ transcript

message = [
    {"role": "system", "content": "You are a helpful assistant that will spot important individual keywords"},
    {"role": "user", "content": query}
]



completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages =message,
)

reply = completion.choices[0].message.content


d = r"C:\Users\seren\OneDrive\Documents\Business\Key words"
t = 'keywords.txt'
output_file_path = os.path.join(d, t)

with open(output_file_path, 'w') as output_file:
    output_file.write(reply)