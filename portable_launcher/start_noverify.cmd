@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_noverify.ps1"
if errorlevel 1 (
  pause
  exit /b 1
)
echo.
echo Press any key to close this window.
pause >nul
