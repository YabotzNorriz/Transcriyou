import os
from getpass import getpass
from transcritor_video import sumarizador


def read_api_key(file_path="api_key.txt"):
    try:
        with open(file_path, "r") as file:
            key = file.readline().strip()
            if key.startswith("sk-") and len(key) > 40:
                return key
            raise ValueError("API Key inválida")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Arquivo com a API não foi encontrado no caminho {file_path}"
        )
    except Exception as e:
        raise RuntimeError(f"Erro lendo aAPI key: {str(e)}")


def main():
    api_key = read_api_key() or getpass("Enter your OpenAI API key: ")

    summarizer = sumarizador.YouTubeSummarizer(api_key)

    url = input("Enter YouTube video URL: ")

    try:
        video_id = summarizer.extract_video_id(url)
        transcript = summarizer.get_transcript(video_id)
        print(f"Retrieved transcript with {len(transcript)} characters.")

        processed_text = summarizer.truncate_text(transcript)
        summary = summarizer.generate_summary(processed_text)

        print("\n--- Sumário ---")
        print(summary)

    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
