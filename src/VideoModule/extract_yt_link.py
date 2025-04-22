# import yt_dlp
# import textwrap
#
#
# def get_video_url(youtube_url):
#     ydl_opts = {
#         'format': 'best',
#         'quiet': True,
#         'noplaylist': True,
#         'extract_flat': False,
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=False)
#         return info
#
# video_info = get_video_url("https://youtu.be/ldYLYRNaucM?si=ximNENy042FR06sR")
# # print(video_info)
# video_url = video_info['url']
# video_title = video_info['title']
# print(video_url)
# # print("Video Title: ",video_title)
# # # print("Video URL: ",video_url)
# # video_url = textwrap.fill(video_url, width=70)
# # print("Video URL: ",video_url)


import yt_dlp
import requests
import json


# def get_video_info_with_subs(youtube_url):
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#         'writesubtitles': True,
#         'writeautomaticsub': True,
#         'subtitleslangs': ['en'],
#         'subtitlesformat': 'json3',
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=False)
#         subtitles = info.get('subtitles', {}) or info.get('automatic_captions', {})
#         if subtitles and 'en' in subtitles:
#             subtitle_url = subtitles['en'][0]['url']
#             return info['title'], subtitle_url
#         return info['title'], None
#
#
# def convert_ms_to_time_format(ms):
#     minutes = ms // 60000
#     seconds = (ms % 60000) // 1000
#     milliseconds = ms % 1000
#     return f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
#
#
# def process_subtitles_grouped(subtitle_url, max_gap_ms=1000, max_duration_ms=10000):
#     try:
#         response = requests.get(subtitle_url)
#         response.raise_for_status()
#         subtitle_data = response.json()
#     except Exception as e:
#         print(f"Subtitle error: {e}")
#         return []
#
#     results = []
#     group = []
#     start_time = None
#     end_time = None
#
#     for event in subtitle_data.get('events', []):
#         if not event.get('segs') or not event.get('tStartMs'):
#             continue
#
#         t_start = event['tStartMs']
#         duration = event.get('dDurationMs', 1000)
#         t_end = t_start + duration
#
#         text = ' '.join(seg.get('utf8', '').strip() for seg in event['segs'] if seg.get('utf8')).strip()
#         if not text:
#             continue
#
#         if start_time is None:
#             start_time = t_start
#             end_time = t_end
#             group.append(text)
#         elif (t_start - end_time <= max_gap_ms) and ((t_end - start_time) <= max_duration_ms):
#             group.append(text)
#             end_time = t_end
#         else:
#             full_text = ' '.join(group)
#             results.append((convert_ms_to_time_format(start_time), convert_ms_to_time_format(end_time), full_text))
#             start_time = t_start
#             end_time = t_end
#             group = [text]
#
#     if group:
#         full_text = ' '.join(group)
#         results.append((convert_ms_to_time_format(start_time), convert_ms_to_time_format(end_time), full_text))
#
#     return results
#
#
# def main():
#     video_url = "https://youtu.be/ldYLYRNaucM?si=ximNENy042FR06sR"
#     video_title, subtitle_url = get_video_info_with_subs(video_url)
#
#     if subtitle_url:
#         print(f"\n🎬 Video Title: {video_title}\n")
#         print("📜 Subtitle Segments (max 10 sec each):\n")
#
#         results = process_subtitles_grouped(subtitle_url)
#         for start, end, text in results:
#             print(f"[{start},{end}] {text}")
#     else:
#         print("No subtitles found.")
#
#
# if __name__ == "__main__":
#     main()



# import yt_dlp
# import requests
# import json
# import yake
#
#
# def get_video_info_with_subs(youtube_url):
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#         'writesubtitles': True,
#         'writeautomaticsub': True,
#         'subtitleslangs': ['en'],
#         'subtitlesformat': 'json3',
#     }
#
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(youtube_url, download=False)
#         subtitles = info.get('subtitles', {}) or info.get('automatic_captions', {})
#         if subtitles and 'en' in subtitles:
#             subtitle_url = subtitles['en'][0]['url']
#             return info['title'], subtitle_url
#         return info['title'], None
#
#
# def convert_ms_to_time_format(ms):
#     minutes = ms // 60000
#     seconds = (ms % 60000) // 1000
#     milliseconds = ms % 1000
#     return f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
#
#
# def extract_keywords(text, max_keywords=3):
#     kw_extractor = yake.KeywordExtractor(top=max_keywords, stopwords=None)
#     keywords = kw_extractor.extract_keywords(text)
#     return [kw for kw, score in keywords]
#
#
# def process_subtitles_on_the_go(subtitle_url):
#     try:
#         response = requests.get(subtitle_url)
#         response.raise_for_status()
#     except requests.RequestException as e:
#         print(f"Failed to download subtitle file: {e}")
#         return []
#
#     try:
#         subtitle_data = response.json()
#     except json.JSONDecodeError as e:
#         print(f"Failed to decode JSON: {e}")
#         return []
#
#     timestamps_keywords = []
#
#     for event in subtitle_data.get('events', []):
#         if not event.get('segs') or not event.get('tStartMs'):
#             continue
#
#         timestamp = event.get('tStartMs')
#         text = ' '.join(seg.get('utf8', '').strip() for seg in event.get('segs', []) if seg.get('utf8', '').strip()).strip()
#
#         if timestamp is not None and text:
#             formatted_time = convert_ms_to_time_format(timestamp)
#             keywords = extract_keywords(text)
#             for kw in keywords:
#                 timestamps_keywords.append((formatted_time, kw))
#
#     return timestamps_keywords
#
#
# def main():
#     video_url = "https://youtu.be/ldYLYRNaucM?si=ximNENy042FR06sR"
#     video_title, subtitle_url = get_video_info_with_subs(video_url)
#
#     if subtitle_url:
#         print(f"\n🎬 Video Title: {video_title}\n")
#         print("🧠 Extracting keywords from subtitles...\n")
#
#         results = process_subtitles_on_the_go(subtitle_url)
#         if results:
#             for formatted_time, keyword in results:
#                 print(f"[{formatted_time}] {keyword}")
#         else:
#             print("No keywords found.")
#     else:
#         print("No subtitles found for the video.")
#
#
# if __name__ == "__main__":
#     main()


import yt_dlp
import requests
import json
import yake


def get_video_info_with_subs(youtube_url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'json3',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        direct_url = info.get('url')
        subtitles = info.get('subtitles', {}) or info.get('automatic_captions', {})
        if subtitles and 'en' in subtitles:
            subtitle_url = subtitles['en'][0]['url']
            return info['title'], subtitle_url, direct_url
        return info['title'],None , direct_url


def convert_ms_to_time_format(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    milliseconds = ms % 1000
    return f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"


def extract_keywords(text, max_keywords=3):
    kw_extractor = yake.KeywordExtractor(top=max_keywords, stopwords=None)
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]


def process_subtitles_grouped(subtitle_url, max_gap_ms=1000, max_duration_ms=10000):
    try:
        response = requests.get(subtitle_url)
        response.raise_for_status()
        subtitle_data = response.json()
    except Exception as e:
        print(f"Subtitle error: {e}")
        return []

    results = []
    group = []
    start_time = None
    end_time = None

    for event in subtitle_data.get('events', []):
        if not event.get('segs') or not event.get('tStartMs'):
            continue

        t_start = event['tStartMs']
        duration = event.get('dDurationMs', 1000)
        t_end = t_start + duration

        text = ' '.join(seg.get('utf8', '').strip() for seg in event['segs'] if seg.get('utf8')).strip()
        if not text:
            continue

        if start_time is None:
            start_time = t_start
            end_time = t_end
            group.append(text)
        elif (t_start - end_time <= max_gap_ms) and ((t_end - start_time) <= max_duration_ms):
            group.append(text)
            end_time = t_end
        else:
            full_text = ' '.join(group)
            keywords = extract_keywords(full_text)
            results.append((convert_ms_to_time_format(start_time), convert_ms_to_time_format(end_time), full_text, keywords))
            start_time = t_start
            end_time = t_end
            group = [text]

    if group:
        full_text = ' '.join(group)
        keywords = extract_keywords(full_text)
        results.append((convert_ms_to_time_format(start_time), convert_ms_to_time_format(end_time), full_text, keywords))

    return results


def main():
    video_url = "https://youtu.be/ldYLYRNaucM?si=ximNENy042FR06sR"
    video_title, subtitle_url ,direct_url = get_video_info_with_subs(video_url)

    if subtitle_url:
        print(f"\n🎬 Video Title: {video_title}\n")
        print("📜 Subtitle Segments with Keywords:\n")

        results = process_subtitles_grouped(subtitle_url)
        for start, end, text, keywords in results:
            print(f"[{start},{end}] {text}")
            print(f"   🔑 Keywords: {', '.join(keywords)}\n")
    else:
        print("No subtitles found.")


if __name__ == "__main__":
    main()
