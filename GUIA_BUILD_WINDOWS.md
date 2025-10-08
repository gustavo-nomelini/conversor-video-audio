# Guia de Build para Windows - Conversor de Vídeo/Áudio

## 🎯 Resumo
Este guia ajuda você a criar um executável Windows (.exe) independente do Conversor de Vídeo/Áudio.

## 📋 Pré-requisitos
- ✅ Windows 10/11
- ✅ Python 3.8 ou superior
- ✅ Conexão com internet (para downloads)

## 🚀 Opções de Build

### Opção 1: Script Automático Simples (RECOMENDADO)
```bash
python build_simple.py
```

### Opção 2: Script Melhorado com Ambiente Virtual
```bash
build_improved.bat
```

### Opção 3: Comando Manual
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Gerar executável
pyinstaller --name ConversorVideoAudio --onefile --windowed --clean --noconfirm main.py
```

## 📁 Arquivos Gerados
Após o build bem-sucedido, você encontrará:
- `dist/ConversorVideoAudio.exe` - Executável principal
- `dist/ConversorVideoAudio_debug.exe` - Versão debug (se necessário)

## ⚙️ Configurações Importantes

### FFmpeg (OBRIGATÓRIO para funcionar)
O executável precisa do FFmpeg para converter vídeos. Duas opções:

**Opção A: Instalar FFmpeg no Sistema**
1. Baixe FFmpeg: https://ffmpeg.org/download.html
2. Extraia e adicione ao PATH do Windows
3. Teste: `ffmpeg -version` no CMD

**Opção B: Incluir FFmpeg com o Executável**
1. Baixe `ffmpeg.exe`
2. Coloque na mesma pasta que `ConversorVideoAudio.exe`

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
- Instale Python 3.8+ de https://www.python.org/
- Marque "Add Python to PATH" durante instalação

### Erro: "Conflito de dependências"
- Execute: `pip install --upgrade pip`
- Use requirements.txt corrigido

### Erro: "PyInstaller falhou"
- Use a versão debug: arquivo `ConversorVideoAudio_debug.exe`
- Execute no terminal para ver erros específicos

### Executável não abre
- Verifique se FFmpeg está disponível
- Execute versão debug para ver erros
- Verifique antivírus (pode bloquear)

## 📦 Distribuição
Para distribuir seu executável:

1. **Arquivos necessários:**
   - `ConversorVideoAudio.exe`
   - `ffmpeg.exe` (opcional, se não instalado no sistema)
   - `README_WINDOWS.md` (instruções)

2. **Teste antes de distribuir:**
   - Execute em máquina limpa (sem Python)
   - Teste download de vídeo
   - Verifique conversão de áudio

## 📊 Tamanho Esperado
- Executável: ~150-250 MB
- Com todas dependências incluídas

## ⚡ Dicas de Performance
- Use SSD para build mais rápido
- Feche outros programas durante build
- Build pode levar 5-15 minutos

## 🆘 Suporte
Se encontrar problemas:
1. Verifique este guia primeiro
2. Execute versão debug
3. Copie mensagens de erro completas
4. Verifique versões de Python e pip

---
**Última atualização:** Outubro 2025
