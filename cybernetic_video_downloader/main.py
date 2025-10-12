"""
Cybernetic Video Downloader
Interface principal com design futurista e cybernético
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import threading
import queue
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
import requests
from io import BytesIO
import yt_dlp
import time
import re

class CyberneticVideoDownloader:
    def __init__(self):
        # Configuração da janela principal
        self.root = ttkb.Window(themename="cyborg")  # Tema escuro cybernético
        self.root.title("Cybernetic Video Downloader")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Cores cybernéticas
        self.colors = {
            'bg': '#0a0a0a',
            'secondary_bg': '#1a1a1a',
            'accent_orange': '#ff6b35',
            'accent_green': '#00ff88',
            'accent_purple': '#b347d9',
            'accent_blue': '#0099ff',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'border': '#333333'
        }
        
        # Configurar estilo personalizado
        self.setup_styles()
        
        # Variáveis de controle
        self.downloads_queue = []
        self.current_downloads = {}
        self.settings = self.load_settings()
        
        # Criar interface
        self.create_interface()
        
        # Configurar eventos
        self.setup_events()
        
    def setup_styles(self):
        """Configurar estilos cybernéticos personalizados"""
        style = ttkb.Style()
        
        # Estilo para frames principais
        style.configure("Cyber.TFrame", 
                       background=self.colors['bg'],
                       borderwidth=1,
                       relief="solid")
        
        # Estilo para botões
        style.configure("CyberOrange.TButton",
                       background=self.colors['accent_orange'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor="none")
        
        style.configure("CyberGreen.TButton",
                       background=self.colors['accent_green'],
                       foreground='black',
                       borderwidth=0,
                       focuscolor="none")
        
        style.configure("CyberPurple.TButton",
                       background=self.colors['accent_purple'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor="none")
        
        # Estilo para entry
        style.configure("Cyber.TEntry",
                       fieldbackground=self.colors['secondary_bg'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       bordercolor=self.colors['accent_blue'])
        
        # Estilo para labels
        style.configure("CyberTitle.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['accent_orange'],
                       font=('Consolas', 16, 'bold'))
        
        style.configure("CyberSubtitle.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['accent_green'],
                       font=('Consolas', 12, 'bold'))
        
        style.configure("CyberText.TLabel",
                       background=self.colors['bg'],
                       foreground=self.colors['text_primary'],
                       font=('Consolas', 10))
        
    def create_interface(self):
        """Criar a interface principal"""
        # Configure o fundo principal
        self.root.configure(bg=self.colors['bg'])
        
        # Header com título cybernético
        self.create_header()
        
        # Área principal dividida em painéis
        self.create_main_panels()
        
        # Barra de status
        self.create_status_bar()
        
    def create_header(self):
        """Criar cabeçalho com título e controles principais"""
        header_frame = ttk.Frame(self.root, style="Cyber.TFrame", padding=20)
        header_frame.pack(fill=X)
        
        # Título principal com efeito neon
        title_label = ttk.Label(header_frame, 
                               text="◢ CYBERNETIC VIDEO DOWNLOADER ◤",
                               style="CyberTitle.TLabel")
        title_label.pack()
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="► Download videos from YouTube, Twitch, TikTok and more ◄",
                                  style="CyberSubtitle.TLabel")
        subtitle_label.pack(pady=(5, 15))
        
        # Frame para URL input
        url_frame = ttk.Frame(header_frame, style="Cyber.TFrame")
        url_frame.pack(fill=X, pady=10)
        
        # Label para URL
        url_label = ttk.Label(url_frame, text="VIDEO URL:", style="CyberText.TLabel")
        url_label.pack(side=LEFT, padx=(0, 10))
        
        # Entry para URL
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, 
                                  textvariable=self.url_var,
                                  style="Cyber.TEntry",
                                  font=('Consolas', 11))
        self.url_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        # Botão para analisar
        self.analyze_btn = ttk.Button(url_frame,
                                     text="ANALYZE",
                                     style="CyberOrange.TButton",
                                     command=self.analyze_video)
        self.analyze_btn.pack(side=RIGHT, padx=(0, 10))
        
        # Botão para configurações
        self.settings_btn = ttk.Button(url_frame,
                                      text="SETTINGS",
                                      style="CyberPurple.TButton",
                                      command=self.open_settings)
        self.settings_btn.pack(side=RIGHT)
        
    def create_main_panels(self):
        """Criar painéis principais da interface"""
        # Container principal
        main_container = ttk.Frame(self.root, style="Cyber.TFrame")
        main_container.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Painel esquerdo - Informações do vídeo
        self.create_video_info_panel(main_container)
        
        # Painel direito - Fila de downloads
        self.create_downloads_panel(main_container)
        
    def create_video_info_panel(self, parent):
        """Painel de informações do vídeo"""
        # Frame principal
        info_frame = ttk.LabelFrame(parent, 
                                   text="► VIDEO INFO",
                                   style="Cyber.TFrame",
                                   padding=15)
        info_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # Área da thumbnail
        self.thumbnail_frame = ttk.Frame(info_frame, style="Cyber.TFrame")
        self.thumbnail_frame.pack(fill=X, pady=(0, 15))
        
        # Label para thumbnail placeholder
        self.thumbnail_label = ttk.Label(self.thumbnail_frame,
                                        text="[THUMBNAIL WILL APPEAR HERE]",
                                        style="CyberText.TLabel",
                                        anchor="center")
        self.thumbnail_label.pack(expand=True, fill=BOTH)
        
        # Informações do vídeo
        info_container = ttk.Frame(info_frame, style="Cyber.TFrame")
        info_container.pack(fill=X)
        
        # Título
        ttk.Label(info_container, text="Title:", style="CyberSubtitle.TLabel").pack(anchor=W)
        self.title_var = tk.StringVar(value="No video loaded")
        self.title_label = ttk.Label(info_container, 
                                    textvariable=self.title_var,
                                    style="CyberText.TLabel",
                                    wraplength=400)
        self.title_label.pack(anchor=W, pady=(0, 10))
        
        # Duração e tamanho em linha
        duration_size_frame = ttk.Frame(info_container, style="Cyber.TFrame")
        duration_size_frame.pack(fill=X, pady=(0, 10))
        
        # Duração
        duration_frame = ttk.Frame(duration_size_frame, style="Cyber.TFrame")
        duration_frame.pack(side=LEFT, fill=X, expand=True)
        ttk.Label(duration_frame, text="Duration:", style="CyberSubtitle.TLabel").pack(anchor=W)
        self.duration_var = tk.StringVar(value="--:--")
        ttk.Label(duration_frame, textvariable=self.duration_var, style="CyberText.TLabel").pack(anchor=W)
        
        # Tamanho estimado
        size_frame = ttk.Frame(duration_size_frame, style="Cyber.TFrame")
        size_frame.pack(side=RIGHT, fill=X, expand=True)
        ttk.Label(size_frame, text="Est. Size:", style="CyberSubtitle.TLabel").pack(anchor=W)
        self.size_var = tk.StringVar(value="-- MB")
        ttk.Label(size_frame, textvariable=self.size_var, style="CyberText.TLabel").pack(anchor=W)
        
        # Opções de qualidade e formato
        options_frame = ttk.Frame(info_frame, style="Cyber.TFrame")
        options_frame.pack(fill=X, pady=15)
        
        # Qualidade
        quality_frame = ttk.Frame(options_frame, style="Cyber.TFrame")
        quality_frame.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        ttk.Label(quality_frame, text="Quality:", style="CyberSubtitle.TLabel").pack(anchor=W)
        self.quality_var = tk.StringVar(value="best")
        self.quality_combo = ttk.Combobox(quality_frame, 
                                         textvariable=self.quality_var,
                                         values=["best", "1080p", "720p", "480p", "360p"],
                                         state="readonly")
        self.quality_combo.pack(fill=X)
        
        # Formato
        format_frame = ttk.Frame(options_frame, style="Cyber.TFrame")
        format_frame.pack(side=RIGHT, fill=X, expand=True)
        ttk.Label(format_frame, text="Format:", style="CyberSubtitle.TLabel").pack(anchor=W)
        self.format_var = tk.StringVar(value="mp4")
        self.format_combo = ttk.Combobox(format_frame,
                                        textvariable=self.format_var,
                                        values=["mp4", "mkv", "webm", "mp3", "wav"],
                                        state="readonly")
        self.format_combo.pack(fill=X)
        
        # Botão de download
        self.download_btn = ttk.Button(info_frame,
                                      text="ADD TO QUEUE",
                                      style="CyberGreen.TButton",
                                      command=self.add_to_queue,
                                      state="disabled")
        self.download_btn.pack(fill=X, pady=15)
        
    def create_downloads_panel(self, parent):
        """Painel da fila de downloads"""
        downloads_frame = ttk.LabelFrame(parent,
                                        text="► DOWNLOADS QUEUE",
                                        style="Cyber.TFrame",
                                        padding=15)
        downloads_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Controles da fila
        queue_controls = ttk.Frame(downloads_frame, style="Cyber.TFrame")
        queue_controls.pack(fill=X, pady=(0, 15))
        
        # Botões de controle
        ttk.Button(queue_controls,
                  text="START ALL",
                  style="CyberGreen.TButton",
                  command=self.start_all_downloads).pack(side=LEFT, padx=(0, 5))
        
        ttk.Button(queue_controls,
                  text="PAUSE ALL",
                  style="CyberOrange.TButton",
                  command=self.pause_all_downloads).pack(side=LEFT, padx=(0, 5))
        
        ttk.Button(queue_controls,
                  text="CLEAR COMPLETED",
                  style="CyberPurple.TButton",
                  command=self.clear_completed).pack(side=RIGHT)
        
        # Lista de downloads com scrollbar
        list_frame = ttk.Frame(downloads_frame, style="Cyber.TFrame")
        list_frame.pack(fill=BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Canvas para lista de downloads
        self.downloads_canvas = tk.Canvas(list_frame,
                                         bg=self.colors['secondary_bg'],
                                         highlightthickness=0,
                                         yscrollcommand=scrollbar.set)
        self.downloads_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.downloads_canvas.yview)
        
        # Frame interno para itens
        self.downloads_inner_frame = ttk.Frame(self.downloads_canvas, style="Cyber.TFrame")
        self.canvas_window = self.downloads_canvas.create_window((0, 0), 
                                                               window=self.downloads_inner_frame,
                                                               anchor="nw")
        
        # Bind scroll events
        self.downloads_inner_frame.bind("<Configure>", self.update_scroll_region)
        self.downloads_canvas.bind("<Configure>", self.update_canvas_width)
        
    def create_status_bar(self):
        """Criar barra de status"""
        status_frame = ttk.Frame(self.root, style="Cyber.TFrame", padding=5)
        status_frame.pack(fill=X, side=BOTTOM)
        
        # Status text
        self.status_var = tk.StringVar(value="Ready to download videos...")
        status_label = ttk.Label(status_frame,
                                textvariable=self.status_var,
                                style="CyberText.TLabel")
        status_label.pack(side=LEFT)
        
        # Contador de downloads
        self.download_count_var = tk.StringVar(value="Downloads: 0 active, 0 completed")
        count_label = ttk.Label(status_frame,
                               textvariable=self.download_count_var,
                               style="CyberText.TLabel")
        count_label.pack(side=RIGHT)
        
    def setup_events(self):
        """Configurar eventos da interface"""
        # Enter key para analisar vídeo
        self.url_entry.bind("<Return>", lambda e: self.analyze_video())
        
        # Paste event para auto-análise
        self.url_entry.bind("<Control-v>", self.on_paste)
        
    def on_paste(self, event):
        """Handler para colar URL e auto-analisar"""
        self.root.after(100, self.auto_analyze_on_paste)
        
    def auto_analyze_on_paste(self):
        """Auto-analisar após colar URL"""
        url = self.url_var.get().strip()
        if url and self.is_valid_url(url):
            self.analyze_video()
            
    def is_valid_url(self, url):
        """Verificar se URL é válida"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    def analyze_video(self):
        """Analisar vídeo da URL fornecida"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return
            
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
            
        # Desabilitar controles durante análise
        self.analyze_btn.config(state="disabled", text="ANALYZING...")
        self.download_btn.config(state="disabled")
        self.status_var.set("Analyzing video...")
        
        # Executar análise em thread separada
        thread = threading.Thread(target=self._analyze_video_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def _analyze_video_thread(self, url):
        """Thread para análise do vídeo"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extrair informações relevantes
                video_info = {
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail'),
                    'formats': info.get('formats', []),
                    'url': url,
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0)
                }
                
                # Atualizar interface na thread principal
                self.root.after(0, self._update_video_info, video_info)
                
        except Exception as e:
            error_msg = f"Failed to analyze video: {str(e)}"
            self.root.after(0, self._handle_analyze_error, error_msg)
            
    def _update_video_info(self, info):
        """Atualizar informações do vídeo na interface"""
        try:
            # Atualizar título
            self.title_var.set(info['title'][:100] + "..." if len(info['title']) > 100 else info['title'])
            
            # Atualizar duração
            duration = info['duration']
            if duration:
                hours = duration // 3600
                minutes = (duration % 3600) // 60
                seconds = duration % 60
                if hours > 0:
                    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                else:
                    duration_str = f"{minutes:02d}:{seconds:02d}"
                self.duration_var.set(duration_str)
            
            # Carregar thumbnail
            if info['thumbnail']:
                self.load_thumbnail(info['thumbnail'])
            
            # Estimar tamanho (aproximado)
            formats = info['formats']
            best_format = None
            for fmt in formats:
                if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none':
                    best_format = fmt
                    break
            
            if best_format and best_format.get('filesize'):
                size_mb = best_format['filesize'] / (1024 * 1024)
                self.size_var.set(f"{size_mb:.1f} MB")
            else:
                self.size_var.set("Unknown")
            
            # Armazenar informações para download
            self.current_video_info = info
            
            # Habilitar botão de download
            self.download_btn.config(state="normal")
            self.status_var.set("Video analyzed successfully")
            
        except Exception as e:
            self._handle_analyze_error(f"Error updating interface: {str(e)}")
        finally:
            # Reabilitar botão de análise
            self.analyze_btn.config(state="normal", text="ANALYZE")
            
    def _handle_analyze_error(self, error_msg):
        """Tratar erro na análise"""
        messagebox.showerror("Analysis Error", error_msg)
        self.analyze_btn.config(state="normal", text="ANALYZE")
        self.status_var.set("Analysis failed")
        
    def load_thumbnail(self, thumbnail_url):
        """Carregar thumbnail do vídeo"""
        try:
            thread = threading.Thread(target=self._load_thumbnail_thread, args=(thumbnail_url,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            
    def _load_thumbnail_thread(self, thumbnail_url):
        """Thread para carregar thumbnail"""
        try:
            response = requests.get(thumbnail_url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            image = image.resize((320, 180), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(image)
            
            # Atualizar na thread principal
            self.root.after(0, self._update_thumbnail, photo)
            
        except Exception as e:
            print(f"Error loading thumbnail: {e}")
            
    def _update_thumbnail(self, photo):
        """Atualizar thumbnail na interface"""
        self.thumbnail_label.config(image=photo, text="")
        self.thumbnail_label.image = photo  # Manter referência
        
    def add_to_queue(self):
        """Adicionar vídeo à fila de download"""
        if not hasattr(self, 'current_video_info'):
            messagebox.showerror("Error", "No video analyzed")
            return
            
        # Criar item da fila
        download_item = {
            'id': len(self.downloads_queue),
            'title': self.current_video_info['title'],
            'url': self.current_video_info['url'],
            'quality': self.quality_var.get(),
            'format': self.format_var.get(),
            'status': 'queued',
            'progress': 0,
            'speed': 0,
            'eta': 0,
            'downloaded': 0,
            'total': 0
        }
        
        self.downloads_queue.append(download_item)
        self.create_download_widget(download_item)
        self.update_download_count()
        
        # Limpar informações atuais
        self.clear_current_video()
        
        messagebox.showinfo("Success", "Video added to download queue!")
        
    def create_download_widget(self, download_item):
        """Criar widget para item de download"""
        # Frame principal do item
        item_frame = ttk.Frame(self.downloads_inner_frame, 
                              style="Cyber.TFrame", 
                              padding=10)
        item_frame.pack(fill=X, pady=5)
        
        # Título do vídeo
        title_label = ttk.Label(item_frame,
                               text=download_item['title'][:50] + "..." if len(download_item['title']) > 50 else download_item['title'],
                               style="CyberSubtitle.TLabel")
        title_label.pack(anchor=W)
        
        # Informações (qualidade, formato, status)
        info_frame = ttk.Frame(item_frame, style="Cyber.TFrame")
        info_frame.pack(fill=X, pady=(5, 10))
        
        info_text = f"Quality: {download_item['quality']} | Format: {download_item['format']} | Status: {download_item['status'].upper()}"
        info_label = ttk.Label(info_frame, text=info_text, style="CyberText.TLabel")
        info_label.pack(side=LEFT)
        
        # Controles
        controls_frame = ttk.Frame(info_frame, style="Cyber.TFrame")
        controls_frame.pack(side=RIGHT)
        
        start_btn = ttk.Button(controls_frame, text="START", 
                              style="CyberGreen.TButton",
                              command=lambda: self.start_download(download_item['id']))
        start_btn.pack(side=LEFT, padx=(0, 5))
        
        pause_btn = ttk.Button(controls_frame, text="PAUSE",
                              style="CyberOrange.TButton",
                              command=lambda: self.pause_download(download_item['id']))
        pause_btn.pack(side=LEFT, padx=(0, 5))
        
        remove_btn = ttk.Button(controls_frame, text="REMOVE",
                               style="CyberPurple.TButton",
                               command=lambda: self.remove_download(download_item['id']))
        remove_btn.pack(side=LEFT)
        
        # Barra de progresso
        progress_frame = ttk.Frame(item_frame, style="Cyber.TFrame")
        progress_frame.pack(fill=X, pady=(10, 0))
        
        progress_bar = ttk.Progressbar(progress_frame, 
                                      mode='determinate',
                                      style="success.Horizontal.TProgressbar")
        progress_bar.pack(fill=X, pady=(0, 5))
        
        # Informações de progresso
        progress_info = ttk.Label(progress_frame,
                                 text="Ready to start",
                                 style="CyberText.TLabel")
        progress_info.pack(anchor=W)
        
        # Armazenar referências dos widgets
        download_item['widgets'] = {
            'frame': item_frame,
            'title_label': title_label,
            'info_label': info_label,
            'start_btn': start_btn,
            'pause_btn': pause_btn,
            'remove_btn': remove_btn,
            'progress_bar': progress_bar,
            'progress_info': progress_info
        }
        
        # Atualizar scroll
        self.update_scroll_region()
        
    def start_download(self, download_id):
        """Iniciar download específico"""
        download_item = self.get_download_by_id(download_id)
        if not download_item:
            return
            
        download_item['status'] = 'downloading'
        self.update_download_widget(download_item)
        
        # Executar download em thread separada
        thread = threading.Thread(target=self._download_thread, args=(download_item,))
        thread.daemon = True
        thread.start()
        
    def _download_thread(self, download_item):
        """Thread para executar o download"""
        try:
            output_path = self.settings.get('download_path', os.path.expanduser('~/Downloads'))
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        downloaded = d.get('downloaded_bytes', 0)
                        total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                        speed = d.get('speed', 0)
                        eta = d.get('eta', 0)
                        
                        if total > 0:
                            progress = (downloaded / total) * 100
                            download_item['progress'] = progress
                            download_item['downloaded'] = downloaded
                            download_item['total'] = total
                            download_item['speed'] = speed
                            download_item['eta'] = eta
                            
                            # Atualizar interface na thread principal
                            self.root.after(0, self.update_download_widget, download_item)
                    except:
                        pass
                elif d['status'] == 'finished':
                    download_item['status'] = 'completed'
                    download_item['progress'] = 100
                    self.root.after(0, self.update_download_widget, download_item)
            
            # Configurar opções do yt-dlp
            format_selector = self._get_format_selector(download_item['quality'], download_item['format'])
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
                'progress_hooks': [progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([download_item['url']])
                
        except Exception as e:
            download_item['status'] = 'error'
            download_item['error'] = str(e)
            self.root.after(0, self.update_download_widget, download_item)
            
    def _get_format_selector(self, quality, format_type):
        """Obter seletor de formato para yt-dlp"""
        if format_type == 'mp3':
            return 'bestaudio/best'
        elif format_type == 'wav':
            return 'bestaudio[ext=wav]/bestaudio/best'
        else:
            if quality == 'best':
                return f'best[ext={format_type}]/best'
            else:
                height = quality.replace('p', '')
                return f'best[height<={height}][ext={format_type}]/best[height<={height}]/best'
        
    def update_download_widget(self, download_item):
        """Atualizar widget do download"""
        widgets = download_item.get('widgets', {})
        if not widgets:
            return
            
        try:
            # Atualizar status na label de informações
            status = download_item['status'].upper()
            quality = download_item['quality']
            format_type = download_item['format']
            
            info_text = f"Quality: {quality} | Format: {format_type} | Status: {status}"
            widgets['info_label'].config(text=info_text)
            
            # Atualizar barra de progresso
            progress = download_item.get('progress', 0)
            widgets['progress_bar']['value'] = progress
            
            # Atualizar informações de progresso
            if download_item['status'] == 'downloading':
                downloaded = download_item.get('downloaded', 0)
                total = download_item.get('total', 0)
                speed = download_item.get('speed', 0)
                eta = download_item.get('eta', 0)
                
                downloaded_mb = downloaded / (1024 * 1024)
                total_mb = total / (1024 * 1024)
                speed_mb = speed / (1024 * 1024) if speed else 0
                
                if eta:
                    eta_str = f"{eta//60}:{eta%60:02d}"
                else:
                    eta_str = "--:--"
                    
                progress_text = f"Downloading: {downloaded_mb:.1f}/{total_mb:.1f} MB | Speed: {speed_mb:.1f} MB/s | ETA: {eta_str}"
                widgets['progress_info'].config(text=progress_text)
                
                # Mudar cor da barra baseada no progresso
                if progress < 30:
                    widgets['progress_bar'].config(style="danger.Horizontal.TProgressbar")
                elif progress < 70:
                    widgets['progress_bar'].config(style="warning.Horizontal.TProgressbar")
                else:
                    widgets['progress_bar'].config(style="success.Horizontal.TProgressbar")
                    
            elif download_item['status'] == 'completed':
                widgets['progress_info'].config(text="Download completed successfully!")
                widgets['progress_bar'].config(style="success.Horizontal.TProgressbar")
                
            elif download_item['status'] == 'error':
                error_msg = download_item.get('error', 'Unknown error')
                widgets['progress_info'].config(text=f"Error: {error_msg}")
                widgets['progress_bar'].config(style="danger.Horizontal.TProgressbar")
                
            elif download_item['status'] == 'paused':
                widgets['progress_info'].config(text="Download paused")
                
            elif download_item['status'] == 'queued':
                widgets['progress_info'].config(text="Ready to start")
                
            self.update_download_count()
            
        except Exception as e:
            print(f"Error updating widget: {e}")
            
    def pause_download(self, download_id):
        """Pausar download (implementação básica)"""
        download_item = self.get_download_by_id(download_id)
        if download_item and download_item['status'] == 'downloading':
            download_item['status'] = 'paused'
            self.update_download_widget(download_item)
            
    def remove_download(self, download_id):
        """Remover download da fila"""
        download_item = self.get_download_by_id(download_id)
        if download_item:
            # Remover widget da interface
            if 'widgets' in download_item:
                download_item['widgets']['frame'].destroy()
                
            # Remover da lista
            self.downloads_queue = [d for d in self.downloads_queue if d['id'] != download_id]
            self.update_download_count()
            self.update_scroll_region()
            
    def get_download_by_id(self, download_id):
        """Obter item de download por ID"""
        for item in self.downloads_queue:
            if item['id'] == download_id:
                return item
        return None
        
    def start_all_downloads(self):
        """Iniciar todos os downloads na fila"""
        for download_item in self.downloads_queue:
            if download_item['status'] == 'queued':
                self.start_download(download_item['id'])
                
    def pause_all_downloads(self):
        """Pausar todos os downloads ativos"""
        for download_item in self.downloads_queue:
            if download_item['status'] == 'downloading':
                self.pause_download(download_item['id'])
                
    def clear_completed(self):
        """Limpar downloads concluídos"""
        completed_items = [d for d in self.downloads_queue if d['status'] == 'completed']
        for item in completed_items:
            self.remove_download(item['id'])
            
    def update_download_count(self):
        """Atualizar contador de downloads"""
        active = len([d for d in self.downloads_queue if d['status'] in ['downloading', 'queued']])
        completed = len([d for d in self.downloads_queue if d['status'] == 'completed'])
        self.download_count_var.set(f"Downloads: {active} active, {completed} completed")
        
    def clear_current_video(self):
        """Limpar informações do vídeo atual"""
        self.title_var.set("No video loaded")
        self.duration_var.set("--:--")
        self.size_var.set("-- MB")
        self.thumbnail_label.config(image="", text="[THUMBNAIL WILL APPEAR HERE]")
        self.download_btn.config(state="disabled")
        self.url_var.set("")
        
        if hasattr(self, 'current_video_info'):
            delattr(self, 'current_video_info')
            
    def update_scroll_region(self, event=None):
        """Atualizar região de scroll do canvas"""
        self.downloads_canvas.configure(scrollregion=self.downloads_canvas.bbox("all"))
        
    def update_canvas_width(self, event=None):
        """Atualizar largura do canvas"""
        canvas_width = self.downloads_canvas.winfo_width()
        self.downloads_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def open_settings(self):
        """Abrir janela de configurações"""
        settings_window = SettingsWindow(self.root, self.settings, self.save_settings)
        
    def load_settings(self):
        """Carregar configurações"""
        default_settings = {
            'download_path': os.path.expanduser('~/Downloads'),
            'concurrent_downloads': 3,
            'auto_start': False,
            'notifications': True
        }
        
        settings_file = 'settings.json'
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    saved_settings = json.load(f)
                    default_settings.update(saved_settings)
            except:
                pass
                
        return default_settings
        
    def save_settings(self, new_settings):
        """Salvar configurações"""
        self.settings.update(new_settings)
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            
    def run(self):
        """Executar aplicação"""
        self.root.mainloop()


class SettingsWindow:
    def __init__(self, parent, current_settings, save_callback):
        self.parent = parent
        self.current_settings = current_settings.copy()
        self.save_callback = save_callback
        
        # Criar janela
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("500x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Configurar estilo
        self.window.configure(bg='#0a0a0a')
        
        self.create_interface()
        
    def create_interface(self):
        """Criar interface de configurações"""
        # Título
        title_frame = ttk.Frame(self.window, padding=20)
        title_frame.pack(fill=X)
        
        title_label = ttk.Label(title_frame, 
                               text="⚙ SETTINGS",
                               font=('Consolas', 16, 'bold'),
                               foreground='#ff6b35')
        title_label.pack()
        
        # Notebook para abas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Aba General
        general_frame = ttk.Frame(notebook, padding=20)
        notebook.add(general_frame, text="General")
        
        # Download Path
        path_frame = ttk.Frame(general_frame)
        path_frame.pack(fill=X, pady=10)
        
        ttk.Label(path_frame, text="Download Path:").pack(anchor=W)
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=X, pady=5)
        
        self.path_var = tk.StringVar(value=self.current_settings.get('download_path', ''))
        path_entry = ttk.Entry(path_entry_frame, textvariable=self.path_var)
        path_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(path_entry_frame, 
                               text="Browse",
                               command=self.browse_folder)
        browse_btn.pack(side=RIGHT)
        
        # Concurrent Downloads
        concurrent_frame = ttk.Frame(general_frame)
        concurrent_frame.pack(fill=X, pady=10)
        
        ttk.Label(concurrent_frame, text="Concurrent Downloads:").pack(anchor=W)
        
        self.concurrent_var = tk.StringVar(value=str(self.current_settings.get('concurrent_downloads', 3)))
        concurrent_spinbox = ttk.Spinbox(concurrent_frame,
                                       from_=1, to=10,
                                       textvariable=self.concurrent_var,
                                       width=10)
        concurrent_spinbox.pack(anchor=W, pady=5)
        
        # Checkboxes
        self.auto_start_var = tk.BooleanVar(value=self.current_settings.get('auto_start', False))
        auto_start_check = ttk.Checkbutton(general_frame,
                                         text="Auto-start downloads",
                                         variable=self.auto_start_var)
        auto_start_check.pack(anchor=W, pady=5)
        
        self.notifications_var = tk.BooleanVar(value=self.current_settings.get('notifications', True))
        notifications_check = ttk.Checkbutton(general_frame,
                                            text="Show notifications",
                                            variable=self.notifications_var)
        notifications_check.pack(anchor=W, pady=5)
        
        # Botões
        buttons_frame = ttk.Frame(self.window, padding=20)
        buttons_frame.pack(fill=X, side=BOTTOM)
        
        ttk.Button(buttons_frame,
                  text="Cancel",
                  command=self.window.destroy).pack(side=RIGHT, padx=(5, 0))
        
        ttk.Button(buttons_frame,
                  text="Save",
                  command=self.save_settings).pack(side=RIGHT)
        
    def browse_folder(self):
        """Procurar pasta de download"""
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)
            
    def save_settings(self):
        """Salvar configurações"""
        new_settings = {
            'download_path': self.path_var.get(),
            'concurrent_downloads': int(self.concurrent_var.get()),
            'auto_start': self.auto_start_var.get(),
            'notifications': self.notifications_var.get()
        }
        
        self.save_callback(new_settings)
        self.window.destroy()


if __name__ == "__main__":
    app = CyberneticVideoDownloader()
    app.run()