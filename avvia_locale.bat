@echo off
REM Avvia un server locale per testare la dashboard (Windows)
cd /d "%~dp0"
echo Cinema Dashboard - server locale su http://localhost:8000
echo Premi Ctrl+C per fermare.
python -m http.server 8000
pause
