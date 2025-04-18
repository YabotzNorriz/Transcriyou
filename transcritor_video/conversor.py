import pypandoc


class MarkdownConverter:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def convert(self):
        try:
            pypandoc.convert_file(self.input_file, "pdf", outputfile=self.output_file)
            print(f"PDF gerado com sucesso em '{self.output_file}'")
        except Exception as e:
            print("Erro na conversão:", e)
