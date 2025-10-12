# Cybernetic Video Downloader - Quick Start Guide

## 📥 Installation

1. **Download** all files to a folder on your Windows computer
2. **Run** `install.bat` as administrator
3. **Launch** the application using `launch.bat`

## 🚀 Quick Start

### Step 1: Launch the Application
Double-click `launch.bat` or run from command line:
```
cd cybernetic_video_downloader
launch.bat
```

### Step 2: Enter Video URL
- Copy video URL from YouTube, Twitch, TikTok, etc.
- Paste into the URL field
- Click "ANALYZE" or press Enter

### Step 3: Configure Download
- Select desired quality (best, 1080p, 720p, etc.)
- Choose format (mp4, mkv, mp3, etc.)
- Review video information and thumbnail

### Step 4: Download
- Click "ADD TO QUEUE" to add to download list
- Use "START ALL" to begin all downloads
- Monitor progress in real-time

## ⚙️ Features Overview

### Core Features
- **Multi-Platform Support**: YouTube, Twitch, TikTok, Instagram, Twitter, and 1000+ sites
- **Real-Time Progress**: Speed, ETA, and bytes downloaded
- **Queue Management**: Multiple downloads with pause/resume/cancel
- **Quality Selection**: Choose from available video/audio qualities
- **Format Options**: MP4, MKV, WebM for video; MP3, WAV for audio

### Interface Features
- **Cybernetic Design**: Futuristic dark theme with neon accents
- **Live Thumbnails**: Preview images loaded automatically
- **Video Information**: Title, duration, estimated size
- **Responsive Layout**: Adapts to window resizing

### Advanced Features
- **Download History**: SQLite database tracking
- **Settings Panel**: Customize paths, concurrent downloads, etc.
- **Error Recovery**: Automatic retry on failures
- **Logging System**: Detailed logs for troubleshooting

## 🎨 Interface Guide

### Main Window Layout
```
┌─────────────────────────────────────────────┐
│ ◢ CYBERNETIC VIDEO DOWNLOADER ◤             │
│ ► Download videos from YouTube, Twitch... ◄ │
├─────────────────────────────────────────────┤
│ URL: [________________] [ANALYZE] [SETTINGS] │
├─────────────────────────────────────────────┤
│ ┌─── VIDEO INFO ──┐ ┌─── DOWNLOADS QUEUE ──┐│
│ │ [THUMBNAIL]     │ │ [START ALL] [PAUSE]  ││
│ │                 │ │ [CLEAR COMPLETED]    ││
│ │ Title: ...      │ │                      ││
│ │ Duration: ...   │ │ ┌─ Download Item 1 ─┐││
│ │ Size: ...       │ │ │ Video Title      │││
│ │                 │ │ │ [▓▓▓▓▓░░░] 67%   │││
│ │ Quality: [▼]    │ │ │ [START][PAUSE]   │││
│ │ Format:  [▼]    │ │ └─────────────────┘││
│ │                 │ │ ┌─ Download Item 2 ─┐││
│ │ [ADD TO QUEUE]  │ │ │ Another Video    │││
│ └─────────────────┘ │ │ Queued           │││
│                     │ └─────────────────┘││
│                     └─────────────────────┘│
├─────────────────────────────────────────────┤
│ Status: Ready... Downloads: 2 active, 1... │
└─────────────────────────────────────────────┘
```

### Color Scheme
- **Background**: Deep black (#0a0a0a)
- **Secondary**: Dark gray (#1a1a1a)
- **Orange Accent**: #ff6b35 (buttons, titles)
- **Green Accent**: #00ff88 (success, active)
- **Purple Accent**: #b347d9 (settings, special)
- **Blue Accent**: #0099ff (links, info)

## 📋 Usage Examples

### Example 1: Download YouTube Video
```
1. Copy: https://youtube.com/watch?v=VIDEO_ID
2. Paste in URL field → Click ANALYZE
3. Select quality: 1080p, format: mp4
4. Click ADD TO QUEUE → START ALL
```

### Example 2: Download Audio Only
```
1. Enter any supported video URL
2. After analysis, select format: mp3
3. Quality automatically becomes "best audio"
4. Download as usual
```

### Example 3: Batch Downloads
```
1. Analyze first video → Add to queue
2. Change URL, analyze second → Add to queue
3. Repeat for more videos
4. Use START ALL for simultaneous downloads
```

## ⚡ Keyboard Shortcuts

- **Enter** in URL field: Analyze video
- **Ctrl+V** in URL field: Auto-analyze after paste
- **Ctrl+S**: Open settings (when implemented)
- **F5**: Refresh/restart analysis

## 🛠️ Troubleshooting Quick Fixes

### Common Issues
1. **"Python not found"** → Run install.bat as admin
2. **Analysis fails** → Check URL, update with update.bat
3. **Slow downloads** → Reduce concurrent downloads in settings
4. **Interface issues** → Restart application

### Update Dependencies
Run `update.bat` regularly to keep yt-dlp updated for latest site compatibility.

## 📁 File Structure
```
cybernetic_video_downloader/
├── main.py              # Main application
├── cyber_utils.py       # Utilities and animations
├── cyber_advanced.py    # Advanced features
├── requirements.txt     # Python dependencies
├── install.bat         # Installation script
├── launch.bat          # Application launcher
├── update.bat          # Update dependencies
├── README.md           # Full documentation
├── CHANGELOG.md        # Version history
└── TROUBLESHOOTING.md  # Detailed troubleshooting
```

## 🎯 Pro Tips

1. **Quality Selection**: "best" automatically selects highest available
2. **Format Priority**: MP4 works on most devices, MKV for quality
3. **Audio Extraction**: Choose MP3/WAV format for audio-only downloads
4. **Batch Processing**: Add multiple videos before starting downloads
5. **Monitor Progress**: Watch the real-time speed and ETA displays
6. **Error Recovery**: Failed downloads can be restarted individually

## 🔧 Advanced Configuration

### Settings Panel Options
- **Download Path**: Choose where files are saved
- **Concurrent Downloads**: Number of simultaneous downloads
- **Auto-start**: Begin downloads immediately when added
- **Notifications**: Enable completion alerts

### Custom Configuration
Edit `cyber_config.json` for advanced settings like retry attempts, timeouts, and appearance options.

---

**Enjoy your cybernetic downloading experience!** 🚀✨