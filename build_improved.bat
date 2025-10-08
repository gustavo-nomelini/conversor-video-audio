@echo off
REM Script melhorado para gerar executável Windows do Conversor de Vídeo/Áudio
REM Execute este script no Windows para criar o .exe

echo ========================================================================
echo  Gerador de Executavel Windows - Conversor de Video/Audio (Melhorado)
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
python --version
echo.

REM Cria ambiente virtual se não existir
echo [*] Configurando ambiente virtual...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual já existe
)

REM Ativa ambiente virtual
echo [*] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)

echo [OK] Ambiente virtual ativado
echo.

REM Atualiza pip
echo [*] Atualizando pip...
python -m pip install --upgrade pip
echo.

REM Instala dependências
echo [*] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias
    echo Tentando instalar individualmente...
    pip install PyQt6==6.7.1
    pip install yt-dlp==2024.8.6
    pip install requests==2.31.0
    pip install selenium==4.15.2
    pip install pyinstaller>=6.0.0
)

echo [OK] Dependencias instaladas
echo.

REM Limpa builds anteriores
echo [*] Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
if exist ConversorVideoAudio.spec del /q ConversorVideoAudio.spec

echo [OK] Limpeza concluida
echo.

REM Gera o executável com configurações otimizadas
echo [*] Gerando executavel...
echo    Isso pode levar alguns minutos...
echo.

pyinstaller ^
    --name ConversorVideoAudio ^
    --onefile ^
    --windowed ^
    --clean ^
    --noconfirm ^
    --add-data "requirements.txt;." ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import yt_dlp ^
    --hidden-import selenium ^
    --hidden-import requests ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    main.py

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo [ERRO] Falha ao gerar executavel
    echo ========================================================================
    echo Tentando com modo console para debug...
    
    pyinstaller ^
        --name ConversorVideoAudio_debug ^
        --onefile ^
        --console ^
        --clean ^
        --noconfirm ^
        --hidden-import PyQt6.QtCore ^
        --hidden-import PyQt6.QtGui ^
        --hidden-import PyQt6.QtWidgets ^
        --hidden-import yt_dlp ^
        --hidden-import selenium ^
        --hidden-import requests ^
        main.py
    
    if errorlevel 1 (
        echo [ERRO] Falha mesmo com modo debug
        pause
        exit /b 1
    ) else (
        echo [OK] Executavel debug criado em dist\ConversorVideoAudio_debug.exe
    )
)

echo.
echo ========================================================================
echo [SUCESSO] Executavel gerado com sucesso!
echo ========================================================================
echo.

REM Verifica se o arquivo foi criado
if exist dist\ConversorVideoAudio.exe (
    echo Executavel principal: %CD%\dist\ConversorVideoAudio.exe
    for %%A in (dist\ConversorVideoAudio.exe) do (
        echo Tamanho: %%~zA bytes
    )
    echo.
)

if exist dist\ConversorVideoAudio_debug.exe (
    echo Executavel debug: %CD%\dist\ConversorVideoAudio_debug.exe
    for %%A in (dist\ConversorVideoAudio_debug.exe) do (
        echo Tamanho: %%~zA bytes
    )
    echo.
)

echo ========================================================================
echo INSTRUCOES IMPORTANTES:
echo ========================================================================
echo.
echo 1. O executavel esta na pasta 'dist\'
echo 2. Para funcionar completamente, o sistema precisa ter:
echo    - FFmpeg instalado e no PATH do sistema
echo    - Ou inclua ffmpeg.exe na mesma pasta do executavel
echo.
echo 3. Para distribuir:
echo    - Copie o arquivo .exe
echo    - Inclua ffmpeg.exe (se necessario)
echo    - Inclua o README_WINDOWS.md com instrucoes
echo.
echo 4. Se houver erros, use a versao debug para ver mensagens
echo.

echo Desativando ambiente virtual...
call venv\Scripts\deactivate.bat

pause
