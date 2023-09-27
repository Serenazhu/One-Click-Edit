import openai
import os

openai.api_key = "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"

folder_path = r"C:\Users\seren\OneDrive\Documents\Business\raw\transcript"
file_list = os.listdir(folder_path)
text_extensions = ['.txt']
all_files = []
for file in file_list:
    file_extension = os.path.splitext(file)[1].lower()
    if file_extension in text_extensions:
        file_path = os.path.join(folder_path, file)
        all_files.append(file_path)
file_contents = []
for path in all_files:
    with open(path, "r") as file:
        content = file.read()
        file_contents.append(content)
combined_content = "\n".join(file_contents)




query="Reorder the following sentences to create a coherent paragraph: "+ combined_content

message = [
    {"role": "system", "content": "You are a helpful assistant that will reorder these sentences."},
    {"role": "user", "content": query}
]



completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages =message,
)

reply = completion.choices[0].message.content


d = r"C:\Users\seren\OneDrive\Documents\Business\together"
t = 'ordered_transcript.txt'
output_file_path = os.path.join(d, t)

with open(output_file_path, 'w') as output_file:
    output_file.write(reply)




