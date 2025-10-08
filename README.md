# 🎬 YouTube Downloader - MP4 & MP3

Uma aplicação desktop com interface gráfica intuitiva para baixar vídeos do YouTube em formato MP4 ou extrair apenas o áudio em MP3.

## 📋 Funcionalidades

- ✅ Interface gráfica amigável (sem necessidade de usar o terminal)
- ✅ Download de vídeos em formato MP4 (melhor qualidade disponível)
- ✅ Extração de áudio em formato MP3 (192kbps)
- ✅ Barra de progresso em tempo real
- ✅ Log de atividades detalhado
- ✅ Seleção de pasta de destino
- ✅ Suporta todos os vídeos do YouTube

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**
- **PyQt6** - Framework para interface gráfica
- **yt-dlp** - Biblioteca para download de vídeos do YouTube

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/gustavo-nomelini/conversor-video-audio.git
cd conversor-video-audio
```

### 2. Crie um ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Instale o FFmpeg (necessário para conversão de áudio)

**macOS:**

```bash
brew install ffmpeg
```

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**

- Baixe o FFmpeg em: https://ffmpeg.org/download.html
- Adicione ao PATH do sistema

## 🚀 Como Usar

### Execute a aplicação:

```bash
python main.py
```

### Passos na interface:

1. **Cole a URL do vídeo do YouTube** no campo de entrada
2. **Selecione a pasta de destino** (padrão: Downloads)
3. **Escolha o formato**:
   - 🎥 **Vídeo MP4** - Baixa o vídeo completo
   - 🎵 **Áudio MP3** - Extrai apenas o áudio
4. **Clique em "Iniciar Download"**
5. **Acompanhe o progresso** na barra e no log

## 📸 Screenshots

A interface possui:

- Campo para URL do YouTube
- Seletor de pasta de destino
- Opções de formato (MP4 ou MP3)
- Barra de progresso
- Log de atividades em tempo real

## ⚙️ Requisitos do Sistema

- Python 3.8 ou superior
- FFmpeg instalado no sistema
- Conexão com a internet
- Espaço em disco suficiente para os downloads

## 🔧 Estrutura do Projeto

```
conversor-video-audio/
├── main.py              # Aplicação principal com GUI
├── requirements.txt     # Dependências do projeto
├── README.md           # Este arquivo
└── .gitignore          # Arquivos ignorados pelo git
```

## 📝 Notas Importantes

- **FFmpeg é obrigatório** para extração de áudio em MP3
- Os downloads são salvos com o título original do vídeo
- A qualidade do vídeo MP4 é a melhor disponível
- O áudio MP3 é extraído em 192kbps de qualidade

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🙏 Agradecimentos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Pela excelente biblioteca de download
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Pelo framework de GUI
- [FFmpeg](https://ffmpeg.org/) - Pela ferramenta de conversão de mídia

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Desenvolvido com ❤️ usando Python, PyQt6 e yt-dlp**
