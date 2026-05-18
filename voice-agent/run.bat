@echo off
setlocal
cd /d "%~dp0"
"%~dp0venv\Scripts\python.exe" agent.py %*
exit /b %ERRORLEVEL%
