@echo off
title AUREON - Command Center Launcher
color 0E

echo ==========================================================
echo       STARTING AUREON COMMAND CENTER
echo ==========================================================
echo.
echo [1/3] Activating virtual environment...

:: Check for virtual environment folder
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Active: Virtual environment (.venv) enabled.
) else (
    echo Warning: Virtual environment (.venv) not found. Trying global Python...
)

echo.
echo [2/3] Launching Web Browser Dashboard...
start http://127.0.0.1:7999/

echo.
echo [3/3] Starting FastAPI Web Server...
echo.
echo ----------------------------------------------------------
echo Keep this terminal window open to keep the server running!
echo ----------------------------------------------------------
echo.

:: Run python module
python -m app.main

pause
