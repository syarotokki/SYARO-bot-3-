import requests
import os
from datetime import datetime

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_latest_video(channel_id):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 1,
        "order": "date",
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    search_res = requests.get(search_url, params=search_params)
    items = search_res.json().get("items")

    if not items:
        return None

    video = items[0]
    video_id = video["id"]["videoId"]
    title = video["snippet"]["title"]

    # 詳細情報を取得（ライブ配信かどうかを判定）
    video_url = f"https://www.googleapis.com/youtube/v3/videos"
    video_params = {
        "part": "snippet,liveStreamingDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY
    }

    video_res = requests.get(video_url, params=video_params).json()
    video_items = video_res.get("items")

    if not video_items:
        return None

    video_data = video_items[0]
    live_details = video_data.get("liveStreamingDetails")

    if live_details and "actualStartTime" in live_details:
        # ライブ配信
        start_time = datetime.fromisoformat(live_details["actualStartTime"].replace("Z", "+00:00"))
        formatted_time = start_time.strftime("%Y/%m/%d %H:%M:%S")
        return f"🔴 ライブ配信が始まりました！\n**{title}**\n開始時刻: {formatted_time}\nhttps://youtu.be/{video_id}"
    else:
        # 通常動画
        return f"📹 新しい動画が投稿されました！\n**{title}**\nhttps://youtu.be/{video_id}"


def fetch_past_videos(channel_id):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 50,
        "order": "date",
        "type": "video",
        "key": YOUTUBE_API_KEY
    }

    search_res = requests.get(search_url, params=search_params)
    items = search_res.json().get("items")

    if not items:
        return []

    videos = []
    for item in items:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]

        # ライブ配信かどうかを確認
        video_url = "https://www.googleapis.com/youtube/v3/videos"
        video_params = {
            "part": "liveStreamingDetails",
            "id": video_id,
            "key": YOUTUBE_API_KEY
        }

        video_res = requests.get(video_url, params=video_params).json()
        video_items = video_res.get("items")

        # ライブ配信は除外、通常動画のみ通知
        if video_items and not video_items[0].get("liveStreamingDetails"):
            videos.append(f"📹 {title}\nhttps://youtu.be/{video_id}")

    return videos
