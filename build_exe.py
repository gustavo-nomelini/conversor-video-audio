#!/usr/bin/env python3
"""
Script para gerar executável Windows (.exe) do Conversor de Vídeo/Áudio
Usa PyInstaller para criar um único arquivo executável
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Gera o executável Windows"""
    
    print("=" * 70)
    print("🚀 Gerador de Executável Windows - Conversor de Vídeo/Áudio")
    print("=" * 70)
    print()
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller detectado")
    except ImportError:
        print("❌ PyInstaller não encontrado!")
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")
    
    print()
    
    # Configurações
    app_name = "ConversorVideoAudio"
    main_script = "main.py"
    icon_file = "icon.ico"  # Opcional
    
    # Verifica se o script principal existe
    if not os.path.exists(main_script):
        print(f"❌ Erro: {main_script} não encontrado!")
        sys.exit(1)
    
    print(f"📝 Arquivo principal: {main_script}")
    print(f"📦 Nome do executável: {app_name}.exe")
    print()
    
    # Remove builds anteriores
    print("🧹 Limpando builds anteriores...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removido: {folder}/")
    
    # Remove arquivos .spec antigos
    spec_file = f"{app_name}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   Removido: {spec_file}")
    
    print("✅ Limpeza concluída!")
    print()
    
    # Comandos do PyInstaller
    print("🔨 Construindo executável...")
    print("   Isso pode levar alguns minutos...")
    print()
    
    pyinstaller_args = [
        'pyinstaller',
        '--name', app_name,
        '--onefile',  # Um único arquivo executável
        '--windowed',  # Sem console (apenas GUI)
        '--clean',  # Limpa cache antes de build
        '--noconfirm',  # Não pede confirmação
    ]
    
    # Adiciona ícone se existir
    if os.path.exists(icon_file):
        pyinstaller_args.extend(['--icon', icon_file])
        print(f"   🎨 Usando ícone: {icon_file}")
    
    # Adiciona dados necessários (se houver)
    # pyinstaller_args.extend(['--add-data', 'recursos:recursos'])
    
    # Script principal
    pyinstaller_args.append(main_script)
    
    # Executa PyInstaller
    try:
        subprocess.check_call(pyinstaller_args)
        print()
        print("=" * 70)
        print("✅ EXECUTÁVEL GERADO COM SUCESSO!")
        print("=" * 70)
        print()
        
        # Localiza o executável
        exe_path = Path('dist') / f"{app_name}.exe"
        if exe_path.exists():
            exe_size = exe_path.stat().st_size / (1024 * 1024)  # MB
            print(f"📁 Localização: {exe_path.absolute()}")
            print(f"📊 Tamanho: {exe_size:.2f} MB")
            print()
            print("📋 Próximos passos:")
            print("   1. O executável está na pasta 'dist/'")
            print("   2. Copie o arquivo .exe para onde desejar")
            print("   3. Execute diretamente no Windows (sem instalar Python!)")
            print("   4. IMPORTANTE: O FFmpeg ainda precisa estar instalado no Windows")
            print()
            print("💡 Dica: Para distribuir, inclua instruções de instalação do FFmpeg")
            print("   Download: https://ffmpeg.org/download.html")
            print()
        else:
            print("⚠️ Executável gerado mas não encontrado na pasta esperada")
            print("   Verifique a pasta 'dist/' manualmente")
        
    except subprocess.CalledProcessError as e:
        print()
        print("=" * 70)
        print("❌ ERRO AO GERAR EXECUTÁVEL")
        print("=" * 70)
        print(f"Detalhes: {e}")
        print()
        print("🔧 Possíveis soluções:")
        print("   1. Certifique-se de que todas as dependências estão instaladas")
        print("   2. Execute: pip install -r requirements.txt")
        print("   3. Tente novamente")
        sys.exit(1)

if __name__ == '__main__':
    main()
