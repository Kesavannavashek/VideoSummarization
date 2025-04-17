import yt_dlp
import textwrap


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

video_info = get_video_url("https://youtu.be/HM_O0A4Xeb4?si=bDJwKzmIFFBzgJrV")
# print(video_info)
video_url = video_info['url']
video_title = video_info['title']
print(video_url)
# print("Video Title: ",video_title)
# # print("Video URL: ",video_url)
# video_url = textwrap.fill(video_url, width=70)
# print("Video URL: ",video_url)
