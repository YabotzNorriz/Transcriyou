from transcritor_video.conversor import MarkdownConverter
from transcritor_video.sumarizador import VideoSummarizer


def main():
    transcritor = VideoSummarizer()
    md_file = transcritor.run()

    if md_file:
        while True:
            converter = input("Deseja converter o arquivo para PDF? ([S]im ou [N]ão)")
            if converter.lower() == "s" or "sim":
                pdf_file = md_file.replace(".md", ".pdf")
                converter = MarkdownConverter(md_file, pdf_file)
                converter.convert()
                break
            elif converter.lower() == "n" or "não" or "nao":
                print("finalizando programa...")
                break
            else:
                print("Digite uma opção válida!")
    else:
        print("Error ")


if __name__ == "__main__":
    main()
