# Cybernetic Video Downloader - Utilities
"""
Funções utilitárias para o downloader de vídeos cybernético
"""

import os
import json
import hashlib
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import time

class CyberAnimations:
    """Classe para animações cybernéticas"""
    
    @staticmethod
    def glow_effect(widget, color="#00ff88", duration=1000):
        """Efeito de brilho cybernético em widget"""
        def animate():
            try:
                original_bg = widget.cget('background')
                steps = 20
                for i in range(steps):
                    # Fade in
                    alpha = i / steps
                    new_color = CyberAnimations.blend_colors(original_bg, color, alpha)
                    widget.configure(background=new_color)
                    widget.update()
                    time.sleep(duration / 1000 / steps / 2)
                    
                for i in range(steps, 0, -1):
                    # Fade out
                    alpha = i / steps
                    new_color = CyberAnimations.blend_colors(original_bg, color, alpha)
                    widget.configure(background=new_color)
                    widget.update()
                    time.sleep(duration / 1000 / steps / 2)
                    
                widget.configure(background=original_bg)
            except:
                pass
                
        thread = threading.Thread(target=animate)
        thread.daemon = True
        thread.start()
        
    @staticmethod
    def blend_colors(color1, color2, alpha):
        """Misturar duas cores"""
        try:
            # Converter cores hex para RGB
            if color1.startswith('#'):
                r1, g1, b1 = tuple(int(color1[1:][i:i+2], 16) for i in (0, 2, 4))
            else:
                return color2
                
            if color2.startswith('#'):
                r2, g2, b2 = tuple(int(color2[1:][i:i+2], 16) for i in (0, 2, 4))
            else:
                return color1
                
            # Blend
            r = int(r1 * (1 - alpha) + r2 * alpha)
            g = int(g1 * (1 - alpha) + g2 * alpha)
            b = int(b1 * (1 - alpha) + b2 * alpha)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color2
            
    @staticmethod
    def pulse_progress_bar(progress_bar, color="#ff6b35"):
        """Efeito de pulso na barra de progresso"""
        def pulse():
            try:
                for i in range(10):
                    progress_bar.configure(style="warning.Horizontal.TProgressbar")
                    progress_bar.update()
                    time.sleep(0.1)
                    progress_bar.configure(style="success.Horizontal.TProgressbar")
                    progress_bar.update()
                    time.sleep(0.1)
            except:
                pass
                
        thread = threading.Thread(target=pulse)
        thread.daemon = True
        thread.start()


class CyberUtils:
    """Utilitários cybernéticos"""
    
    @staticmethod
    def format_bytes(bytes_value):
        """Formatar bytes em formato legível"""
        if bytes_value == 0:
            return "0 B"
            
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
        
    @staticmethod
    def format_speed(bytes_per_second):
        """Formatar velocidade de download"""
        return f"{CyberUtils.format_bytes(bytes_per_second)}/s"
        
    @staticmethod
    def format_time(seconds):
        """Formatar tempo em formato legível"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds//60:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"
            
    @staticmethod
    def generate_hash(text):
        """Gerar hash único para texto"""
        return hashlib.md5(text.encode()).hexdigest()[:8]
        
    @staticmethod
    def validate_filename(filename):
        """Validar e corrigir nome de arquivo"""
        # Caracteres inválidos no Windows
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
        
    @staticmethod
    def create_cyber_notification(title, message, notification_type="info"):
        """Criar notificação com estilo cybernético"""
        def show_notification():
            # Criar janela de notificação personalizada
            notification = tk.Toplevel()
            notification.title("Cyber Notification")
            notification.geometry("400x150")
            notification.resizable(False, False)
            notification.configure(bg='#0a0a0a')
            
            # Remover decorações da janela
            notification.overrideredirect(True)
            
            # Posicionar no canto inferior direito
            x = notification.winfo_screenwidth() - 420
            y = notification.winfo_screenheight() - 200
            notification.geometry(f"400x150+{x}+{y}")
            
            # Frame principal
            main_frame = tk.Frame(notification, bg='#1a1a1a', relief='solid', bd=1)
            main_frame.pack(fill='both', expand=True, padx=2, pady=2)
            
            # Título
            title_label = tk.Label(main_frame, 
                                  text=title,
                                  font=('Consolas', 12, 'bold'),
                                  fg='#ff6b35',
                                  bg='#1a1a1a')
            title_label.pack(pady=(10, 5))
            
            # Mensagem
            message_label = tk.Label(main_frame,
                                   text=message,
                                   font=('Consolas', 10),
                                   fg='#ffffff',
                                   bg='#1a1a1a',
                                   wraplength=350)
            message_label.pack(pady=(0, 10))
            
            # Botão fechar
            close_btn = tk.Button(main_frame,
                                text="✕",
                                font=('Consolas', 12, 'bold'),
                                fg='#ff6b35',
                                bg='#2a2a2a',
                                activebackground='#ff6b35',
                                activeforeground='#000000',
                                relief='flat',
                                bd=0,
                                command=notification.destroy)
            close_btn.place(relx=0.95, rely=0.05, anchor='ne')
            
            # Auto-fechar após 5 segundos
            notification.after(5000, notification.destroy)
            
            # Efeito de fade in
            notification.attributes('-alpha', 0)
            notification.update()
            
            for i in range(20):
                alpha = i / 20
                notification.attributes('-alpha', alpha)
                notification.update()
                time.sleep(0.05)
        
        # Executar em thread separada
        thread = threading.Thread(target=show_notification)
        thread.daemon = True
        thread.start()


class CyberLogger:
    """Sistema de log cybernético"""
    
    def __init__(self, log_file="cyber_downloader.log"):
        self.log_file = log_file
        self.max_size = 10 * 1024 * 1024  # 10MB
        
    def log(self, message, level="INFO"):
        """Registrar mensagem no log"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] [{level}] {message}\n"
            
            # Verificar tamanho do arquivo
            if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > self.max_size:
                self._rotate_log()
                
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Logging error: {e}")
            
    def _rotate_log(self):
        """Rotacionar arquivo de log"""
        try:
            if os.path.exists(self.log_file):
                backup_file = f"{self.log_file}.old"
                if os.path.exists(backup_file):
                    os.remove(backup_file)
                os.rename(self.log_file, backup_file)
        except:
            pass
            
    def info(self, message):
        """Log de informação"""
        self.log(message, "INFO")
        
    def warning(self, message):
        """Log de aviso"""
        self.log(message, "WARNING")
        
    def error(self, message):
        """Log de erro"""
        self.log(message, "ERROR")
        
    def debug(self, message):
        """Log de debug"""
        self.log(message, "DEBUG")


class CyberConfig:
    """Gerenciador de configurações cybernéticas"""
    
    def __init__(self, config_file="cyber_config.json"):
        self.config_file = config_file
        self.default_config = {
            "appearance": {
                "theme": "cyborg",
                "animations": True,
                "glow_effects": True,
                "transparency": False
            },
            "downloads": {
                "max_concurrent": 3,
                "retry_attempts": 3,
                "timeout": 300,
                "auto_start": False,
                "auto_clear_completed": False
            },
            "paths": {
                "download_folder": os.path.expanduser("~/Downloads/CyberDownloader"),
                "temp_folder": os.path.expanduser("~/Downloads/CyberDownloader/temp")
            },
            "formats": {
                "preferred_video": "mp4",
                "preferred_audio": "mp3",
                "quality_preference": "best"
            },
            "notifications": {
                "enabled": True,
                "sound": True,
                "completion_notify": True,
                "error_notify": True
            }
        }
        
        self.config = self.load_config()
        
    def load_config(self):
        """Carregar configurações"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge com configurações padrão
                    config = self.default_config.copy()
                    self._deep_update(config, loaded_config)
                    return config
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config.copy()
            
    def save_config(self):
        """Salvar configurações"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
            
    def get(self, key_path, default=None):
        """Obter valor de configuração por caminho (ex: 'downloads.max_concurrent')"""
        try:
            keys = key_path.split('.')
            value = self.config
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
            
    def set(self, key_path, value):
        """Definir valor de configuração por caminho"""
        try:
            keys = key_path.split('.')
            config = self.config
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            config[keys[-1]] = value
            return True
        except Exception as e:
            print(f"Error setting config: {e}")
            return False
            
    def _deep_update(self, base_dict, update_dict):
        """Atualização profunda de dicionário"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value


# Instâncias globais
cyber_logger = CyberLogger()
cyber_config = CyberConfig()
cyber_utils = CyberUtils()
cyber_animations = CyberAnimations()