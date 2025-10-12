@echo off
echo Checking for updates...
python -m pip install --upgrade yt-dlp
python -m pip install --upgrade -r requirements.txt
echo Updates complete!
pause