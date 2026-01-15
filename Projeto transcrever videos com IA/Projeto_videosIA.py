import os
from pytubefix import YouTube   # Para baixar o vídeo do YouTube
import whisper                  # Para transcrever o áudio localmente
from openai import OpenAI       # Para gerar o resumo com o GPT


# ENTRADA DE DADOS

video_url: str = input("Coloque o link do vídeo do YouTube: ")
print("Você digitou:", video_url)

# Verifica se o link é válido

if ("youtube.com" in video_url) or ("youtu.be" in video_url):
    print("Link válido!")
else:
    print("Link inválido!")
    exit(1)


# Download do áudio

print("Baixando o vídeo do YouTube...")
yt = YouTube(video_url)
stream = yt.streams.filter(only_audio=True).first()  # Baixa apenas o áudio
stream.download(filename="video.mp4") #Salva o arquivo do audio como video.mp4
print("Download concluído: video.mp4")


#Converter para MP3 (com FFmpeg)

print("🎧 Convertendo para MP3...")
comando_ffmpeg: str = f'ffmpeg -i "video.mp4" -q:a 0 -map a "audio.mp3" -y'
ret = os.system(comando_ffmpeg)
if ret != 0:
    print("Erro ao converter com FFmpeg.")
    exit(1)
print("Conversão concluída: audio.mp3")


#Transcrever o áudio com Whisper local

print("Transcrevendo o áudio com Whisper")
modelo = whisper.load_model("base")  # Opções: tiny, base, small, medium, large
resultado = modelo.transcribe("audio.mp3")

texto_transcrito: str = resultado["text"]
print("Transcrição concluída")

#Salva a transcrição do video em um arquivo

with open("transcricao.txt", "w", encoding="utf-8") as f:
    f.write(texto_transcrito)
print("Transcrição salva em 'transcricao.txt'.")


