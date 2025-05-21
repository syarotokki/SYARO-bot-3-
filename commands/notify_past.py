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

    # 重複排除 & 新しい順のまま返す
    return list(dict.fromkeys(videos))
