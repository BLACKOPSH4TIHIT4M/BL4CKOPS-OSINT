#!/bin/bash
# BL4CKOPS OSINT - Auto TOR Startup Script

echo "=================================="
echo "BL4CKOPS OSINT - TOR Auto Setup"
echo "=================================="
echo ""

# Check if TOR is already running
echo "[*] Checking TOR service..."
if command -v nc &> /dev/null; then
    if nc -z 127.0.0.1 9050 2>/dev/null; then
        echo "[✓] TOR already running on port 9050"
    else
        echo "[*] Starting TOR service..."
        tor --SocksPort 9050 --RunAsDaemon 1
        
        # Wait for TOR to start
        for i in {1..20}; do
            if nc -z 127.0.0.1 9050 2>/dev/null; then
                echo "[✓] TOR service started successfully"
                break
            fi
            echo "[*] Waiting for TOR... ($i/20)"
            sleep 1
        done
    fi
elif command -v timeout &> /dev/null; then
    # Alternative check using timeout and exec
    if timeout 1 bash -c "cat < /dev/null > /dev/tcp/127.0.0.1/9050" 2>/dev/null; then
        echo "[✓] TOR already running on port 9050"
    else
        echo "[*] Starting TOR service..."
        tor --SocksPort 9050 --RunAsDaemon 1
        sleep 5
        echo "[✓] TOR service started"
    fi
else
    echo "[!] Warning: Cannot check TOR status reliably"
    echo "[*] Attempting to start TOR service..."
    tor --SocksPort 9050 --RunAsDaemon 1
    sleep 5
fi

echo ""
echo "[*] Starting BL4CKOPS OSINT..."
echo ""

# Run Python script
cd /home/h4tihit4m/BL4CKOPS_REVEALED
python bl4ckops_osint.py

# Cleanup
echo ""
echo "[*] Stopping TOR service..."
pkill -f "tor --SocksPort" 2>/dev/null || true
echo "[✓] Done"
echo "║  Docs:  SETUP_COMPLETE.md  |  TOR_BROWSER_SETUP.md         ║"
echo "║  Logs:  backend.log        |  frontend.log                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Open your browser to http://localhost:3000"
echo ""
