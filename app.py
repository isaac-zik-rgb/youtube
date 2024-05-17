# from flask import Flask, request, jsonify, send_from_directory
# from pytube import YouTube
# from flask_cors import CORS
# from urllib.parse import quote
# import os



# app = Flask(__name__)

# CORS(app)

# @app.route('/get', methods=['GET'])
# def get():
#     return jsonify({'success': True, 'message': 'Hello World!'})

# @app.route('/download-youtube-video', methods=['POST'])
# def download_youtube_video():
#     # Get the video ID from the request
#     video_id = request.json.get('video_id')
    
#     # Call the youtube_video_id function
#     try:
#         encoded_file_name = youtube_video_id(video_id)
#         directory = "YoutubeVideos"
#         file_path = os.path.join(directory, encoded_file_name + '.mp4')
        
#         return send_from_directory(directory, encoded_file_name + '.mp4', as_attachment=True)
#     except Exception as e:
#         return jsonify({'success': False, 'message': str(e)})








# def youtube_video_id(video_id):
#     """A function that takes in video id and downloads the video"""
#     # Extract the video ID
#     videoId = video_id[0]
#     print(videoId)
#     # Create a YouTube object and print the video link
#     yt_video = YouTube(f'https://www.youtube.com/watch?v={videoId}')
#     print(f"Video Link: {yt_video.watch_url}")
    
#     # Download the video
#     downloaded_file_path = yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("C:\\Users\\Chima\\Videos\\YoutubeVideos")
    
#     # Get the video title and URL-encode it
#     file_name = yt_video.title
#     encoded_file_name = quote(file_name)
    
#     # Construct the new file path with the encoded filename
#     new_file_path = os.path.join("YoutubeVideos", encoded_file_name + '.mp4')
    
#     # Rename the downloaded file to the encoded filename
#     os.rename(downloaded_file_path, new_file_path)
    
#     print(f"Downloaded video renamed to: {new_file_path}")
    
#     # Return the encoded filename
#     return encoded_file_name

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
from flask_cors import CORS
from urllib.parse import quote
import os
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)
CORS(app)

# Configure your S3 bucket and AWS region
S3_BUCKET = 'cythianbucket'
S3_REGION = 'US West (Oregon) us-west-2'

# Initialize the S3 client
s3_client = boto3.client('s3')

# Get video directory from environment variable or use a default value
VIDEO_DIR = "~/YoutubeVideos"

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/download-youtube-video', methods=['POST'])
def download_youtube_video():
    video_id = request.json.get('video_id')
    
    try:
        # Ensure the video directory exists
        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)
        
        # encoded_file_name = youtube_video_id(video_id)
        # file_path = os.path.join(VIDEO_DIR, encoded_file_name + '.mp4')
        
        # Upload the file to S3
        # s3_url = upload_to_s3(file_path, encoded_file_name + '.mp4')
        
        # # Return the S3 URL
        # return jsonify({'success': True, 'url': s3_url})

        encoded_file_name = youtube_video_id(video_id)
        
        file_path = os.path.join(VIDEO_DIR, encoded_file_name + '.mp4')
        
        return send_from_directory(VIDEO_DIR, encoded_file_name + '.mp4', as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def youtube_video_id(video_id):
    videoId = video_id[0]
    yt_video = YouTube(f'https://www.youtube.com/watch?v={videoId}')
    
    downloaded_file_path = yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(VIDEO_DIR)
    
    file_name = yt_video.title
    encoded_file_name = quote(file_name)
    new_file_path = os.path.join(VIDEO_DIR, encoded_file_name + '.mp4')
    
    os.rename(downloaded_file_path, new_file_path)
    
    return encoded_file_name

# def upload_to_s3(file_path, file_name):
#     try:
#         s3_client.upload_file(file_path, S3_BUCKET, file_name)
#         s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
#         return s3_url
#     except FileNotFoundError:
#         raise Exception("The file was not found")
#     except NoCredentialsError:
#         raise Exception("Credentials not available")

if __name__ == '__main__':
    app.run(debug=True)
