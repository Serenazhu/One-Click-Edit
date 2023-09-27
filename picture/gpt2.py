import openai
import os

openai.api_key = "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"

# Open the file in read mode
with open(r'C:\Users\seren\OneDrive\Documents\Business\picture\keywords.txt', 'r') as file:
    # Read the contents of the file
    transcript = file.read()

query="Read the list of keywords extracted from a video. Get rid of the ones that are repetitive, not important or the ones that seems like a person's name. get rid at least one third of the original list and give me a new list in square brackets without title "+ transcript

message = [
    {"role": "system", "content": "You are a helpful assistant that will get rid of keywords that don't need to be emphasized visually"},
    {"role": "user", "content": query}
]



completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages =message,
)

reply = completion.choices[0].message.content


d = r"C:\Users\seren\OneDrive\Documents\Business\picture"
t = 'min_keywords.txt'
output_file_path = os.path.join(d, t)

with open(output_file_path, 'w') as output_file:
    output_file.write(reply)
