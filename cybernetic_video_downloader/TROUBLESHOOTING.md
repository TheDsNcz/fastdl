# Cybernetic Video Downloader - Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Python Not Found
**Problem**: `'python' is not recognized as an internal or external command`
**Solution**: 
1. Install Python from https://python.org
2. During installation, check "Add Python to PATH"
3. Restart command prompt and try again

#### Dependency Installation Fails
**Problem**: `pip install` commands fail
**Solution**:
1. Update pip: `python -m pip install --upgrade pip`
2. Check internet connection
3. Try running as administrator
4. Use: `python -m pip install --user -r requirements.txt`

### Runtime Issues

#### Video Analysis Fails
**Problem**: "Failed to analyze video" error
**Solutions**:
1. Check if URL is valid and accessible
2. Update yt-dlp: run `update.bat`
3. Check internet connection
4. Some videos may be region-restricted

#### Download Fails
**Problem**: Downloads start but fail immediately
**Solutions**:
1. Check available disk space
2. Verify download folder permissions
3. Try different quality/format settings
4. Update yt-dlp and dependencies

#### Slow Download Speeds
**Problem**: Downloads are very slow
**Solutions**:
1. Check your internet connection
2. Try different times of day
3. Consider your ISP's throttling policies
4. Close other bandwidth-heavy applications

### Interface Issues

#### Interface Looks Wrong
**Problem**: Colors or layout appear incorrect
**Solutions**:
1. Ensure all dependencies are installed
2. Update ttkbootstrap: `pip install --upgrade ttkbootstrap`
3. Try running with different theme settings

#### Thumbnails Don't Load
**Problem**: Video thumbnails appear as placeholder text
**Solutions**:
1. Check internet connection
2. Verify PIL/Pillow installation
3. Some videos may not have thumbnails available

### Performance Issues

#### High CPU Usage
**Problem**: Application uses too much CPU
**Solutions**:
1. Reduce concurrent downloads in settings
2. Close unnecessary applications
3. Restart the application periodically

#### Memory Issues
**Problem**: Application becomes unresponsive
**Solutions**:
1. Clear completed downloads regularly
2. Restart application for long sessions
3. Ensure adequate RAM available

## Advanced Troubleshooting

### Enable Debug Mode
1. Open `main.py` in text editor
2. Find the logging configuration section
3. Change log level to DEBUG
4. Check `cyber_downloader.log` for detailed information

### Manual Dependency Check
Run these commands to verify installations:
```
python -c "import yt_dlp; print('yt-dlp:', yt_dlp.__version__)"
python -c "import PIL; print('PIL:', PIL.__version__)"
python -c "import ttkbootstrap; print('ttkbootstrap installed')"
python -c "import requests; print('requests installed')"
```

### Completely Reset Application
1. Delete `settings.json`
2. Delete `cyber_config.json`
3. Delete `cyber_downloads.db`
4. Restart application

### Platform-Specific Issues

#### Windows Defender/Antivirus
Some antivirus software may flag the application:
1. Add exception for the application folder
2. Ensure Python and pip are allowed through firewall

#### Network Restrictions
If behind corporate firewall:
1. Configure proxy settings if needed
2. Contact IT department about yt-dlp requirements
3. May need to whitelist certain domains

## Getting Help

### Log Files
Check these files for error information:
- `cyber_downloader.log` - Application log
- Console output when running from command line

### Reporting Issues
When reporting problems, please include:
1. Operating system version
2. Python version (`python --version`)
3. Error message (exact text)
4. Steps to reproduce the issue
5. Log file contents if available

### Useful Commands
```bat
# Check Python version
python --version

# Update all dependencies
python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt

# Test video URL manually
python -c "import yt_dlp; yt_dlp.YoutubeDL().extract_info('YOUR_URL', download=False)"

# Clear pip cache
python -m pip cache purge
```

## Known Limitations

1. Some platforms may block automated downloads
2. Region-restricted content cannot be downloaded
3. Private/premium content requires authentication
4. Very long playlists may take time to process
5. Some live streams cannot be downloaded

## Performance Tips

1. Use lower quality settings for faster downloads
2. Limit concurrent downloads based on your connection
3. Close other applications during large downloads
4. Use SSD storage for better performance
5. Ensure stable internet connection