import yt_dlp
import requests
import json

video_url = "https://youtu.be/ldYLYRNaucM?feature=shared"

ydl_opts = {
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(video_url,download=False)
    subtitles = info.get("automatic_captions", {})

if 'en' in subtitles:
    subtitle_url = subtitles['en'][0]['url']
    response = requests.get(subtitle_url)
    subtitle_content = response.text
else:
    print("Subtitles not available in English.")

subtitle_data = json.loads(subtitle_content)

def extract_subtitle_text(subtitle_data):
    parsed_text = ""

    for event in subtitle_data.get("events", []):
        for seg in event.get("segs", []):
            text = seg.get("utf8", "")

            if text.strip():
                parsed_text += text + " "

    return parsed_text.strip()

parsed_subtitle_text = extract_subtitle_text(subtitle_data)

print(parsed_subtitle_text)

def split_into_chunks(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

chunks = split_into_chunks(parsed_subtitle_text, chunk_size=50, overlap=10)
