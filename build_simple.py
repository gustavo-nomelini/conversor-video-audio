#!/usr/bin/env python3
"""
Build Script Simplificado para Conversor de Vídeo/Áudio
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("="*60)
    print(" BUILD CONVERSOR DE VÍDEO/ÁUDIO")
    print("="*60)
    
    # Verifica Python
    print(f"Python: {sys.version}")
    
    # Instala dependências
    print("\n[1/4] Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependências instaladas")
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar dependências")
        return False
    
    # Instala PyInstaller
    print("\n[2/4] Instalando PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller instalado")
    except subprocess.CalledProcessError:
        print("✗ Erro ao instalar PyInstaller")
        return False
    
    # Limpa build anterior
    print("\n[3/4] Limpando builds anteriores...")
    import shutil
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"✓ Removido {folder}/")
    
    # Gera executável
    print("\n[4/4] Gerando executável...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "ConversorVideoAudio",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Executável gerado com sucesso!")
        
        exe_path = Path("dist/ConversorVideoAudio.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / 1024 / 1024
            print(f"📁 Local: {exe_path.absolute()}")
            print(f"📏 Tamanho: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError:
        print("✗ Erro ao gerar executável")
        print("\nTentando build com console para debug...")
        
        cmd_debug = [
            sys.executable, "-m", "PyInstaller",
            "--name", "ConversorVideoAudio_debug",
            "--onefile",
            "--console",
            "--clean",
            "--noconfirm",
            "main.py"
        ]
        
        try:
            subprocess.run(cmd_debug, check=True)
            print("✓ Executável debug gerado!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Falhou também no modo debug")
            return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("\nIMPORTANTE: Para funcionar, instale FFmpeg no sistema")
        print("ou coloque ffmpeg.exe na mesma pasta do executável")
    else:
        print("\n❌ BUILD FALHOU")
    
    input("\nPressione Enter para sair...")
