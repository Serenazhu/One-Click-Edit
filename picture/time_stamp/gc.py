from google.cloud import speech_v1p1beta1 as speech
from pydub import AudioSegment
from google.cloud import storage

# Initialize the Speech client
client = speech.SpeechClient()

storage_client = storage.Client()
bucket_name = "audio1977"

# Configure the recognition settings with word-level time offsets
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code="en-US",
    enable_word_time_offsets=True,  # This enables word-level time stamps
)
#delete all before uploading
bucket_name = "audio1977"
bucket_d = storage_client.bucket(bucket_name)
b = bucket_d.list_blobs()

# Delete each object (file) in the bucket
for audio in b:
    audio.delete()

# Upload the mono audio WAV file to Google Cloud Storage
mono_audio_file_path = r"C:\Users\seren\OneDrive\Documents\Business\picture\time_stamp\mono.wav"
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob("mono.wav")
blob.upload_from_filename(mono_audio_file_path)

# Configure the audio input using GCS URI
audio_uri = f"gs://{bucket_name}/mono.wav"

# Create a LongRunningRecognizeRequest
long_running_request = speech.LongRunningRecognizeRequest(
    config=config, audio=speech.RecognitionAudio(uri=audio_uri)
)

# Start the asynchronous recognition
operation = client.long_running_recognize(request=long_running_request)

# Wait for the operation to complete
response = operation.result(timeout=90)  # Adjust the timeout as needed
# Open the text file for reading
path = r"C:\Users\seren\OneDrive\Documents\Business\picture\min_keywords.txt"
        # Read the keywords from the file
with open(path, 'r') as file:
    keywords = file.read()

# Remove unwanted characters
keywords = keywords.replace("[", "").replace("]", "").replace("'", "").replace(",", "")


# Split the text into individual words
words = keywords.split()

# Iterate through the words
for key in words:
    print(key.lower())


for result in response.results:
    for word_info in result.alternatives[0].words:
        start_time = word_info.start_time.total_seconds()
        end_time = word_info.end_time.total_seconds()
        word = word_info.word
        #print(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}")
        for key in words:
            if key.lower() == word:
                print(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}")
    
        
# Open the text file for writing
output_file_path = r"C:\Users\seren\OneDrive\Documents\Business\picture\keyword_with_timestamps.txt"
with open(output_file_path, "w") as output_file:
    # Process the API response
    for result in response.results:
        for word_info in result.alternatives[0].words:
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            word = word_info.word
            for key in words:
                if key.lower() == word:
                    # Write the word, start time, and end time to the output file
                    output_file.write(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}\n")
                    # Print the information to the console (optional)
                    #print(f"Word: {word}, Start Time: {start_time}, End Time: {end_time}")

# Close the output file
output_file.close()





