#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 ist nicht installiert. Bitte von https://www.python.org/downloads/ installieren."
  open "https://www.python.org/downloads/"
  read -p "Enter zum Schliessen"
  exit 1
fi
python3 demo_start.py
read -p "Enter zum Schliessen"
