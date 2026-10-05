@echo off
title AI-Powered Learning Path System Launcher
echo ======================================================================
echo Launching AI-Powered Personalized Learning Path Generation System...
echo ======================================================================
echo.
echo [1/2] Starting Python AI Backend Server (Port 5000)...
start "AI Learning Path Backend" cmd /k "cd /d %~dp0 && python -m backend.app"
timeout /t 3 /nobreak >nul
echo.
echo [2/2] Starting React Vite Frontend (Port 5173)...
start "AI Learning Path Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
echo.
echo ======================================================================
echo Both servers are starting up!
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:5000
echo Demo Login: alex.morgan@example.com / password123
echo ======================================================================
pause
