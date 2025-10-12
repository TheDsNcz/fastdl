@echo off
title Cybernetic Video Downloader
color 0A

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                                                              ║
echo    ║    ██████╗██╗   ██╗██████╗ ███████╗██████╗                   ║
echo    ║   ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗                  ║
echo    ║   ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝                  ║
echo    ║   ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗                  ║
echo    ║   ╚██████╗   ██║   ██████╔╝███████╗██║  ██║                  ║
echo    ║    ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝                  ║
echo    ║                                                              ║
echo    ║           VIDEO DOWNLOADER - CYBERNETIC EDITION              ║
echo    ║                                                              ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
echo    Starting Cybernetic Video Downloader...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR: Python not found!
    echo    Please run install.bat first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist main.py (
    echo    ERROR: main.py not found!
    echo    Please make sure all files are in the correct location.
    echo.
    pause
    exit /b 1
)

REM Launch the application
echo    Launching application...
echo.
python main.py

REM If we get here, the application has closed
echo.
echo    Application closed.
echo    Press any key to exit...
pause >nul