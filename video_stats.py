import requests
import json 
from datetime import date

import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "ion_lab"
max_results = 50


def get_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        # print(json.dumps(data, indent=4))

        channel_items = data['items'][0]
        channel_playlistid = channel_items['contentDetails']['relatedPlaylists']['uploads']

        return channel_playlistid
    
    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlist_id):

    video_ids = []
    page_token = None 

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"

    try:

        while True:
            url = base_url

            if page_token:
                url += f"&pageToken={page_token}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)
            
            page_token = data.get('nextPageToken')

            if not page_token:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_ids, batch_size):
        
        print("Defining batches...")

        for video_id in range(0,len(video_ids),batch_size):
            yield video_ids[video_id: video_id + batch_size]

        # print(batch_list(video_ids, max_results))
    
    try:
        for batch in batch_list(video_ids, max_results):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails%2C%20snippet%2Cstatistics&id={video_ids_str}&key={API_KEY}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'published_at': snippet['publishedAt'],
                    'duration': contentDetails['duration'],
                    'view_count': statistics.get('viewCount', None),
                    'like_count': statistics.get('likeCount', None),
                    'comment_count': statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)
                print(extracted_data)
        
        return extracted_data
    

    except requests.exceptions.RequestException as e:
        raise e

def load_to_json(extracted_data):
    file_path = f"./_data/YT_data_{date.today()}.json"
    

    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4,ensure_ascii=False)



if __name__ == "__main__":
    print("Defining playlist_id...")

    playlist_id=get_playlist_id()
    print(f"playlistid: {playlist_id}")

    print("Defining video_ids...")

    video_ids = get_video_ids(playlist_id)
    print(f"Total number of videos: {len(video_ids)}")

    print("Extracting data...")
    video_data = extract_video_data(video_ids)

    print("Loading data...")
    load_to_json(video_data)

    print("Done!")

        