from flask import Flask, render_template, redirect, session, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth
import dropbox
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

# Configure OAuth
oauth = OAuth(app)
dropbox_oauth = oauth.remote_app(
    'dropbox',
    consumer_key='hre5iem8s3h050b',
    consumer_secret='9uqb4eumdz04e8y',
    base_url='https://api.dropboxapi.com/2/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.dropboxapi.com/oauth2/token',
    authorize_url='https://www.dropbox.com/oauth2/authorize',
    request_token_params={'scope': 'files.content.write files.content.read'},
)

def get_dropbox_client():
    return dropbox.Dropbox(session['dropbox_token'][0])

@app.route('/')
def index():
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

def split_video(input_file, output_dir, max_duration=181):
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Get the video duration using FFmpeg
        duration_command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file]
        video_duration = float(subprocess.check_output(duration_command, universal_newlines=True))

        num_splits = int(video_duration / max_duration) + 1
        split_videos = []

        for i in range(num_splits):
            start_time = i * max_duration
            end_time = (i + 1) * max_duration if i < num_splits - 1 else video_duration
            split_file = os.path.join(output_dir, f"split_{i + 1}.mp4")

            # Use FFmpeg to trim the video segment
            trim_command = ['ffmpeg', '-ss', str(start_time), '-i', input_file, '-t', str(end_time - start_time), '-c:v', 'libx264', '-c:a', 'aac', split_file]
            subprocess.run(trim_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            split_videos.append(split_file)

        return split_videos

    except Exception as e:
        print("Error splitting video:", str(e))
        return []







@app.route('/upload', methods=['POST'])
def upload_file():
    if 'dropbox_token' not in session:
        return redirect('/login')
    dbx = get_dropbox_client()
    #deleting existing files in db
    db_folder_path = '/uploads/'

    try:
        result = dbx.files_list_folder(db_folder_path)
        for entry in result.entries:
            dbx.files_delete_v2(entry.path_display)
    except dropbox.exceptions.ApiError as e:
        if isinstance(e.user_message_text, dict) and 'path' in e.user_message_text:
            print(f"Error: {e.user_message_text['path']}")
        else:
            print(f"General API error: {e}") 
    clear = r"C:\Users\seren\OneDrive\Documents\Business\upload\clear_history.py"
    subprocess.run(["python", clear])
    all_uploaded_files = request.files.getlist('file')
    for uploaded_file in all_uploaded_files:
        if uploaded_file and uploaded_file.filename.endswith('.mp4'):
            video_duration = get_video_duration(uploaded_file)
            print(video_duration)
        if video_duration > 181:
            p = 'C:/Users/seren/OneDrive/Documents/Business/temp/' + uploaded_file.filename
            # Split the video if it's longer than 3 minutes
            split_videos = split_video(p, 'C:/Users/seren/OneDrive/Documents/Business/temp')
            os.remove(p)
    db_folder_path = '/uploads/'

    local = r"C:\Users\seren\OneDrive\Documents\Business\temp"
    all_local_files = os.listdir(local) #listdir gives filenames
    
    def upload_file(file_name):
        local_each_file = os.path.join(local, file_name)
        dropbox_file_path = os.path.join(db_folder_path, file_name)
        with open(local_each_file, 'rb') as f:
            dbx.files_upload(f.read(), dropbox_file_path)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(upload_file, all_local_files)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    return dropbox_oauth.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('dropbox_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = dropbox_oauth.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['dropbox_token'] = (response['access_token'], '')
    return redirect(url_for('index'))

@dropbox_oauth.tokengetter
def get_dropbox_oauth_token():
    return session.get('dropbox_token')

@app.route('/list_files')
def list_files():
    if 'dropbox_token' not in session:
        return redirect('/login')
    dbx = get_dropbox_client()

    try:
        files_list = dbx.files_list_folder('/uploads')
        file_names = [entry.name for entry in files_list.entries if isinstance(entry, dropbox.files.FileMetadata)]
        return render_template('file_list.html', file_names=file_names)
    except dropbox.exceptions.ApiError as e:
        return f"An error occurred: {e}"

def get_db_connection():
    connection = sqlite3.connect('feedback.db')  # Replace 'feedback.db' with your SQLite database file path
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

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        feedback_message = request.form['feedback']
        insert_feedback(feedback_message)
        return render_template('thank_you.html') 

@app.route('/download_files')
def download_files():
    if 'dropbox_token' not in session:
        return redirect('/login')

    dbx = get_dropbox_client()
    db_folder_path = '/uploads/' 
    local_folder_path = 'C:/Users/seren/OneDrive/Documents/Business/raw/' 

    try:
        files_list = dbx.files_list_folder(db_folder_path)
        for entry in files_list.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                file_path = entry.path_display
                _, file_name = os.path.split(file_path)
                local_file_path = os.path.join(local_folder_path, file_name)
                dbx.files_download_to_file(local_file_path, file_path)
        run = r'C:\Users\seren\OneDrive\Documents\Business\final\run_all.py'
        # Start the subprocess in the background
        subprocess_process = subprocess.Popen(["python", run])
        return render_template('wait.html')
    except Exception as e:
        return str(e)

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
    #deleting existing files in db
    db_folder_path = '/uploads/'
    dbx = get_dropbox_client()

    try:
        result = dbx.files_list_folder(db_folder_path)
        for entry in result.entries:
            dbx.files_delete_v2(entry.path_display)
    except dropbox.exceptions.ApiError as e:
        if isinstance(e.user_message_text, dict) and 'path' in e.user_message_text:
            print(f"Error: {e.user_message_text['path']}")
        else:
            print(f"General API error: {e}")
    #upload FINAL to dropbox
    FINAL_path = r"C:\Users\seren\OneDrive\Documents\Business\FINAL.mp4"
    file_name = "FINAL.mp4"
    dropbox_FINAL_path = os.path.join(db_folder_path, file_name)
    with open(FINAL_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_FINAL_path)

    metadata, res = dbx.files_download(path=dropbox_FINAL_path)
    name = 'edited_video.mp4'
        # Set the appropriate content type for the response
    response = send_file(
        io.BytesIO(res.content),
        as_attachment=True,
        download_name=os.path.basename(name),
        mimetype='application/octet-stream'
    )

    time.sleep(60)
    clear = r"C:\Users\seren\OneDrive\Documents\Business\upload\clear_history.py"
    subprocess.run(["python", clear])

            
    return response



if __name__ == '__main__':
    app.run(debug=True)
