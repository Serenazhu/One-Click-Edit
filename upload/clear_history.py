import os
import shutil

# Define the root directory you want to start searching from
root_directory = r'c:\Users\seren\OneDrive\Documents\Business'

# Function to delete files with specific extensions recursively
def delete_files_with_extensions(directory, extensions):
    for root, _, files in os.walk(directory):
        # Check if the current directory is a .git directory
        if '.git' in root.split(os.path.sep):
            continue  # Skip files in the .git directory
        for file in files:
            if any(file.lower().endswith(extension) for extension in extensions):
                file_path = os.path.join(root, file)
                # Check if the file is named 'logo_f.png' and skip it
                if file.lower() == 'logo_f.png' or file.lower() == '.gitignore.txt':
                    continue
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# List of file extensions to delete
extensions_to_delete = ['.mp4', '.wav', '.txt', '.png', '.mp3']

# Call the function to delete files with specified extensions
delete_files_with_extensions(root_directory, extensions_to_delete)
