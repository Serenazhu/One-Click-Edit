import re

# Open the text file for reading
with open(r"C:\Users\seren\OneDrive\Documents\Business\picture\keyword_with_timestamps.txt", "r") as file:
    lines = file.readlines()

# Define a regular expression pattern to extract words after "Word:"
pattern = r"Word: ([\w'-]+),"

# Initialize a list to store the extracted words
extracted_words = []

# Process each line in the file
for line in lines:
    # Use regular expression to find and extract the word
    match = re.search(pattern, line)
    if match:
        extracted_word = match.group(1)
        extracted_words.append(extracted_word)

# Save the extracted words to a new text file
output_file_path = r"C:\Users\seren\OneDrive\Documents\Business\final\actual_keywords.txt"
with open(output_file_path, "w") as output_file:
    # Write each extracted word to the output file
    for extracted_word in extracted_words:
        output_file.write(extracted_word + "\n")

# Print a message indicating where the result is saved
print(f"Extracted words saved to {output_file_path}")

