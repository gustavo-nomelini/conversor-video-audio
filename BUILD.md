# 🔨 Guia de Build - Executável Windows

Este guia explica como gerar o arquivo executável (.exe) do Conversor de Vídeo/Áudio para Windows.

## 📋 Pré-requisitos

### No Windows (recomendado para gerar .exe Windows):

1. **Python 3.8 ou superior**
   - Download: https://www.python.org/downloads/
   - ⚠️ **IMPORTANTE:** Marque a opção "Add Python to PATH" durante instalação

2. **Git** (opcional, para clonar o repositório)
   - Download: https://git-scm.com/download/win

3. **Visual C++ Redistributable** (se não tiver)
   - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### No macOS/Linux (cross-compilation - mais complexo):

- Recomendamos gerar o .exe no Windows
- Para cross-compilation, use Wine + PyInstaller (avançado)

## 🚀 Método 1: Script Automático (Recomendado)

### No Windows:

1. **Clone ou baixe o repositório:**
   ```cmd
   git clone https://github.com/gustavo-nomelini/conversor-video-audio.git
   cd conversor-video-audio
   ```

2. **Execute o script de build:**
   ```cmd
   build_windows.bat
   ```

3. **Aguarde a conclusão** (pode levar 5-10 minutos)

4. **Executável gerado em:** `dist\ConversorVideoAudio.exe`

### Usando Python (cross-platform):

```bash
python build_exe.py
```

## 🔧 Método 2: Manual com PyInstaller

### Passo 1: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Limpe builds anteriores (opcional)

**Windows:**
```cmd
rmdir /s /q build dist
del ConversorVideoAudio.spec
```

**macOS/Linux:**
```bash
rm -rf build dist ConversorVideoAudio.spec
```

### Passo 3: Gere o executável

**Opção A - Usando arquivo .spec (recomendado):**

```bash
pyinstaller ConversorVideoAudio.spec
```

**Opção B - Linha de comando:**

```bash
pyinstaller --name ConversorVideoAudio --onefile --windowed --clean --noconfirm main.py
```

### Passo 4: Localize o executável

O arquivo `ConversorVideoAudio.exe` estará em:
```
dist/ConversorVideoAudio.exe
```

## 📦 Customização Avançada

### Adicionar Ícone Personalizado

1. **Crie ou baixe um ícone (.ico):**
   - Tamanho recomendado: 256x256 pixels
   - Formato: .ico (use https://convertio.co/png-ico/)

2. **Salve como:** `icon.ico` na raiz do projeto

3. **Edite o arquivo .spec:**
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # Adicione esta linha
       ...
   )
   ```

4. **Ou use linha de comando:**
   ```bash
   pyinstaller --icon=icon.ico --name ConversorVideoAudio --onefile --windowed main.py
   ```

### Incluir Arquivos Extras

Se precisar incluir arquivos adicionais (imagens, configs, etc):

**No arquivo .spec:**
```python
datas=[
    ('recursos/*', 'recursos'),
    ('config.json', '.'),
],
```

**Ou linha de comando:**
```bash
pyinstaller --add-data "recursos:recursos" --add-data "config.json:." main.py
```

### Otimizar Tamanho do Executável

1. **Use UPX para compressão:**
   ```bash
   # Baixe UPX: https://upx.github.io/
   # Coloque upx.exe na pasta do projeto ou PATH
   
   pyinstaller --upx-dir=. ConversorVideoAudio.spec
   ```

2. **Exclua módulos não usados:**
   
   Edite o arquivo .spec:
   ```python
   excludes=[
       'matplotlib',
       'numpy',
       'pandas',
       'scipy',
       'PIL',
       'tkinter',
       'IPython',
       'jupyter',
   ],
   ```

### Gerar com Console (para Debug)

Para ver mensagens de erro durante desenvolvimento:

```bash
pyinstaller --name ConversorVideoAudio --onefile --console main.py
```

Ou edite .spec:
```python
console=True,  # Mude de False para True
```

## 🐛 Solução de Problemas

### Erro: "PyInstaller não encontrado"

**Solução:**
```bash
pip install pyinstaller
```

### Erro: "Module not found"

**Solução:** Adicione imports ocultos ao .spec:
```python
hiddenimports=[
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'yt_dlp',
    # Adicione outros módulos que faltam
],
```

### Executável muito grande (>200 MB)

**Soluções:**
1. Use `--onefile` (já configurado)
2. Adicione mais exclusões ao .spec
3. Use UPX para compressão
4. Considere `--windowed` (sem console)

### Antivírus bloqueia o .exe

**Normal!** Executáveis PyInstaller são frequentemente marcados como falsos positivos.

**Soluções:**
1. Adicione exceção no antivírus
2. Assine digitalmente o executável (requer certificado)
3. Envie o .exe para análise no VirusTotal
4. Documente que é falso positivo

### Erro "Failed to execute script"

**Soluções:**
1. Gere com console para ver erros: `--console`
2. Verifique se todos os arquivos necessários estão incluídos
3. Teste em ambiente limpo (sem Python instalado)

### Erro de DLL faltando

**Solução:**
Instale Visual C++ Redistributable:
```
https://aka.ms/vs/17/release/vc_redist.x64.exe
```

## 📊 Tamanho Esperado

- **Sem otimização:** ~150-200 MB
- **Com UPX:** ~100-120 MB
- **Altamente otimizado:** ~80-100 MB

## ✅ Checklist Pré-Distribuição

Antes de distribuir o executável:

- [ ] Testado em Windows limpo (sem Python)
- [ ] Testado em Windows 10 e Windows 11
- [ ] FFmpeg documentado como requisito
- [ ] README_WINDOWS.md incluído
- [ ] Verificado em VirusTotal
- [ ] Ícone personalizado (opcional)
- [ ] Versão documentada
- [ ] Changelog incluído

## 📤 Distribuição

### Opções de distribuição:

1. **GitHub Releases:**
   - Crie uma release
   - Anexe o .exe
   - Inclua README_WINDOWS.md

2. **Download direto:**
   - Hospede em servidor próprio
   - Use Google Drive / Dropbox

3. **Instalador (avançado):**
   - Use Inno Setup: https://jrsoftware.org/isinfo.php
   - Crie MSI com WiX Toolset

## 🎯 Resultado Final

Após build bem-sucedido:

```
dist/
└── ConversorVideoAudio.exe  (executável standalone)
```

**Características:**
- ✅ Executável único (portable)
- ✅ Não requer instalação de Python
- ✅ Todas as dependências incluídas
- ✅ Interface gráfica moderna
- ⚠️ Requer FFmpeg instalado no sistema

## 📞 Suporte

Problemas durante o build?

1. Verifique a documentação do PyInstaller: https://pyinstaller.org/
2. Abra uma issue: https://github.com/gustavo-nomelini/conversor-video-audio/issues
3. Consulte a comunidade PyInstaller

---

**Bom build! 🚀**
