import yt_dlp
import torch
from transformers import pipeline
from pydub import AudioSegment

# Set the YouTube URL
youtube_url = "https://youtu.be/nz4j4lNHhkE?si=MYAN-HSGR_VSltCs"

# Define audio output filename
audio_filename = "audio.mp3"

# Download the audio using yt-dlp
ydl_opts = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": audio_filename,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([youtube_url])

# Convert audio to required format (if necessary)
audio = AudioSegment.from_file(audio_filename)
audio = audio.set_frame_rate(16000).set_channels(1)  # Ensure it's mono 16kHz
audio.export("processed_audio.wav", format="wav")

# Load Whisper model from Hugging Face
device = "cuda" if torch.cuda.is_available() else "cpu"
whisper_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-base", device=device)

# Transcribe the audio
result = whisper_pipeline("processed_audio.wav",return_timestamps=True)
transcription = result["text"]

print("Transcription:")
print(transcription)
