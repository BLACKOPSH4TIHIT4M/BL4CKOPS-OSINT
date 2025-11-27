#!/bin/bash
# BL4CKOPS OSINT - Start All Services Script
# Usage: chmod +x start.sh && ./start.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   BL4CKOPS OSINT - Starting All Services                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Kill any existing processes
echo "[1/4] Cleaning up old processes..."
pkill -f "uvicorn\|next dev" 2>/dev/null || true
sleep 2

# Start Backend
echo "[2/4] Starting Backend (port 8000)..."
cd /home/h4tihit4m/BL4CKOPS_REVEALED
source bin/activate
nohup uvicorn backend.api:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
sleep 3
echo "✓ Backend ready at http://127.0.0.1:8000"

# Start Frontend
echo "[3/4] Starting Frontend (port 3000)..."
cd /home/h4tihit4m/Downloads/bl4ckops-osint-gui-customization-main
npm run dev > frontend.log 2>&1 &
sleep 5
echo "✓ Frontend ready at http://localhost:3000"

# Start Tor (optional)
echo "[4/4] Checking Tor..."
if sudo systemctl is-active --quiet tor; then
    echo "✓ Tor already running on 127.0.0.1:9050"
elif ps aux | grep -q "[t]or "; then
    echo "✓ Tor daemon already running"
else
    echo "⚠ Tor not running (optional for browser use)"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✅ ALL SERVICES READY                     ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Backend:      http://127.0.0.1:8000/health                ║"
echo "║  Frontend:     http://localhost:3000                       ║"
echo "║  Frontend LAN: http://192.168.1.9:3000                    ║"
echo "║  Tor Proxy:    127.0.0.1:9050 (browser only, optional)    ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║  Docs:  SETUP_COMPLETE.md  |  TOR_BROWSER_SETUP.md         ║"
echo "║  Logs:  backend.log        |  frontend.log                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Open your browser to http://localhost:3000"
echo ""
