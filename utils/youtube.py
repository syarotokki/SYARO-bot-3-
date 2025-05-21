import os
import requests

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

def fetch_latest_video(channel_id):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 1,
        "order": "date",
        "type": "video",
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" not in data or not data["items"]:
        return None

    item = data["items"][0]
    video_id = item["id"]["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return {
        "url": video_url,
        "title": item["snippet"]["title"],
        "publishedAt": item["snippet"]["publishedAt"],
        "is_live": item["snippet"].get("liveBroadcastContent") == "live"
    }

def fetch_past_videos(channel_id):
    videos = []
    next_page_token = None

    while True:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 50,
            "order": "date",
            "type": "video",
            "key": YOUTUBE_API_KEY,
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data:
            break

        for item in data["items"]:
            video_id = item["id"]["videoId"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append(video_url)

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    # 重複排除 & 昇順に（古い順に）
    return list(dict.fromkeys(videos[::-1]))
