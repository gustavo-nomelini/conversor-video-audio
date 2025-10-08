#!/usr/bin/env python3
"""
Script auxiliar para build do Conversor de Vídeo/Áudio
Verifica dependências e gera executável
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"[ERRO] Python {version.major}.{version.minor} não é suportado")
        print("Instale Python 3.8 ou superior")
        return False
    
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Instala as dependências necessárias"""
    print("\n[*] Instalando dependências...")
    
    # Lista de pacotes essenciais
    packages = [
        "PyQt6==6.7.1",
        "yt-dlp==2024.8.6", 
        "requests==2.31.0",
        "selenium==4.15.2",
        "pyinstaller>=6.0.0"
    ]
    
    # Atualiza pip primeiro
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("[OK] Pip atualizado")
    except subprocess.CalledProcessError as e:
        print(f"[AVISO] Falha ao atualizar pip: {e}")
    
    # Instala cada pacote
    for package in packages:
        try:
            print(f"   Instalando {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERRO] Falha ao instalar {package}: {e}")
            return False
    
    print("[OK] Todas as dependências instaladas")
    return True

def clean_build():
    """Remove arquivos de build anteriores"""
    print("\n[*] Limpando builds anteriores...")
    
    dirs_to_remove = ["build", "dist", "__pycache__"]
    files_to_remove = ["ConversorVideoAudio.spec", "ConversorVideoAudio_debug.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f"   Removido: {dir_name}/")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"   Removido: {file_name}")
    
    print("[OK] Limpeza concluída")

def build_executable():
    """Gera o executável usando PyInstaller"""
    print("\n[*] Gerando executável...")
    print("   Isso pode levar alguns minutos...")
    
    # Comando base do PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "ConversorVideoAudio",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--add-data", "requirements.txt;.",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui", 
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "selenium",
        "--hidden-import", "requests",
        "--exclude-module", "tkinter",
        "--exclude-module", "matplotlib",
        "--exclude-module", "numpy",
        "--exclude-module", "pandas",
        "main.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[OK] Executável gerado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao gerar executável: {e}")
        print(f"Stderr: {e.stderr}")
        
        # Tenta build debug
        print("\n[*] Tentando build debug...")
        cmd_debug = cmd.copy()
        cmd_debug[2] = "ConversorVideoAudio_debug"  # nome
        cmd_debug.remove("--windowed")
        cmd_debug.append("--console")
        
        try:
            subprocess.run(cmd_debug, check=True, capture_output=True, text=True)
            print("[OK] Executável debug gerado!")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"[ERRO] Falha também no build debug: {e2}")
            return False

def check_result():
    """Verifica se o executável foi criado"""
    print("\n" + "="*70)
    print(" RESULTADO DO BUILD")
    print("="*70)
    
    exe_path = Path("dist/ConversorVideoAudio.exe")
    debug_path = Path("dist/ConversorVideoAudio_debug.exe")
    
    if exe_path.exists():
        size = exe_path.stat().st_size
        print(f"[SUCESSO] Executável principal: {exe_path.absolute()}")
        print(f"          Tamanho: {size:,} bytes ({size/1024/1024:.1f} MB)")
    
    if debug_path.exists():
        size = debug_path.stat().st_size
        print(f"[INFO] Executável debug: {debug_path.absolute()}")
        print(f"       Tamanho: {size:,} bytes ({size/1024/1024:.1f} MB)")
    
    if not exe_path.exists() and not debug_path.exists():
        print("[ERRO] Nenhum executável foi criado!")
        return False
    
    print("\n" + "="*70)
    print(" INSTRUÇÕES IMPORTANTES")
    print("="*70)
    print("1. Para funcionar completamente, o sistema precisa ter:")
    print("   - FFmpeg instalado e no PATH do sistema")
    print("   - Ou inclua ffmpeg.exe na mesma pasta do executável")
    print("")
    print("2. Para distribuir:")
    print("   - Copie o arquivo .exe")
    print("   - Inclua ffmpeg.exe (se necessário)")
    print("   - Inclua documentação")
    print("")
    print("3. Se houver erros, use a versão debug para ver mensagens")
    
    return True

def main():
    """Função principal"""
    print("="*70)
    print(" GERADOR DE EXECUTÁVEL - CONVERSOR DE VÍDEO/ÁUDIO")
    print("="*70)
    
    # Verifica Python
    if not check_python_version():
        return 1
    
    # Instala dependências
    if not install_dependencies():
        return 1
    
    # Limpa builds anteriores
    clean_build()
    
    # Gera executável
    if not build_executable():
        return 1
    
    # Verifica resultado
    if not check_result():
        return 1
    
    print("\n[SUCESSO] Build concluído!")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n[CANCELADO] Build interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO INESPERADO] {e}")
        sys.exit(1)
    
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
