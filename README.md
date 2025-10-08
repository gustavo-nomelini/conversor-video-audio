# 🎬 Conversor de Vídeo/Áudio - MP4 & MP3

Uma aplicação desktop com interface gráfica intuitiva para baixar vídeos do YouTube e Streamyard em formato MP4 ou extrair apenas o áudio em MP3.

## 📋 Funcionalidades

- ✅ Interface gráfica amigável (sem necessidade de usar o terminal)
- ✅ Download de vídeos em formato MP4 (melhor qualidade disponível)
- ✅ Extração de áudio em formato MP3 (192kbps)
- ✅ Barra de progresso em tempo real
- ✅ Log de atividades detalhado
- ✅ Seleção de pasta de destino
- ✅ Suporte para vídeos do YouTube
- ✅ Suporte para transmissões do Streamyard

## 🌐 Plataformas Suportadas

### YouTube

- Vídeos regulares: `https://www.youtube.com/watch?v=...`
- Vídeos curtos: `https://www.youtube.com/shorts/...`
- Links compartilhados: `https://youtu.be/...`

### Streamyard

✨ **EXTRAÇÃO AUTOMÁTICA DE VOD.MP4**: A aplicação detecta e baixa automaticamente!

Basta colar o link da página do Streamyard e o aplicativo:

1. Acessa a página automaticamente (em modo headless)
2. Captura as requisições de rede
3. Encontra o arquivo VOD.mp4
4. Inicia o download

**Exemplo de links suportados:**

- `https://streamyard.com/xzn8pctyeayj`
- `https://streamyard.com/watch/ABC123`

**Nenhuma configuração manual necessária!** 🎉

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

### 5. Instale o ChromeDriver (necessário para Streamyard)

A aplicação usa Selenium para extrair automaticamente os links do Streamyard. Você precisa ter o Chrome/Chromium instalado.

**macOS:**

```bash
brew install chromedriver
```

**Ubuntu/Debian:**

```bash
# Instalar Chrome se ainda não tiver
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Instalar ChromeDriver
sudo apt-get install chromium-chromedriver
```

**Windows:**

- O Selenium gerenciará automaticamente o ChromeDriver
- Certifique-se de ter o Google Chrome instalado

## 🚀 Como Usar

### Execute a aplicação:

```bash
python main.py
```

### Passos na interface:

1. **Cole a URL do vídeo** (YouTube ou Streamyard) no campo de entrada
2. **Selecione a pasta de destino** (padrão: Downloads)
3. **Escolha o formato**:
   - 🎥 **Vídeo MP4** - Baixa o vídeo completo
   - 🎵 **Áudio MP3** - Extrai apenas o áudio
4. **Clique em "Iniciar Download"**
5. **Acompanhe o progresso** na barra e no log

**Para Streamyard**: O app detecta automaticamente e extrai o link do stream - você só precisa colar o link da página!

## 📸 Screenshots

A interface possui:

- Campo para URL (YouTube ou Streamyard - extração automática)
- Seletor de pasta de destino
- Opções de formato (MP4 ou MP3)
- Barra de progresso
- Log de atividades em tempo real

## ✨ Funcionalidade Especial: Extração Automática do Streamyard

A aplicação possui um sistema inteligente que automatiza todo o processo:

### Como funciona:

1. **Você cola o link** do Streamyard (ex: `https://streamyard.com/xzn8pctyeayj`)
2. **O app detecta** automaticamente que é um link do Streamyard
3. **Selenium abre a página** em modo headless (invisível)
4. **Clica no play** automaticamente
5. **Captura as requisições** de rede usando Chrome DevTools Protocol
6. **Encontra o arquivo VOD.mp4** nas requisições
7. **Extrai o link direto** do vídeo
8. **Inicia o download** usando yt-dlp

### Vantagens:

- ✅ **Zero configuração manual** - Apenas cole o link!
- ✅ **Não precisa abrir DevTools** manualmente
- ✅ **Não precisa procurar arquivos** .mp4
- ✅ **Totalmente automático** - A aplicação faz tudo sozinha
- ✅ **Interface simples** - Mesma experiência para YouTube e Streamyard

**Você só precisa colar o link e esperar!** 🎉

## ⚙️ Requisitos do Sistema

- Python 3.8 ou superior
- FFmpeg instalado no sistema
- Google Chrome ou Chromium instalado (para Streamyard)
- ChromeDriver (instalado automaticamente pelo Selenium ou manualmente)
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
- [Selenium](https://www.selenium.dev/) - Pela automação web que permite extrair links do Streamyard

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Desenvolvido com 💛 para as escolas do Munícipio de Cascavel por Gustavo Lopes Nomelini**
