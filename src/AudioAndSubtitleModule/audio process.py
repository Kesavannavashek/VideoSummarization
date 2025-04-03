import yt_dlp
import torch
from transformers import pipeline
from pydub import AudioSegment
import textwrap


youtube_url = "https://youtu.be/oO8w6XcXJUs?si=duhKfePkQ8jHFhQA"


audio_filename = "audio.mp3"


ydl_opts = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": audio_filename,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_url])

audio = AudioSegment.from_file(audio_filename)
audio = audio.set_frame_rate(16000).set_channels(1)
audio.export("processed_audio.wav", format="wav")

device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=device)

result = whisper_pipeline("processed_audio.wav",return_timestamps=True)
transcription = result["text"]

print("Transcription:")
print(transcription)

formatted_text = textwrap.fill(transcription, width=50)
print("Transcription:\n")
print(formatted_text)