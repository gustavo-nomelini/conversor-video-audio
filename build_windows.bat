@echo off
REM Script para gerar executável Windows do Conversor de Vídeo/Áudio
REM Execute este script no Windows para criar o .exe

echo ========================================================================
echo  Gerador de Executavel Windows - Conversor de Video/Audio
echo ========================================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8+ do site: https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python detectado
echo.

REM Instala dependências
echo [*] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias
    pause
    exit /b 1
)

echo [OK] Dependencias instaladas
echo.

REM Instala PyInstaller
echo [*] Instalando PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERRO] Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo [OK] PyInstaller instalado
echo.

REM Limpa builds anteriores
echo [*] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ConversorVideoAudio.spec del /q ConversorVideoAudio.spec
echo [OK] Limpeza concluida
echo.

REM Gera o executável
echo [*] Gerando executavel...
echo    Isso pode levar alguns minutos...
echo.

pyinstaller ^
    --name ConversorVideoAudio ^
    --onefile ^
    --windowed ^
    --clean ^
    --noconfirm ^
    main.py

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo [ERRO] Falha ao gerar executavel
    echo ========================================================================
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo [SUCESSO] Executavel gerado com sucesso!
echo ========================================================================
echo.
echo Localizacao: %CD%\dist\ConversorVideoAudio.exe
echo.

REM Verifica o tamanho do arquivo
if exist dist\ConversorVideoAudio.exe (
    for %%A in (dist\ConversorVideoAudio.exe) do (
        set size=%%~zA
    )
    echo Tamanho: %size% bytes
    echo.
    echo Proximos passos:
    echo 1. O executavel esta na pasta 'dist\'
    echo 2. Copie o arquivo .exe para onde desejar
    echo 3. Execute diretamente no Windows
    echo 4. IMPORTANTE: FFmpeg precisa estar instalado no sistema
    echo.
    echo Para distribuir, inclua o README_WINDOWS.md com instrucoes
    echo.
) else (
    echo [AVISO] Executavel gerado mas nao encontrado
    echo Verifique a pasta 'dist\' manualmente
    echo.
)

pause
