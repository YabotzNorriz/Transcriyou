import os
from getpass import getpass
from transcritor_video import sumarizador


def main():
    api_key = os.getenv("") or getpass("Enter your OpenAI API key: ")

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
