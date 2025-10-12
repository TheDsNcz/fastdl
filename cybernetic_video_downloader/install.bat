@echo off
echo ===================================================
echo   CYBERNETIC VIDEO DOWNLOADER - INSTALLER
echo ===================================================
echo.
echo Installing dependencies and setting up the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Found Python version: %PYTHON_VERSION%

REM Install required packages
echo.
echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

REM Create desktop shortcut (optional)
echo.
set /p CREATE_SHORTCUT="Create desktop shortcut? (y/n): "
if /i "%CREATE_SHORTCUT%"=="y" (
    echo Creating desktop shortcut...
    
    set CURRENT_DIR=%~dp0
    set SHORTCUT_TARGET="%CURRENT_DIR%launch.bat"
    set DESKTOP=%USERPROFILE%\Desktop
    
    REM Create VBS script to create shortcut
    echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
    echo sLinkFile = "%DESKTOP%\Cybernetic Video Downloader.lnk" >> CreateShortcut.vbs
    echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
    echo oLink.TargetPath = %SHORTCUT_TARGET% >> CreateShortcut.vbs
    echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> CreateShortcut.vbs
    echo oLink.Description = "Cybernetic Video Downloader" >> CreateShortcut.vbs
    echo oLink.Save >> CreateShortcut.vbs
    
    cscript CreateShortcut.vbs >nul
    del CreateShortcut.vbs
    
    echo Desktop shortcut created successfully!
)

echo.
echo ===================================================
echo   INSTALLATION COMPLETED SUCCESSFULLY!
echo ===================================================
echo.
echo You can now run the application using launch.bat
echo or double-click the desktop shortcut if created.
echo.
pause