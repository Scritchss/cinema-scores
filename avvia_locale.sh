#!/bin/bash
# Avvia un server locale per testare la dashboard
cd "$(dirname "$0")"
echo "🎬 Cinema Dashboard — server locale su http://localhost:8000"
echo "   Premi Ctrl+C per fermare."
python3 -m http.server 8000
