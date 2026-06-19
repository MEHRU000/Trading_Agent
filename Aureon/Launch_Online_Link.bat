@echo off
title AUREON - Online Link Launcher
color 0A

echo ==========================================================
echo       STARTING SECURE ONLINE TUNNEL FOR AUREON
echo ==========================================================
echo.
echo [1/2] Activating virtual environment...

:: Check for virtual environment folder
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Active: Virtual environment (.venv) enabled.
) else (
    echo Warning: Virtual environment (.venv) not found. Trying global Python...
)

echo.
echo [2/2] Exposing local server port 7999 to secure URL...
python expose_dashboard.py

pause
