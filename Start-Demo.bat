@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AMB+ Demo
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 demo_start.py
  goto ende
)
python -c "import sys" >nul 2>nul
if %errorlevel%==0 (
  python demo_start.py
  goto ende
)
echo.
echo Python ist auf diesem Rechner nicht installiert.
echo Bitte von https://www.python.org/downloads/ installieren
echo und beim Installieren "Add python.exe to PATH" ankreuzen.
echo Danach diese Datei erneut doppelklicken.
echo.
start https://www.python.org/downloads/
:ende
pause
