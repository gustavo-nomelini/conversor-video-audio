# 🚀 Guia Rápido - Gerar Executável Windows

## Para gerar o .exe no Windows:

### Opção 1: Script Automático (Mais Fácil)
```cmd
build_windows.bat
```

### Opção 2: Python
```bash
python build_exe.py
```

### Opção 3: PyInstaller Direto
```bash
pip install pyinstaller
pyinstaller ConversorVideoAudio.spec
```

## Resultado:
✅ Executável em: `dist/ConversorVideoAudio.exe`

## Distribuir:
1. Copie `dist/ConversorVideoAudio.exe`
2. Inclua `README_WINDOWS.md` com instruções
3. Informe sobre requisito do FFmpeg

## Documentação Completa:
📖 Veja `BUILD.md` para guia detalhado

---

**Tempo estimado:** 5-10 minutos  
**Tamanho final:** ~100-150 MB  
**Requer:** Python, pip, dependências instaladas
