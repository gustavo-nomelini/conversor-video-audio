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
    QTextEdit, QFileDialog, QProgressBar, QGroupBox, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon
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


class DownloadThread(QThread):
    """Thread para executar o download sem bloquear a interface"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    download_progress = pyqtSignal(int)
    
    def __init__(self, url, output_path, download_type):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.download_type = download_type
        
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
                # Parâmetros: -f "bv*[ext=mp4]+ba[ext=m4a]/mp4" --merge-output-format mp4 --no-playlist
                ydl_opts.update({
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                    'merge_output_format': 'mp4',
                })
                self.progress.emit("Iniciando download do vídeo em MP4...")
                
            elif self.download_type == 'mp3':
                # Parâmetros: -f bestaudio -x --audio-format mp3 --audio-quality 0 --no-playlist
                ydl_opts.update({
                    'format': 'bestaudio',
                    'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
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
        self.init_ui()
        
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("Conversor de Vídeo/Áudio - MP4 & MP3")
        self.setMinimumSize(700, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title_label = QLabel("🎬 Conversor de Vídeo/Áudio")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtítulo
        subtitle_label = QLabel("Baixe vídeos em MP4 ou extraia áudio em MP3 (YouTube e Streamyard)")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #666;")
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(10)
        
        # Grupo: URL do Vídeo
        url_group = QGroupBox("URL do Vídeo")
        url_layout = QVBoxLayout()
        
        url_label = QLabel("Cole o link do vídeo:")
        
        # Adiciona instrução informativa
        info_label = QLabel("✨ Suporta YouTube e Streamyard (extração automática do stream)")
        info_label.setStyleSheet("color: #0066cc; font-size: 9pt; margin-bottom: 5px;")
        info_label.setWordWrap(True)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=... ou https://streamyard.com/watch/...")
        self.url_input.setMinimumHeight(35)
        
        url_layout.addWidget(url_label)
        url_layout.addWidget(info_label)
        url_layout.addWidget(self.url_input)
        url_group.setLayout(url_layout)
        main_layout.addWidget(url_group)
        
        # Grupo: Pasta de Destino
        path_group = QGroupBox("Pasta de Destino")
        path_layout = QHBoxLayout()
        
        self.path_input = QLineEdit()
        self.path_input.setText(str(Path.home() / "Downloads"))
        self.path_input.setMinimumHeight(35)
        
        browse_button = QPushButton("📁 Procurar")
        browse_button.setMinimumHeight(35)
        browse_button.clicked.connect(self.browse_folder)
        
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        path_group.setLayout(path_layout)
        main_layout.addWidget(path_group)
        
        # Grupo: Tipo de Download
        type_group = QGroupBox("Formato de Download")
        type_layout = QVBoxLayout()
        
        self.button_group = QButtonGroup()
        
        self.radio_mp4 = QRadioButton("🎥 Vídeo MP4 (melhor qualidade)")
        self.radio_mp4.setChecked(True)
        
        self.radio_mp3 = QRadioButton("🎵 Áudio MP3 (apenas áudio, melhor qualidade)")
        
        self.button_group.addButton(self.radio_mp4)
        self.button_group.addButton(self.radio_mp3)
        
        type_layout.addWidget(self.radio_mp4)
        type_layout.addWidget(self.radio_mp3)
        type_group.setLayout(type_layout)
        main_layout.addWidget(type_group)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimumHeight(25)
        main_layout.addWidget(self.progress_bar)
        
        # Botão de Download
        self.download_button = QPushButton("⬇️ Iniciar Download")
        self.download_button.setMinimumHeight(45)
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)
        
        # Log de status
        log_label = QLabel("Log de Atividades:")
        main_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Courier New', 'Monaco', monospace;
            }
        """)
        main_layout.addWidget(self.log_text)
        
        # Rodapé
        footer_label = QLabel("Desenvolvido com PyQt6 e yt-dlp")
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_label.setStyleSheet("color: #999; font-size: 9px;")
        main_layout.addWidget(footer_label)
        
        central_widget.setLayout(main_layout)
        
        # Log inicial
        self.add_log("Aplicação iniciada. Pronta para download!")
        
    def browse_folder(self):
        """Abre diálogo para selecionar pasta de destino"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Selecionar Pasta de Destino",
            self.path_input.text()
        )
        if folder:
            self.path_input.setText(folder)
            self.add_log(f"Pasta de destino alterada para: {folder}")
    
    def add_log(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.append(f"• {message}")
        # Auto-scroll para o final
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_download(self):
        """Inicia o processo de download"""
        url = self.url_input.text().strip()
        output_path = self.path_input.text().strip()
        
        # Validações
        if not url:
            QMessageBox.warning(self, "Aviso", "Por favor, insira uma URL válida!")
            return
        
        if not output_path or not os.path.exists(output_path):
            QMessageBox.warning(
                self,
                "Aviso",
                "Por favor, selecione uma pasta de destino válida!"
            )
            return
        
        # Determina o tipo de download
        download_type = 'mp4' if self.radio_mp4.isChecked() else 'mp3'
        
        # Desabilita o botão durante o download
        self.download_button.setEnabled(False)
        self.download_button.setText("⏳ Baixando...")
        self.progress_bar.setValue(0)
        
        # Limpa log anterior
        self.add_log("=" * 50)
        self.add_log(f"Iniciando download: {download_type.upper()}")
        self.add_log(f"URL: {url}")
        
        # Cria e inicia a thread de download
        self.download_thread = DownloadThread(url, output_path, download_type)
        self.download_thread.progress.connect(self.add_log)
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, value):
        """Atualiza a barra de progresso"""
        self.progress_bar.setValue(value)
    
    def download_finished(self, success, message):
        """Callback quando o download termina"""
        self.download_button.setEnabled(True)
        self.download_button.setText("⬇️ Iniciar Download")
        
        if success:
            self.add_log("✅ " + message)
            QMessageBox.information(self, "Sucesso", message)
            self.progress_bar.setValue(100)
        else:
            self.add_log("❌ " + message)
            QMessageBox.critical(self, "Erro", message)
            self.progress_bar.setValue(0)


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
