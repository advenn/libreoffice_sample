#!/bin/bash
set -e

echo "Container startup: Checking LibreOffice installation..."

# Check if LibreOffice is available
if ! command -v /usr/local/bin/libreoffice-generic &>/dev/null; then
    echo "LibreOffice not found. Attempting runtime installation..."
    /usr/local/bin/install_libre.sh
else
    echo "LibreOffice found. Running verification..."
    /usr/local/bin/libreoffice-generic --headless --version || true
fi

# Start FastAPI with uvicorn
echo "Starting FastAPI..."
exec python3 -m uvicorn web.app:app --host 0.0.0.0 --port 8000
