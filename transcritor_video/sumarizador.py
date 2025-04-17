import re
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline


class VideoSummarizer:
    def __init__(self):

        self.url = None
        self.output = None
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def ask_user_input(self):

        self.url = input("Digite a URL do vídeo no YouTube: ").strip()
        output_file = input(
            "Digite o nome do arquivo de saída (pressione Enter para usar 'resumo.md'): "
        ).strip()
        self.output = output_file if output_file else "resumo.md"

    def extract_video_id(self) -> str:

        regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search(regex, self.url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Não foi possível extrair o ID do vídeo a partir da URL.")

    def get_transcript(self, video_id: str):

        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["pt", "en"]
        )
        return transcript

    def summarize_text(self, text: str) -> str:
        words = text.split()
        chunk_size = 500
        chunks = [
            " ".join(words[i : i + chunk_size])
            for i in range(0, len(words), chunk_size)
        ]

        summary_chunks = []
        for chunk in chunks:
            summary = self.summarizer(
                chunk, max_length=200, min_length=50, do_sample=False
            )
            summary_chunks.append(summary[0]["summary_text"])

        combined_summary = "\n\n".join(summary_chunks)
        return combined_summary

    def write_output(self, content: str):
        with open(self.output, "w", encoding="utf-8") as file:
            file.write(content)

    def run(self):
        try:
            self.ask_user_input()
            video_id = self.extract_video_id()
            transcript_segments = self.get_transcript(video_id)
            full_text = " ".join([segment["text"] for segment in transcript_segments])

            print("Gerando resumo, por favor aguarde...")
            summary = self.summarize_text(full_text)

            markdown_content = f"# Resumo do Vídeo\n\n{summary}\n"
            self.write_output(markdown_content)

            print(f"Resumo salvo no arquivo '{self.output}'")
        except Exception as e:
            print("Erro:", e)
