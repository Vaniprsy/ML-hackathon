#!/usr/bin/env bash
# Laptop 2: serve the evaluator UI over http (needed so map tiles load), port 8080.
set -euo pipefail
cd "$(dirname "$0")/ui"
echo "Open http://localhost:8080 in the browser, then set the API address to http://<laptop-1-ip>:8000"
exec python3 -m http.server 8080
