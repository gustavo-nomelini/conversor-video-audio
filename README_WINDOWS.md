# 🎬 Conversor de Vídeo/Áudio - Versão Windows

## 📦 Executável Standalone para Windows

Este é um executável único que **não requer instalação do Python** no Windows!

## 🚀 Download e Instalação

### Pré-requisitos

**IMPORTANTE:** Você precisa ter o FFmpeg instalado:

1. **Baixe o FFmpeg:**
   - Acesse: https://ffmpeg.org/download.html
   - Ou use o link direto: https://github.com/BtbN/FFmpeg-Builds/releases

2. **Instale o FFmpeg:**
   - Extraia o arquivo ZIP baixado
   - Copie a pasta para `C:\FFmpeg`
   - **Adicione ao PATH do Windows:**
     1. Abra "Editar as variáveis de ambiente do sistema"
     2. Clique em "Variáveis de Ambiente"
     3. Em "Variáveis do sistema", encontre "Path"
     4. Clique em "Editar"
     5. Clique em "Novo"
     6. Adicione: `C:\FFmpeg\bin`
     7. Clique em "OK" em todas as janelas

3. **Verifique a instalação:**
   ```cmd
   ffmpeg -version
   ```

### Executar a Aplicação

1. **Baixe o executável:** `ConversorVideoAudio.exe`
2. **Duplo clique no arquivo** para executar
3. **Pronto!** A aplicação abrirá automaticamente

## ✨ Funcionalidades

- ✅ Interface gráfica moderna com tema escuro
- ✅ Download de vídeos do YouTube em MP4
- ✅ Extração de áudio em MP3
- ✅ Suporte para Streamyard (extração automática)
- ✅ Nome de arquivo personalizável
- ✅ Análise prévia do vídeo
- ✅ Barra de progresso em tempo real
- ✅ **Não requer Python instalado!**

## 🎯 Como Usar

1. **Abra o aplicativo** (duplo clique no .exe)

2. **Cole a URL do vídeo:**
   - YouTube: `https://www.youtube.com/watch?v=...`
   - Streamyard: `https://streamyard.com/watch/...`

3. **Clique em "🔍 Analisar Vídeo"**
   - Veja informações do vídeo
   - Personalize o nome do arquivo (opcional)

4. **Escolha o formato:**
   - 🎥 Vídeo MP4 (completo)
   - 🎵 Áudio MP3 (apenas áudio)

5. **Clique em "⬇️ Iniciar Download"**

6. **Aguarde a conclusão!**
   - Acompanhe o progresso
   - Arquivo salvo na pasta Downloads

## 🔧 Solução de Problemas

### "FFmpeg não encontrado"

**Solução:** Instale o FFmpeg seguindo as instruções acima.

### "Erro ao extrair URL do Streamyard"

**Possíveis causas:**
- Vídeo não está mais disponível
- Problemas de conexão
- Chrome/Chromium não instalado

**Solução:** 
- Verifique se o Google Chrome está instalado
- Teste se o vídeo abre no navegador
- Tente novamente em alguns minutos

### Executável não abre

**Soluções:**
1. **Antivírus bloqueando:**
   - Adicione o .exe à lista de exceções do antivírus
   - Executáveis PyInstaller às vezes são marcados como suspeitos

2. **Windows SmartScreen:**
   - Clique em "Mais informações"
   - Clique em "Executar assim mesmo"

3. **Falta de permissões:**
   - Clique com botão direito no .exe
   - "Executar como administrador"

### Erro de DLL faltando

**Solução:**
- Instale o Visual C++ Redistributable:
  - https://aka.ms/vs/17/release/vc_redist.x64.exe

## 📋 Informações Técnicas

- **Tamanho do executável:** ~100-150 MB
- **Plataforma:** Windows 10/11 (64-bit)
- **Tecnologias:** PyQt6, yt-dlp, Selenium
- **FFmpeg:** Requerido para conversão MP3

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se o FFmpeg está instalado corretamente
2. Teste sua conexão com a internet
3. Verifique se o antivírus não está bloqueando
4. Abra uma issue no GitHub: https://github.com/gustavo-nomelini/conversor-video-audio

## 📄 Licença

MIT License - Uso livre e gratuito

## 👨‍💻 Desenvolvedor

**Gustavo Nomelini**
- GitHub: https://github.com/gustavo-nomelini
- Projeto: https://github.com/gustavo-nomelini/conversor-video-audio

---

**Desenvolvido com ❤️ usando Python, PyQt6 e yt-dlp**
