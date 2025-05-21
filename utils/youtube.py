import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_latest_video(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet&order=date&maxResults=1"
    response = requests.get(url)
    data = response.json()

    if "items" not in data or len(data["items"]) == 0:
        return None

    item = data["items"][0]
    video_id = item["id"].get("videoId")
    if not video_id:
        return None

    # 追加：動画の詳細取得
    details_url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={video_id}&part=snippet,liveStreamingDetails"
    details_resp = requests.get(details_url).json()
    video_data = details_resp.get("items", [{}])[0]

    is_live = "liveStreamingDetails" in video_data
    published_at = video_data.get("snippet", {}).get("publishedAt", "不明")

    return {
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "is_live": is_live,
        "published_at": published_at
    }
