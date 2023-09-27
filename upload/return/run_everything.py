# import os
# import subprocess

# # List of directories containing your Python files
# directories = [
#     '/path/to/directory1',
#     '/path/to/directory2',
#     # Add more directories as needed
# ]

# # Iterate through directories and execute Python files
# for directory in directories:
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith(".py"):
#                 script_path = os.path.join(root, file)
#                 print(f"Running {script_path}")
#                 subprocess.run(["python", script_path])
