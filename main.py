#!/usr/bin/env python3
"""
Video/Audio Downloader com Interface Gráfica
Suporte para YouTube e Streamyard (extração automática)
Desenvolvido com PyQt6 e yt-dlp
"""

import sys
import os
import re
import requests
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup,
    QTextEdit, QFileDialog, QProgressBar, QGroupBox, QMessageBox,
    QScrollArea
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor
import yt_dlp


def extract_streamyard_url(url):
    """
    Extrai automaticamente o link VOD.mp4 de uma página do Streamyard
    usando Selenium para capturar requisições de rede
    
    Args:
        url: URL da página do Streamyard (ex: https://streamyard.com/watch/...)
    
    Returns:
        str: URL do vídeo VOD.mp4 ou None se não encontrado
    """
    try:
        # Verifica se é uma URL do Streamyard
        if 'streamyard.com' not in url.lower():
            return None
        
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        import time
        
        # Configurações do Chrome em modo headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Habilita o log de performance para capturar requisições de rede
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        # Inicia o driver
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            # Acessa a página
            driver.get(url)
            
            # Aguarda a página carregar
            time.sleep(5)
            
            # Tenta clicar no botão de play se existir
            try:
                play_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label*="play"], button[class*="play"], .play-button, button svg'))
                )
                play_button.click()
                time.sleep(3)  # Aguarda o vídeo começar a carregar
            except TimeoutException:
                # Se não encontrar botão de play, continua mesmo assim
                pass
            
            # Captura os logs de rede
            logs = driver.get_log('performance')
            
            vod_urls = []
            for log in logs:
                try:
                    import json
                    message = json.loads(log['message'])['message']
                    
                    # Procura por requisições de rede
                    if message['method'] == 'Network.responseReceived' or message['method'] == 'Network.requestWillBeSent':
                        if 'params' in message and 'request' in message['params']:
                            request_url = message['params']['request']['url']
                        elif 'params' in message and 'response' in message['params']:
                            request_url = message['params']['response']['url']
                        else:
                            continue
                        
                        # Procura por URLs que contenham VOD.mp4 ou .mp4 de CDNs conhecidas
                        if any(pattern in request_url.lower() for pattern in ['vod.mp4', 'vod-', '.mp4', 'cloudfront.net', 'akamai', 'cdn']):
                            if request_url.endswith('.mp4') or 'vod' in request_url.lower():
                                vod_urls.append(request_url)
                
                except Exception as e:
                    continue
            
            driver.quit()
            
            # Retorna o primeiro URL VOD.mp4 encontrado
            if vod_urls:
                # Prioriza URLs que contenham "vod" no nome
                vod_priority = [u for u in vod_urls if 'vod' in u.lower()]
                return vod_priority[0] if vod_priority else vod_urls[0]
            
            return None
            
        finally:
            if driver:
                driver.quit()
        
    except ImportError:
        print("Selenium não está instalado. Instale com: pip install selenium")
        return None
    except Exception as e:
        print(f"Erro ao extrair URL do Streamyard: {e}")
        return None


class VideoInfoThread(QThread):
    """Thread para buscar informações do vídeo sem bloquear a interface"""
    info_received = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        """Busca informações do vídeo"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                video_info = {
                    'title': info.get('title', 'video'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Desconhecido'),
                }
                self.info_received.emit(video_info)
        except Exception as e:
            self.error_occurred.emit(str(e))


class DownloadThread(QThread):
    """Thread para executar o download sem bloquear a interface"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    download_progress = pyqtSignal(int)
    
    def __init__(self, url, output_path, download_type, custom_filename=None):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.download_type = download_type
        self.custom_filename = custom_filename
        
    def progress_hook(self, d):
        """Callback para atualizar o progresso do download"""
        if d['status'] == 'downloading':
            try:
                # Calcula a porcentagem do download
                if 'total_bytes' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                elif 'total_bytes_estimate' in d:
                    percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                else:
                    percent = 0
                
                self.download_progress.emit(int(percent))
                
                # Envia informações detalhadas
                speed = d.get('speed', 0)
                speed_str = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "N/A"
                eta = d.get('eta', 0)
                eta_str = f"{eta}s" if eta else "N/A"
                
                self.progress.emit(
                    f"Baixando: {int(percent)}% | Velocidade: {speed_str} | ETA: {eta_str}"
                )
            except Exception as e:
                self.progress.emit(f"Baixando... {str(e)}")
                
        elif d['status'] == 'finished':
            self.progress.emit("Download concluído! Processando arquivo...")
            self.download_progress.emit(100)
    
    def run(self):
        """Executa o download"""
        try:
            # Verifica se é um link do Streamyard e extrai o .m3u8 automaticamente
            url_to_download = self.url
            
            if 'streamyard.com' in self.url.lower() and '.m3u8' not in self.url.lower():
                self.progress.emit("🔍 Detectado link do Streamyard! Extraindo URL do stream...")
                extracted_url = extract_streamyard_url(self.url)
                
                if extracted_url:
                    url_to_download = extracted_url
                    self.progress.emit(f"✅ URL do stream extraída com sucesso!")
                    self.progress.emit(f"📡 Stream: {extracted_url[:60]}...")
                else:
                    self.finished.emit(False, 
                        "❌ Não foi possível extrair o link do stream do Streamyard.\n\n"
                        "Tente:\n"
                        "1. Verificar se o vídeo está disponível\n"
                        "2. Copiar manualmente o link .m3u8 usando F12 → Rede"
                    )
                    return
            
            # Configurações base do yt-dlp
            ydl_opts = {
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,  # --no-playlist
                # Configurações para evitar bloqueio de bot e erro 403
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'ios', 'web'],
                        'skip': ['hls', 'dash'],
                    }
                },
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
            }
            
            # Configurações específicas por tipo de download
            if self.download_type == 'mp4':
                # Define o nome do arquivo
                if self.custom_filename:
                    output_template = os.path.join(self.output_path, f"{self.custom_filename}.%(ext)s")
                else:
                    output_template = os.path.join(self.output_path, '%(title)s.%(ext)s')
                
                # Parâmetros: -f "bv*[ext=mp4]+ba[ext=m4a]/mp4" --merge-output-format mp4 --no-playlist
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': output_template,
                    'merge_output_format': 'mp4',
                })
                self.progress.emit("Iniciando download do vídeo em MP4...")
                
            elif self.download_type == 'mp3':
                # Define o nome do arquivo
                if self.custom_filename:
                    output_template = os.path.join(self.output_path, f"{self.custom_filename}.%(ext)s")
                else:
                    output_template = os.path.join(self.output_path, '%(title)s.%(ext)s')
                
                # Parâmetros: -f bestaudio -x --audio-format mp3 --audio-quality 0 --no-playlist
                ydl_opts.update({
                    'format': 'bestaudio',
                    'outtmpl': output_template,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '0',  # 0 = melhor qualidade
                    }],
                    'extractaudio': True,  # -x
                })
                self.progress.emit("Iniciando extração de áudio em MP3...")
            
            # Executa o download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_to_download, download=True)
                filename = ydl.prepare_filename(info)
                
                # Para MP3, o nome do arquivo muda após a conversão
                if self.download_type == 'mp3':
                    filename = os.path.splitext(filename)[0] + '.mp3'
                
                self.finished.emit(True, f"Download concluído!\nArquivo salvo em:\n{filename}")
                
        except Exception as e:
            self.finished.emit(False, f"Erro durante o download:\n{str(e)}")


class YouTubeDownloaderGUI(QMainWindow):
    """Interface gráfica principal do YouTube Downloader"""
    
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.video_info_thread = None
        self.suggested_filename = ""
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Conversor de Vídeo/Áudio - MP4 & MP3")
        self.setMinimumSize(850, 800)
        
        # Aplica tema moderno com alto contraste (compatível com tema escuro)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QScrollArea {
                background-color: #1a1a1a;
                border: none;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QGroupBox {
                background-color: #2d2d2d;
                border: 3px solid #4a9eff;
                border-radius: 10px;
                margin-top: 16px;
                padding-top: 20px;
                font-weight: bold;
                font-size: 14pt;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: #4a9eff;
                font-size: 14pt;
            }
            QLabel {
                color: #ffffff;
                font-size: 13pt;
                background-color: transparent;
            }
            QLineEdit {
                padding: 14px 18px;
                border: 3px solid #4a4a4a;
                border-radius: 8px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 13pt;
                selection-background-color: #4a9eff;
                selection-color: #ffffff;
            }
            QLineEdit:focus {
                border: 3px solid #4a9eff;
                background-color: #353535;
            }
            QLineEdit:disabled {
                background-color: #252525;
                color: #666666;
                border: 3px solid #333333;
            }
            QLineEdit::placeholder {
                color: #888888;
            }
            QRadioButton {
                spacing: 12px;
                font-size: 13pt;
                padding: 8px;
                color: #ffffff;
                font-weight: bold;
            }
            QRadioButton::indicator {
                width: 22px;
                height: 22px;
            }
            QRadioButton::indicator:unchecked {
                border: 3px solid #4a9eff;
                border-radius: 11px;
                background-color: #2d2d2d;
            }
            QRadioButton::indicator:checked {
                border: 3px solid #4a9eff;
                border-radius: 11px;
                background-color: #4a9eff;
            }
            QRadioButton:hover {
                color: #4a9eff;
            }
            QProgressBar {
                border: 3px solid #4a4a4a;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                font-size: 13pt;
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a9eff, stop:1 #64b5f6);
                border-radius: 5px;
            }
            QTextEdit {
                background-color: #2d2d2d;
                border: 3px solid #4a4a4a;
                border-radius: 8px;
                padding: 15px;
                font-family: 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace;
                font-size: 12pt;
                color: #ffffff;
                line-height: 1.6;
            }
        """)
        
        # Widget central com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Cabeçalho com gradiente vibrante
        header_widget = QWidget()
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a9eff, stop:1 #2979ff);
                border-radius: 15px;
                padding: 25px;
            }
        """)
        header_layout = QVBoxLayout()
        header_layout.setSpacing(12)
        
        # Título
        title_label = QLabel("🎬 Conversor de Vídeo/Áudio")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #ffffff; background: transparent; font-weight: 900;")
        header_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Baixe vídeos em MP4 ou extraia áudio em MP3")
        subtitle_font = QFont()
        subtitle_font.setPointSize(15)
        subtitle_font.setBold(True)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #ffffff; background: transparent;")
        header_layout.addWidget(subtitle_label)
        
        # Badge de plataformas suportadas
        platforms_label = QLabel("✨ YouTube • Streamyard • E mais")
        platforms_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        platforms_font = QFont()
        platforms_font.setPointSize(12)
        platforms_font.setBold(True)
        platforms_label.setFont(platforms_font)
        platforms_label.setStyleSheet("""
            color: #ffffff; 
            background: rgba(255,255,255,0.25); 
            padding: 10px 20px;
            border-radius: 20px;
        """)
        platforms_label.setMaximumWidth(350)
        header_layout.addWidget(platforms_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        header_widget.setLayout(header_layout)
        main_layout.addWidget(header_widget)
        
        # Grupo: URL do Vídeo
        url_group = QGroupBox("🔗 URL do Vídeo")
        url_layout = QVBoxLayout()
        url_layout.setSpacing(10)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Cole aqui o link do vídeo...")
        self.url_input.setMinimumHeight(50)
        self.url_input.textChanged.connect(self.on_url_changed)
        
        # Botão para analisar vídeo
        analyze_layout = QHBoxLayout()
        self.analyze_button = QPushButton("🔍 Analisar Vídeo")
        self.analyze_button.setMinimumHeight(50)
        analyze_font = QFont()
        analyze_font.setPointSize(13)
        analyze_font.setBold(True)
        self.analyze_button.setFont(analyze_font)
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background-color: #2979ff;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        self.analyze_button.clicked.connect(self.analyze_video)
        self.analyze_button.setEnabled(False)
        analyze_layout.addStretch()
        analyze_layout.addWidget(self.analyze_button)
        
        url_layout.addWidget(self.url_input)
        url_layout.addLayout(analyze_layout)
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)
        
        # Info do vídeo (inicialmente oculto)
        self.video_info_widget = QWidget()
        self.video_info_widget.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border: 3px solid #4a9eff;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.video_info_widget.setVisible(False)
        video_info_layout = QVBoxLayout()
        
        self.video_title_label = QLabel()
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        self.video_title_label.setFont(title_font)
        self.video_title_label.setStyleSheet("font-weight: bold; color: #4a9eff; background: transparent;")
        self.video_title_label.setWordWrap(True)
        
        self.video_details_label = QLabel()
        details_font = QFont()
        details_font.setPointSize(12)
        self.video_details_label.setFont(details_font)
        self.video_details_label.setStyleSheet("color: #cccccc; background: transparent;")
        
        video_info_layout.addWidget(self.video_title_label)
        video_info_layout.addWidget(self.video_details_label)
        self.video_info_widget.setLayout(video_info_layout)
        main_layout.addWidget(self.video_info_widget)
        
        # Grupo: Nome do Arquivo
        filename_group = QGroupBox("📝 Nome do Arquivo")
        filename_layout = QVBoxLayout()
        filename_layout.setSpacing(12)
        
        filename_hint = QLabel("Personalize o nome do arquivo ou deixe vazio para usar o nome original")
        hint_font = QFont()
        hint_font.setPointSize(12)
        filename_hint.setFont(hint_font)
        filename_hint.setStyleSheet("color: #aaaaaa; font-weight: normal;")
        filename_hint.setWordWrap(True)
        
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("Nome do arquivo (sem extensão)")
        self.filename_input.setMinimumHeight(50)
        
        filename_layout.addWidget(filename_hint)
        filename_layout.addWidget(self.filename_input)
        filename_group.setLayout(filename_layout)
        main_layout.addWidget(filename_group)
        
        # Grupo: Pasta de Destino
        path_group = QGroupBox("📁 Pasta de Destino")
        path_layout = QHBoxLayout()
        
        self.path_input = QLineEdit()
        self.path_input.setText(str(Path.home() / "Downloads"))
        self.path_input.setMinimumHeight(50)
        
        browse_button = QPushButton("Procurar")
        browse_button.setMinimumHeight(50)
        browse_button.setMinimumWidth(140)
        browse_font = QFont()
        browse_font.setPointSize(13)
        browse_font.setBold(True)
        browse_button.setFont(browse_font)
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #6c6c6c;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8c8c8c;
            }
        """)
        browse_button.clicked.connect(self.browse_folder)
        
        path_layout.addWidget(self.path_input, 1)
        path_layout.addWidget(browse_button)
        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)
        
        # Grupo: Tipo de Download
        type_group = QGroupBox("🎯 Formato de Download")
        type_layout = QVBoxLayout()
        type_layout.setSpacing(15)
        
        self.button_group = QButtonGroup()
        
        self.radio_mp4 = QRadioButton("🎥 Vídeo MP4 (melhor qualidade disponível)")
        self.radio_mp4.setChecked(True)
        
        self.radio_mp3 = QRadioButton("🎵 Áudio MP3 (apenas áudio, alta qualidade)")
        
        self.button_group.addButton(self.radio_mp4)
        self.button_group.addButton(self.radio_mp3)
        
        type_layout.addWidget(self.radio_mp4)
        type_layout.addWidget(self.radio_mp3)
        type_group.setLayout(type_layout)
        main_layout.addWidget(type_group)
        
        # Barra de progresso
        progress_label = QLabel("⚡ Progresso do Download:")
        progress_font = QFont()
        progress_font.setPointSize(14)
        progress_font.setBold(True)
        progress_label.setFont(progress_font)
        progress_label.setStyleSheet("font-weight: bold; color: #ffffff; margin-top: 10px;")
        main_layout.addWidget(progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimumHeight(38)
        self.progress_bar.setFormat("%p% - Pronto para iniciar")
        main_layout.addWidget(self.progress_bar)
        
        # Botão de Download (destaque)
        self.download_button = QPushButton("⬇️ Iniciar Download")
        self.download_button.setMinimumHeight(65)
        download_font = QFont()
        download_font.setPointSize(16)
        download_font.setBold(True)
        self.download_button.setFont(download_font)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #00c853;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #00e676;
            }
            QPushButton:pressed {
                background-color: #00a844;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)
        
        # Log de status
        log_label = QLabel("📋 Log de Atividades:")
        log_font = QFont()
        log_font.setPointSize(14)
        log_font.setBold(True)
        log_label.setFont(log_font)
        log_label.setStyleSheet("font-weight: bold; color: #ffffff; margin-top: 15px;")
        main_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        main_layout.addWidget(self.log_text)
        
        # Rodapé
        footer_label = QLabel("💻 Desenvolvido com PyQt6 e yt-dlp | Gustavo Nomelini © 2025")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_font = QFont()
        footer_font.setPointSize(11)
        footer_label.setFont(footer_font)
        footer_label.setStyleSheet("color: #888888; margin-top: 20px;")
        main_layout.addWidget(footer_label)
        
        central_widget.setLayout(main_layout)
        
        # Log inicial
        self.add_log("✅ Aplicação iniciada e pronta para uso!")
        self.add_log("ℹ️ Cole uma URL e clique em 'Analisar Vídeo' para começar")
    
    def on_url_changed(self, text):
        """Habilita/desabilita botão de análise baseado na URL"""
        self.analyze_button.setEnabled(bool(text.strip()))
        self.video_info_widget.setVisible(False)
        self.filename_input.clear()
    
    def analyze_video(self):
        """Analisa o vídeo e obtém informações"""
        url = self.url_input.text().strip()
        
        if not url:
            return
        
        self.analyze_button.setEnabled(False)
        self.analyze_button.setText("🔄 Analisando...")
        self.add_log(f"🔍 Analisando vídeo: {url[:50]}...")
        
        # Inicia thread para buscar info
        self.video_info_thread = VideoInfoThread(url)
        self.video_info_thread.info_received.connect(self.on_video_info_received)
        self.video_info_thread.error_occurred.connect(self.on_video_info_error)
        self.video_info_thread.start()
    
    def on_video_info_received(self, info):
        """Callback quando informações do vídeo são recebidas"""
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("🔍 Analisar Vídeo")
        
        # Limpa e formata o título para usar como nome de arquivo
        title = info['title']
        # Remove caracteres inválidos para nomes de arquivo
        clean_title = re.sub(r'[<>:"/\\|?*]', '', title)
        clean_title = clean_title.strip()
        
        self.suggested_filename = clean_title
        
        # Mostra informações do vídeo
        self.video_title_label.setText(f"📹 {title}")
        
        duration = info.get('duration', 0)
        duration_str = f"{duration // 60}:{duration % 60:02d}" if duration > 0 else "Desconhecido"
        uploader = info.get('uploader', 'Desconhecido')
        
        self.video_details_label.setText(f"👤 {uploader} | ⏱️ Duração: {duration_str}")
        
        # Sugere o nome do arquivo
        self.filename_input.setText(clean_title)
        self.filename_input.selectAll()
        
        self.video_info_widget.setVisible(True)
        
        self.add_log(f"✅ Vídeo analisado: {title}")
        self.add_log(f"💡 Nome sugerido para o arquivo: {clean_title}")
    
    def on_video_info_error(self, error):
        """Callback quando ocorre erro ao buscar informações"""
        self.analyze_button.setEnabled(True)
        self.analyze_button.setText("🔍 Analisar Vídeo")
        
        self.add_log(f"⚠️ Não foi possível analisar o vídeo: {error}")
        QMessageBox.warning(
            self,
            "Aviso",
            "Não foi possível analisar o vídeo.\nVocê ainda pode tentar fazer o download."
        )
        
    def browse_folder(self):
        """Abre diálogo para selecionar pasta de destino"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Destino",
            self.path_input.text()
        )
        if folder:
            self.path_input.setText(folder)
            self.add_log(f"📁 Pasta de destino: {folder}")
    
    def add_log(self, message):
        """Adiciona mensagem ao log com timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        # Auto-scroll para o final
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_download(self):
        """Inicia o processo de download"""
        url = self.url_input.text().strip()
        output_path = self.path_input.text().strip()
        custom_filename = self.filename_input.text().strip()
        
        # Validações
        if not url:
            QMessageBox.warning(
                self,
                "Campo Obrigatório",
                "Por favor, insira a URL do vídeo!"
            )
            self.url_input.setFocus()
            return
        
        if not output_path or not os.path.exists(output_path):
            QMessageBox.warning(
                self,
                "Pasta Inválida",
                "Por favor, selecione uma pasta de destino válida!"
            )
            return
        
        # Determina o tipo de download
        download_type = 'mp4' if self.radio_mp4.isChecked() else 'mp3'
        
        # Desabilita controles durante o download
        self.download_button.setEnabled(False)
        self.download_button.setText("⏳ Baixando...")
        self.url_input.setEnabled(False)
        self.filename_input.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p% - Iniciando...")
        
        # Log
        self.add_log("=" * 60)
        self.add_log(f"🚀 Iniciando download: {download_type.upper()}")
        self.add_log(f"🔗 URL: {url[:70]}{'...' if len(url) > 70 else ''}")
        if custom_filename:
            self.add_log(f"📝 Nome personalizado: {custom_filename}.{download_type}")
        
        # Cria e inicia a thread de download
        self.download_thread = DownloadThread(url, output_path, download_type, custom_filename)
        self.download_thread.progress.connect(self.add_log)
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, value):
        """Atualiza a barra de progresso"""
        self.progress_bar.setValue(value)
        if value < 100:
            self.progress_bar.setFormat(f"%p% - Baixando...")
        else:
            self.progress_bar.setFormat("%p% - Concluído!")
    
    def download_finished(self, success, message):
        """Callback quando o download termina"""
        # Reabilita controles
        self.download_button.setEnabled(True)
        self.download_button.setText("⬇️ Iniciar Download")
        self.url_input.setEnabled(True)
        self.filename_input.setEnabled(True)
        self.analyze_button.setEnabled(True)
        
        if success:
            self.add_log("✅ " + message.split('\n')[0])
            self.add_log(f"💾 {message.split('Arquivo salvo em:')[-1].strip() if 'Arquivo salvo em:' in message else ''}")
            self.progress_bar.setValue(100)
            self.progress_bar.setFormat("100% - Concluído com sucesso!")
            
            # Mensagem de sucesso
            QMessageBox.information(
                self,
                "✅ Download Concluído",
                message,
                QMessageBox.StandardButton.Ok
            )


def main():
    """Função principal"""
    app = QApplication(sys.argv)
    
    # Estilo da aplicação
    app.setStyle('Fusion')
    
    window = YouTubeDownloaderGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
