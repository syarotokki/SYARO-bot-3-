import os
import requests

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_latest_video(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&order=date&part=snippet&type=video&maxResults=1"
    res = requests.get(url).json()
    if "items" in res and len(res["items"]) > 0:
        video_id = res["items"][0]["id"]["videoId"]
        return f"https://www.youtube.com/watch?v={video_id}"
    return None

def fetch_past_videos(channel_id, max_results=5):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&order=date&part=snippet&type=video&maxResults={max_results}"
    res = requests.get(url).json()
    videos = []
    for item in res.get("items", []):
        video_id = item["id"]["videoId"]
        videos.append(f"https://www.youtube.com/watch?v={video_id}")
    return videos