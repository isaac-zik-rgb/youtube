from flask import Flask, request, jsonify, send_from_directory
from pytube import YouTube
from flask_cors import CORS
from urllib.parse import quote
import os



app = Flask(__name__)

CORS(app)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'


@app.route('/download-youtube-video', methods=['POST'])
def download_youtube_video():
    # Get the video ID from the request
    video_id = request.json.get('video_id')
    
    # Call the youtube_video_id function
    try:
        encoded_file_name = youtube_video_id(video_id)
        directory = "YoutubeVideos"
        file_path = os.path.join(directory, encoded_file_name + '.mp4')
        
        return send_from_directory(directory, encoded_file_name + '.mp4', as_attachment=True)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})








def youtube_video_id(video_id):
    """A function that takes in video id and downloads the video"""
    # Extract the video ID
    videoId = video_id[0]
    print(videoId)
    # Create a YouTube object and print the video link
    yt_video = YouTube(f'https://www.youtube.com/watch?v={videoId}')
    print(f"Video Link: {yt_video.watch_url}")
    
    # Download the video
    downloaded_file_path = yt_video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("C:\\Users\\Chima\\Videos\\YoutubeVideos")
    
    # Get the video title and URL-encode it
    file_name = yt_video.title
    encoded_file_name = quote(file_name)
    
    # Construct the new file path with the encoded filename
    new_file_path = os.path.join("YoutubeVideos", encoded_file_name + '.mp4')
    
    # Rename the downloaded file to the encoded filename
    os.rename(downloaded_file_path, new_file_path)
    
    print(f"Downloaded video renamed to: {new_file_path}")
    
    # Return the encoded filename
    return encoded_file_name

if __name__ == '__main__':
    app.run(debug=True, port=8080)
