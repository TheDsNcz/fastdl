"""
Teste básico das funcionalidades do Cybernetic Video Downloader
"""

import sys
import os

def test_dependencies():
    """Testar se todas as dependências estão instaladas"""
    print("🔧 Testing Dependencies...")
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError:
        print("❌ tkinter - FAILED")
        
    try:
        import ttkbootstrap
        print("✅ ttkbootstrap - OK")
    except ImportError:
        print("❌ ttkbootstrap - FAILED")
        
    try:
        import yt_dlp
        print(f"✅ yt-dlp - OK (version: {yt_dlp.__version__})")
    except ImportError:
        print("❌ yt-dlp - FAILED")
        
    try:
        import PIL
        print(f"✅ PIL/Pillow - OK (version: {PIL.__version__})")
    except ImportError:
        print("❌ PIL/Pillow - FAILED")
        
    try:
        import requests
        print(f"✅ requests - OK (version: {requests.__version__})")
    except ImportError:
        print("❌ requests - FAILED")

def test_basic_functionality():
    """Testar funcionalidades básicas"""
    print("\n🧪 Testing Basic Functionality...")
    
    try:
        # Test yt-dlp with a simple URL
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        # Test URL (YouTube's own channel)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            print(f"✅ Video extraction - OK (Title: {info.get('title', 'Unknown')[:50]}...)")
            
    except Exception as e:
        print(f"❌ Video extraction - FAILED ({str(e)[:100]}...)")

def test_gui():
    """Testar se a GUI pode ser criada"""
    print("\n🖥️  Testing GUI Creation...")
    
    try:
        import tkinter as tk
        import ttkbootstrap as ttkb
        
        # Create a simple test window
        root = ttkb.Window(themename="cyborg")
        root.title("Test Window")
        root.geometry("300x200")
        
        label = ttkb.Label(root, text="GUI Test Successful!")
        label.pack(pady=50)
        
        # Don't show the window, just test creation
        root.withdraw()
        root.destroy()
        
        print("✅ GUI Creation - OK")
        
    except Exception as e:
        print(f"❌ GUI Creation - FAILED ({str(e)[:100]}...)")

def main():
    """Executar todos os testes"""
    print("🚀 Cybernetic Video Downloader - System Test")
    print("=" * 50)
    
    test_dependencies()
    test_basic_functionality()
    test_gui()
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("\nIf all tests passed, you can run the main application with:")
    print("python main.py")
    print("\nOr use the launcher:")
    print("launch.bat")

if __name__ == "__main__":
    main()