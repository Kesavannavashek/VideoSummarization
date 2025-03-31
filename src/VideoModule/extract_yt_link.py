import yt_dlp

def get_video_url(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info

video_info = get_video_url("https://youtu.be/ldYLYRNaucM?feature=shared")
video_url = video_info['url']
video_title = video_info['title']
