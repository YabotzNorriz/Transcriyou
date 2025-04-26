import os
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
import whisper
from transformers import pipeline, AutoTokenizer


# import subprocess

os.environ["PATH"] += os.pathsep + "C:\\ffmpeg\\bin"

# def encontrar_ffmpeg():
#     try:
#         resultado = subprocess.check_output(
#             ["where", "ffmpeg"], stderr=subprocess.STDOUT, text=True
#         ).strip()
#         print(f"Caminho ffmpeg: {resultado}")
#         return resultado.split("\n")[0]

#     except subprocess.CalledProcessError:
#         locais_comuns = [
#             os.path.join(os.environ["SYSTEMDRIVE"], "ffmpeg", "bin", "ffmpeg.exe"),
#             os.path.join(os.environ["PROGRAMFILES"], "ffmpeg", "bin", "ffmpeg.exe"),
#             os.path.join(os.environ["USERPROFILE"], "ffmpeg", "bin", "ffmpeg.exe"),
#         ]

#         for caminho in locais_comuns:
#             if os.path.exists(caminho):
#                 print(f"Caminho ffmpeg: {caminho}")
#                 return caminho
#             else:
#                 print(f"Caminho ffmpeg: {caminho}")

#         return "FFmpeg não encontrado no sistema"


def download_youtube_audio(url, ffmpeg_path="C:\\ffmpeg\\bin\\ffmpeg.exe"):
    config = {
        "ffmpeg_location": str(ffmpeg_path),
        "outtmpl": "audio",
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "16000",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(config) as ydl:
            info = ydl.extract_info(url, download=True)
            return Path("audio.wav").absolute()
    except Exception as e:
        print(f"Erro no download: {str(e)}")
        return None


def transcrever_audio(audio_path):
    try:
        model = whisper.load_model("base", device="cpu")
        result = model.transcribe(str(audio_path))
        return result["text"]
    except Exception as e:
        print(f"Erro na transcrição: {str(e)}")
        return None


def resumir_texto(texto, max_length=200):
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model_name, tokenizer=model_name)

    chunk_size = 1000
    chunks = [texto[i : i + chunk_size] for i in range(0, len(texto), chunk_size)]

    resumos = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024)
        if len(inputs["input_ids"][0]) > 1024:
            continue

        output = summarizer(
            chunk,
            max_length=max_length,
            min_length=max_length // 4,
            num_beams=4,
            repetition_penalty=2.0,
        )
        resumos.append(output[0]["summary_text"])

    return "\n".join(resumos)


def main(url):
    print("Baixando o áudio")
    audio_path = download_youtube_audio(url)

    print("Transcrevendo o áudio")
    transcricao = transcrever_audio(audio_path)

    print("Resumindo o áudio")
    resumo = resumir_texto(transcricao)

    os.remove(audio_path)

    return resumo


url_youtube = "https://youtu.be/l3MEXQqIBAQ?si=uqma99rVAEQ8f2aN"
resultado = main(url_youtube)
print("Resumo do vídeo:")
print(resultado)
