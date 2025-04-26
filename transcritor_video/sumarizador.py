import re
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from openai import OpenAI


class YouTubeSummarizer:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, timeout=30, max_retries=5)
        self.model = "gpt-3.5-turbo-instruct"
        self.max_tokens = 3000
        self.temperature = 0.3

    def extract_video_id(self, url: str) -> str:
        patterns = [
            r"(?:v=|\/)([0-9A-Za-z_-]{11})",
            r"(?:be\/|shorts\/)([0-9A-Za-z_-]{11})",
            r"(?:embed\/)([0-9A-Za-z_-]{11})",
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError("URL Inválida")

    def get_transcript(self, video_id: str) -> str:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join([entry["text"] for entry in transcript])
        except (TranscriptsDisabled, NoTranscriptFound):
            raise Exception("Esse vídeo não tem uma transcrição")
        except Exception as e:
            raise Exception(f"Erro ao adquirir transcrição: {str(e)}")

    def truncate_text(self, text: str) -> str:
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(text)
        if len(tokens) > self.max_tokens:
            tokens = tokens[: self.max_tokens]
            truncated_text = encoding.decode(tokens)
            print(f"Transcrição truncado para {self.max_tokens} tokens.")
            return truncated_text
        return text

    def generate_summary(self, text: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é uma assistente que ajuda a fazer sumários de vídeos",
                    },
                    {
                        "role": "user",
                        "content": f"Resuma a transcrição deste vídeo de forma clara e concisa. Destaque os pontos principais e evite detalhes desnecessários:\n\n{text}",
                    },
                ],
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating summary: {str(e)}")
