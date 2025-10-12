# Cybernetic Video Downloader - Advanced Features
"""
Recursos avançados para o downloader cybernético
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import threading
import queue
import json
import os
import re
from datetime import datetime
import yt_dlp
import requests
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from io import BytesIO
import sqlite3
from cyber_utils import cyber_logger, cyber_config, cyber_utils, cyber_animations

class CyberDatabase:
    """Banco de dados para histórico de downloads"""
    
    def __init__(self, db_file="cyber_downloads.db"):
        self.db_file = db_file
        self.init_database()
        
    def init_database(self):
        """Inicializar banco de dados"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS downloads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    duration INTEGER,
                    quality TEXT,
                    format TEXT,
                    file_size INTEGER,
                    download_path TEXT,
                    status TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    error_message TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    title TEXT,
                    video_count INTEGER,
                    created_time TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            cyber_logger.info("Database initialized successfully")
            
        except Exception as e:
            cyber_logger.error(f"Database initialization failed: {e}")
            
    def add_download(self, download_info):
        """Adicionar download ao histórico"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO downloads 
                (url, title, duration, quality, format, file_size, download_path, status, start_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                download_info.get('url'),
                download_info.get('title'),
                download_info.get('duration'),
                download_info.get('quality'),
                download_info.get('format'),
                download_info.get('file_size'),
                download_info.get('download_path'),
                'started',
                datetime.now()
            ))
            
            download_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return download_id
            
        except Exception as e:
            cyber_logger.error(f"Failed to add download to database: {e}")
            return None
            
    def update_download_status(self, download_id, status, error_message=None):
        """Atualizar status do download"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            if status == 'completed' or status == 'error':
                cursor.execute('''
                    UPDATE downloads 
                    SET status = ?, end_time = ?, error_message = ?
                    WHERE id = ?
                ''', (status, datetime.now(), error_message, download_id))
            else:
                cursor.execute('''
                    UPDATE downloads 
                    SET status = ?, error_message = ?
                    WHERE id = ?
                ''', (status, error_message, download_id))
                
            conn.commit()
            conn.close()
            
        except Exception as e:
            cyber_logger.error(f"Failed to update download status: {e}")
            
    def get_download_history(self, limit=50):
        """Obter histórico de downloads"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM downloads 
                ORDER BY start_time DESC 
                LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return results
            
        except Exception as e:
            cyber_logger.error(f"Failed to get download history: {e}")
            return []


class CyberPlaylistHandler:
    """Manipulador de playlists"""
    
    def __init__(self):
        self.supported_platforms = {
            'youtube': r'youtube\.com/playlist',
            'youtube_channel': r'youtube\.com/c/',
            'youtube_user': r'youtube\.com/user/',
        }
        
    def is_playlist(self, url):
        """Verificar se URL é uma playlist"""
        for platform, pattern in self.supported_platforms.items():
            if re.search(pattern, url, re.IGNORECASE):
                return True
        return 'playlist' in url.lower() or 'list=' in url
        
    def extract_playlist_info(self, url):
        """Extrair informações da playlist"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,  # Não baixar, apenas extrair URLs
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:
                    playlist_info = {
                        'title': info.get('title', 'Unknown Playlist'),
                        'uploader': info.get('uploader', 'Unknown'),
                        'video_count': len(info['entries']),
                        'videos': []
                    }
                    
                    for entry in info['entries']:
                        if entry:
                            video_info = {
                                'title': entry.get('title', 'Unknown'),
                                'url': entry.get('url', ''),
                                'duration': entry.get('duration', 0),
                                'id': entry.get('id', '')
                            }
                            playlist_info['videos'].append(video_info)
                            
                    return playlist_info
                    
        except Exception as e:
            cyber_logger.error(f"Failed to extract playlist info: {e}")
            return None


class CyberAdvancedDownloader:
    """Downloader avançado com recursos extras"""
    
    def __init__(self):
        self.db = CyberDatabase()
        self.playlist_handler = CyberPlaylistHandler()
        self.download_sessions = {}
        
    def create_download_session(self, download_info):
        """Criar sessão de download"""
        session_id = cyber_utils.generate_hash(f"{download_info['url']}_{datetime.now()}")
        
        # Configurar opções do yt-dlp
        output_template = os.path.join(
            cyber_config.get('paths.download_folder'),
            '%(title)s.%(ext)s'
        )
        
        ydl_opts = {
            'format': self._get_format_string(download_info['quality'], download_info['format']),
            'outtmpl': output_template,
            'writeinfojson': True,
            'writethumbnail': True,
            'embedsubs': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'ignoreerrors': False,
            'retries': cyber_config.get('downloads.retry_attempts', 3),
            'fragment_retries': cyber_config.get('downloads.retry_attempts', 3),
            'socket_timeout': cyber_config.get('downloads.timeout', 300),
        }
        
        # Adicionar hooks de progresso
        progress_hooks = [self._create_progress_hook(session_id)]
        ydl_opts['progress_hooks'] = progress_hooks
        
        self.download_sessions[session_id] = {
            'info': download_info,
            'ydl_opts': ydl_opts,
            'status': 'ready',
            'progress': 0,
            'speed': 0,
            'eta': 0
        }
        
        return session_id
        
    def _get_format_string(self, quality, format_type):
        """Obter string de formato para yt-dlp"""
        if format_type in ['mp3', 'wav', 'm4a']:
            return 'bestaudio/best'
        elif quality == 'best':
            return f'best[ext={format_type}]/best'
        else:
            height = quality.replace('p', '')
            return f'best[height<={height}][ext={format_type}]/best[height<={height}]/best'
            
    def _create_progress_hook(self, session_id):
        """Criar hook de progresso para sessão"""
        def progress_hook(d):
            session = self.download_sessions.get(session_id)
            if not session:
                return
                
            if d['status'] == 'downloading':
                try:
                    downloaded = d.get('downloaded_bytes', 0)
                    total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                    speed = d.get('speed', 0)
                    eta = d.get('eta', 0)
                    
                    if total > 0:
                        progress = (downloaded / total) * 100
                        session['progress'] = progress
                        session['downloaded'] = downloaded
                        session['total'] = total
                        session['speed'] = speed
                        session['eta'] = eta
                        session['status'] = 'downloading'
                        
                except Exception as e:
                    cyber_logger.warning(f"Progress hook error: {e}")
                    
            elif d['status'] == 'finished':
                session['status'] = 'completed'
                session['progress'] = 100
                cyber_logger.info(f"Download completed: {d.get('filename', 'Unknown')}")
                
            elif d['status'] == 'error':
                session['status'] = 'error'
                cyber_logger.error(f"Download error: {d.get('error', 'Unknown error')}")
                
        return progress_hook
        
    def start_download(self, session_id):
        """Iniciar download da sessão"""
        session = self.download_sessions.get(session_id)
        if not session:
            return False
            
        def download_thread():
            try:
                session['status'] = 'downloading'
                
                # Adicionar ao banco de dados
                db_id = self.db.add_download(session['info'])
                session['db_id'] = db_id
                
                with yt_dlp.YoutubeDL(session['ydl_opts']) as ydl:
                    ydl.download([session['info']['url']])
                    
                # Atualizar status no banco
                if db_id:
                    self.db.update_download_status(db_id, 'completed')
                    
                cyber_logger.info(f"Download session {session_id} completed successfully")
                
            except Exception as e:
                session['status'] = 'error'
                session['error'] = str(e)
                
                # Atualizar status no banco
                if session.get('db_id'):
                    self.db.update_download_status(session['db_id'], 'error', str(e))
                    
                cyber_logger.error(f"Download session {session_id} failed: {e}")
                
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
        
        return True
        
    def get_session_status(self, session_id):
        """Obter status da sessão"""
        return self.download_sessions.get(session_id, {})
        
    def cancel_download(self, session_id):
        """Cancelar download (implementação básica)"""
        session = self.download_sessions.get(session_id)
        if session:
            session['status'] = 'cancelled'
            
            # Atualizar no banco
            if session.get('db_id'):
                self.db.update_download_status(session['db_id'], 'cancelled')


class CyberThumbnailProcessor:
    """Processador de thumbnails com efeitos cybernéticos"""
    
    @staticmethod
    def apply_cyber_effects(image_path_or_pil, effect_type="glow"):
        """Aplicar efeitos cybernéticos na imagem"""
        try:
            # Carregar imagem
            if isinstance(image_path_or_pil, str):
                image = Image.open(image_path_or_pil)
            else:
                image = image_path_or_pil
                
            # Aplicar efeito baseado no tipo
            if effect_type == "glow":
                return CyberThumbnailProcessor._add_glow_effect(image)
            elif effect_type == "neon":
                return CyberThumbnailProcessor._add_neon_border(image)
            elif effect_type == "scan_lines":
                return CyberThumbnailProcessor._add_scan_lines(image)
            elif effect_type == "cyber_grid":
                return CyberThumbnailProcessor._add_cyber_grid(image)
            else:
                return image
                
        except Exception as e:
            cyber_logger.error(f"Failed to apply cyber effects: {e}")
            return image_path_or_pil if isinstance(image_path_or_pil, Image.Image) else None
            
    @staticmethod
    def _add_glow_effect(image):
        """Adicionar efeito de brilho"""
        # Criar uma versão borrada
        glowed = image.filter(ImageFilter.GaussianBlur(radius=3))
        
        # Aumentar a saturação e brilho
        enhancer = ImageEnhance.Brightness(glowed)
        glowed = enhancer.enhance(1.5)
        
        enhancer = ImageEnhance.Color(glowed)
        glowed = enhancer.enhance(1.3)
        
        # Combinar com a imagem original
        return Image.blend(image, glowed, 0.3)
        
    @staticmethod
    def _add_neon_border(image):
        """Adicionar borda neon"""
        from PIL import ImageDraw
        
        # Criar nova imagem com borda
        border_width = 4
        new_size = (image.width + border_width * 2, image.height + border_width * 2)
        new_image = Image.new('RGB', new_size, (0, 255, 136))  # Verde cybernético
        
        # Colar imagem original no centro
        new_image.paste(image, (border_width, border_width))
        
        return new_image
        
    @staticmethod
    def _add_scan_lines(image):
        """Adicionar linhas de scan CRT"""
        from PIL import ImageDraw
        
        draw = ImageDraw.Draw(image)
        
        # Adicionar linhas horizontais
        for y in range(0, image.height, 4):
            draw.line([(0, y), (image.width, y)], fill=(0, 255, 136, 50))
            
        return image
        
    @staticmethod
    def _add_cyber_grid(image):
        """Adicionar grade cybernética"""
        from PIL import ImageDraw
        
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Grade vertical
        for x in range(0, image.width, 20):
            draw.line([(x, 0), (x, image.height)], fill=(0, 255, 136, 30))
            
        # Grade horizontal
        for y in range(0, image.height, 20):
            draw.line([(0, y), (image.width, y)], fill=(0, 255, 136, 30))
            
        # Combinar com imagem original
        return Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')


# Instância global do downloader avançado
cyber_downloader = CyberAdvancedDownloader()