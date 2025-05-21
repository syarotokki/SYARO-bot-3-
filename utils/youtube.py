import requests
import os

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

def fetch_past_videos(channel_id, max_results=500):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    videos = []
    page_token = None
    total_fetched = 0

    while True:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 50,
            "order": "date",
            "type": "video",
            "key": YOUTUBE_API_KEY
        }
        if page_token:
            params["pageToken"] = page_token

        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            break

        data = response.json()
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_url)
            total_fetched += 1
            if total_fetched >= max_results:
                return videos

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return videos
