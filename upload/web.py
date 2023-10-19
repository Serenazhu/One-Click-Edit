from flask import Flask, render_template, redirect, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
import os
import requests
import sqlite3
from moviepy.editor import VideoFileClip
import urllib
import concurrent.futures
import subprocess
from flask import send_file
import threading
import io


app = Flask(__name__)
app.secret_key = "2006"

@app.route('/')
def index():
    return render_template('title.html')

@app.route('/main')
def main():

    return render_template('index.html')


def get_video_duration(uploaded_file):
    try:
        temp_file_path = 'C:/Users/seren/OneDrive/Documents/Business/temp/' + uploaded_file.filename
        with open(temp_file_path, 'wb') as f:
            f.write(uploaded_file.read())
        video_clip = VideoFileClip(temp_file_path)
        duration = video_clip.duration
        return duration
    except Exception as e:
        print("Error getting video duration:", str(e))
        return None

from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import VideoClip

import os
import subprocess

import subprocess

# def split_video(input_file, output_directory, segment_duration=120):
#     try:
#         command = [
#             "ffmpeg",
#             "-i", input_file,
#             "-c:v", "copy",
#             # "-f", "segment",
#             # "-segment_time", str(segment_duration),
#             # "-reset_timestamps", "1",
#             # "-map", "0",
#             # f"{output_directory}/segment_%03d.mp4"
#         ]

    #     subprocess.run(command, check=True)
    #     print("Video splitting completed successfully.")

    # except subprocess.CalledProcessError as e:
    #     print(f"An error occurred: {e}")



# def get_all_files_in_directory(root_dir):
#         all_files = []
#         for foldername, subfolders, filenames in os.walk(root_dir):
#             for filename in filenames:
#                 file_path = os.path.join(foldername, filename)
#                 all_files.append(file_path)
#         return all_files

# def upload_file(file_path):
#     dbx = get_dropbox_client()

#     db_folder_path = '/uploads/'
#     # Extract the file name from the full path
#     file_name = os.path.basename(file_path)

 
    # dropbox_file_path = os.path.join(db_folder_path, file_name)
    
    # with open(file_path, 'rb') as f:
    #     dbx.files_upload(f.read(), dropbox_file_path)
# p=None
# all_local_files = []
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    # clear = r"C:\Users\seren\OneDrive\Documents\Business\upload\clear_history.py"
    # subprocess.run(["python", clear])

    #check duration
    all_uploaded_files = request.files.getlist('file')
    for uploaded_file in all_uploaded_files:
        video_duration = get_video_duration(uploaded_file)
        print(video_duration)
        
    #     #Split long videos
    #     if video_duration > 120:
    #         p = 'C:/Users/seren/OneDrive/Documents/Business/temp/' + uploaded_file.filename
    #         # Split the video if it's longer than 3 minutes
    #         split_video(p, 'C:/Users/seren/OneDrive/Documents/Business/temp')

    #         root_directory = r"C:\Users\seren\OneDrive\Documents\Business\temp"
    #     # Get a list of all files in the directory and its subdirectories
            # for root, direct, files in os.walk(root_directory):
            #     for file in files:
            #         file_path = os.path.join(root, file)
            #         all_local_files.append(file_path)
            # print(all_local_files)
            #all_local_files.remove(p)
    # Use concurrent.futures.ThreadPoolExecutor
        #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            
        #         for file_path in all_local_files:
        #             executor.submit(upload_file, file_path)
        # else: 
        #     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        #         for file_path in all_local_files:
        #             executor.submit(upload_file, file_path)

    return render_template('index.html')



@app.route('/join')
def authoPage():
    return render_template('autho.html')
import json
@app.route('/Authentication', methods=['GET','POST'])
def autho():
    response = {}
    response2 = {}

    

    if request.method == 'POST': #sending data to a server
        unique_username = request.form.get("unique-username1")
        email = request.form.get("email1")
        username = request.form.get("username1")
        print("unique_username:", unique_username)
        print("email:", email)
        print("username:", username)

        if username is None:
            try:
                user_folder = "C:/Users/seren/OneDrive/Documents/Business/Users/" + unique_username
                os.makedirs(user_folder) 
                insert_email(email)
                response['status'] = 'user_created'
                return json.dumps(response) #serializes dictionaly into a JSON formatted string
            except FileExistsError as e:
                response['status'] = 'username_exists'
                return json.dumps(response) #convert a Python dictionary into JSON formatted string
        
        if unique_username is None and email is None:
            print("username: "+ username)
            user_folder = "C:/Users/seren/OneDrive/Documents/Business/Users/" + username
            if os.path.exists(user_folder):
                response2['status'] = 'user_does_exist'
            
            else:
                response2['status'] = 'user_does_not_exist'
                print(response2)
        

    return json.dumps(response2)
        


@app.route('/list_files')
def list_files():
    folder_path = r"C:\Users\seren\OneDrive\Documents\Business\temp"
    file_names = []
# Create a Path object for the folder
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # List all files in the folder
        for file_name in os.listdir(folder_path):
            # Check if the item is a file
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                file_names.append(file_name)
    print(file_names)
    return render_template('file_list.html', file_names=file_names)


def get_db_connection():
    connection = sqlite3.connect('feedback.db')  
    connection.row_factory = sqlite3.Row
    return connection

def insert_feedback(message):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO feedback (message) VALUES (?)', (message,))
        connection.commit()
    except Exception as e:
        print("Error inserting feedback:", str(e))
    finally:
        connection.close()

def insert_email(email):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users_email (email) VALUES(?)', (email,))
    connection.commit()

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback_message = request.form['feedback']
        insert_feedback(feedback_message)
        return render_template('thank_you.html') 
    
@app.route('/feature_options')
def select_features():
    return render_template('choose_features.html')

@app.route('/download_files', methods=['GET','POST'])
def download_files():

    db_folder_path = '/uploads/' 
    local_folder_path = 'C:/Users/seren/OneDrive/Documents/Business/raw/' 

    run_with_kw = r"C:\Users\seren\OneDrive\Documents\Business\final\run_with_kw.py"
    run_default = r'C:\Users\seren\OneDrive\Documents\Business\final\run_default.py' #OK
    run_with_img = r'C:\Users\seren\OneDrive\Documents\Business\final\run_all.py' #OK
    run_everything = r"C:\Users\seren\OneDrive\Documents\Business\final\run_everything.py"

    if len(selected_checkboxes) == 0:
        subprocess_process = subprocess.Popen(["python", run_default])
    elif len(selected_checkboxes) == 1:
        if 'Img Overlay' in selected_checkboxes:
            subprocess_process = subprocess.Popen(["python", run_with_img])
        else:
            subprocess_process = subprocess.Popen(["python", run_with_kw])
    elif len(selected_checkboxes) == 2:
            subprocess_process = subprocess.Popen(["python", run_everything])

        #subprocess_process = subprocess.Popen(["python", run_all])
    return render_template('wait.html')


@app.route('/join_us', methods=['POST'])
def join():
    if request.method == 'POST':
        global selected_checkboxes
        selected_checkboxes = request.form.getlist('checkbox')
        print(selected_checkboxes)
    return render_template('join_us.html')

@app.route('/check_status')
def check_status():
    p = r'c:\Users\seren\OneDrive\Documents\Business\FINAL.mp4'
    if os.path.exists(p):
        return render_template('done.html')
    else:
        return render_template('patient.html')
   
@app.route('/wait')
def display_wait_template():
    return render_template('wait.html')


import time
@app.route('/download_final')
def download_final():

    FINAL_path = r"C:\Users\seren\OneDrive\Documents\Business\FINAL.mp4"
    file_name = "FINAL.mp4"

  
    with open(FINAL_path, 'rb') as file:
        video_binary_data = file.read()

    name = 'edited_video.mp4'
    edited_video_stream = io.BytesIO(video_binary_data)

    response = send_file(
        edited_video_stream,
        as_attachment=True,
        download_name='edited_video.mp4',
        mimetype='application/octet-stream'
    )
      
    

    time.sleep(30)


            
    return response



if __name__ == '__main__':
    app.run(debug=True)
