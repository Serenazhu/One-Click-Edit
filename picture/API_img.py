import openai
from PIL import Image
import requests
from io import BytesIO
import os

# Set your OpenAI API key
openai.api_key = "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"
l = []
# Read the keywords from the text file
with open(r'C:\Users\seren\OneDrive\Documents\Business\final\actual_keywords.txt', 'r') as file:
    for line in file:
        words = line.split()
        for word in words:
            l.append(word)
print(l)

   



output_folder = r"C:\Users\seren\OneDrive\Documents\Business\picture\imgs"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Now you can iterate through the list of words
for w in l:
    response = openai.Image.create(
        prompt=f"a clip art of a {w}",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    response = requests.get(image_url)
    image_data = BytesIO(response.content)

    # Open the image using PIL
    image = Image.open(image_data)

    # Specify the full path and filename where you want to save the image
    output_filename = f"{w}_image.png"
    output_path = os.path.join(output_folder, output_filename)

    # Save the image to the specified path
    image.save(output_path)

    print(f"Image for '{w}' saved to '{output_path}'")
