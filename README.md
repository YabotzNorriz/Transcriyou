# Transcritor e Resumidor de Vídeo do YouTube

Este projeto é um script em Python que permite extrair a transcrição de um vídeo do YouTube, resumir o conteúdo utilizando um modelo de *summarization* (neste caso, o `facebook/bart-large-cnn` da biblioteca Transformers) e salvar o resumo em um arquivo Markdown.

## Funcionalidades

- **Entrada interativa:** Solicita que o usuário informe a URL do vídeo do YouTube e o nome do arquivo para salvar o resumo.
- **Extração do ID do vídeo:** Utiliza expressões regulares para identificar o identificador único presente na URL.
- **Transcrição:** Obtém a transcrição do vídeo (caso as legendas estejam disponíveis) através da API [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api). São priorizadas as legendas em português, mas se não estiverem disponíveis, tenta em inglês.
- **Resumo:** Divide a transcrição em partes (chunks) para contornar limites do modelo e utiliza o modelo `facebook/bart-large-cnn` para gerar um resumo do conteúdo.
- **Saída em Markdown:** Salva o resumo final em um arquivo Markdown, com um título e formatação legível.

## Requisitos

- **Python 3**
- Bibliotecas Python:
  - `youtube-transcript-api`
  - `transformers`
  - `torch`

## Instalação

1. Clone o repositório ou copie os arquivos para uma pasta local de sua preferência.

2. Instale as dependências necessárias utilizando o `pip`:

   ```bash
   pip install youtube-transcript-api transformers torch
