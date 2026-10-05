@echo off
title Python AI Learning Path Backend Server
echo ===================================================
echo Starting AI Learning Path Backend (Flask API)
echo ===================================================
cd /d "%~dp0"
python -m backend.app
pause
