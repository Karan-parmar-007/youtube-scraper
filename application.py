from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import logging
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)
application = app

@app.route("/", methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/results", methods=['POST', 'GET'])
@cross_origin()
def results():
    if request.method == 'POST':
        try:
            logging.info("post request")
            handle = request.form['content']
            api_key = request.form['api_key']
            try:
                video_details = get_channel_videos(api_key, handle)
                if video_details:
                    return render_template("result.html", reviews=video_details)
                else:
                    print("No videos found or error retrieving videos.")
                    return render_template("index.html", error="No videos found or error retrieving videos.")
            except HttpError as e:
                print(f"An HTTP error occurred: {e}")
                return render_template("index.html", error=f"An HTTP error occurred: {e}")
        except Exception as e:
            logging.info(f"Error in post request: {e}")
            return render_template("index.html", error=f"Error: {e}")

def get_channel_id(api_key, handle):
    youtube = build('youtube', 'v3', developerKey=api_key)
    try:
        search_response = youtube.search().list(
            q=handle,
            part='snippet',
            type='channel',
            maxResults=1
        ).execute()
        
        if not search_response.get('items'):
            print(f"No channel found for handle: {handle}")
            return None
        
        channel_id = search_response['items'][0]['snippet']['channelId']
        return channel_id
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None

def get_channel_videos(api_key, handle):
    channel_id = get_channel_id(api_key, handle)
    if not channel_id:
        return []

    youtube = build('youtube', 'v3', developerKey=api_key)
    
    uploads_playlist_id = youtube.channels().list(
        id=channel_id,
        part='contentDetails'
    ).execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    video_details = []
    next_page_token = None
    videos_fetched = 0
    max_videos = 5

    while True:
        playlist_response = youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=min(50, max_videos - videos_fetched),
            pageToken=next_page_token
        ).execute()
        
        for item in playlist_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            video_published_at = item['snippet']['publishedAt']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            
            video_response = youtube.videos().list(
                id=video_id,
                part='statistics'
            ).execute()
            
            video_views = video_response['items'][0]['statistics'].get('viewCount', 'N/A')
            video_likes = video_response['items'][0]['statistics'].get('likeCount', 'N/A')
            
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            
            video_details.append({
                'URL': video_url,
                'Thumbnail URL': thumbnail_url,
                'Views': video_views,
                'Likes': video_likes,
                'Time Posted': video_published_at,
                'Title': video_title
            })
            videos_fetched += 1
            if videos_fetched >= max_videos:
                return video_details

        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    return video_details

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
