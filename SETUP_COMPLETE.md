# BL4CKOPS OSINT - Complete Setup Guide

## ✅ Status
- ✓ Backend API running on `0.0.0.0:8000` (LAN accessible)
- ✓ Frontend UI running on `localhost:3001` (or `192.168.1.9:3001`)
- ✓ Tor daemon running on `127.0.0.1:9050` (for browser use)
- ✓ All 4 OSINT modules (files, mails, numbers, person) operational
- ✓ Favicon fixed (build error resolved)

---

## 🚀 Quick Start

### 1. Verify Everything is Running

```bash
# Backend
curl http://127.0.0.1:8000/health

# Frontend (open in browser)
# Option A (localhost): http://localhost:3001
# Option B (LAN):       http://192.168.1.9:3001
```

### 2. Test OSINT Modules

```bash
# Simulate Mode (No Google blocking)
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "module": "files",
    "target": "example.com",
    "mode": "simulate"
  }'

# Live Mode (requires authorization)
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "module": "person",
    "target": "john_doe",
    "mode": "live",
    "authorization_confirm": "I confirm I have authorization"
  }'
```

### 3. Use Frontend UI

1. Open http://localhost:3001
2. Select module (files/mails/numbers/person)
3. Enter target domain/query
4. Click "Run"
5. View results in terminal widget

---

## 🔒 Tor Setup (For Browser Only)

### Quick Setup
```bash
# Start Tor daemon (if not auto-started)
sudo tor &

# Verify Tor is listening
netstat -ln | grep 9050
# Expected: tcp 0 0 127.0.0.1:9050 0.0.0.0:* LISTEN
```

### Firefox + Tor (Manual)
1. Settings → Network Settings
2. Manual Proxy Configuration
   - SOCKS Host: `127.0.0.1`
   - Port: `9050`
   - SOCKS v5: ✓
3. Test: https://check.torproject.org

### Tor Browser
```bash
# Kali Linux
sudo apt install torbrowser-launcher
torbrowser-launcher

# macOS (Homebrew)
brew install tor-browser

# Manual download
# https://www.torproject.org/download/
```

### Chrome/Opera
- Use "SwitchyOmega" plugin
- Create profile: SOCKS5 @ 127.0.0.1:9050
- Switch profile when needed

**Full guide**: See `TOR_BROWSER_SETUP.md`

---

## 📋 API Documentation

### Endpoints

#### `/health` (GET)
Check backend status
```bash
curl http://127.0.0.1:8000/health
```

#### `/run` (POST)
Execute OSINT module
```bash
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "module": "files|mails|numbers|person",
    "target": "example.com",
    "mode": "simulate|live",
    "authorization_confirm": "I confirm I have authorization",
    "results_per_query": 10,
    "pause_seconds": 2.0
  }'
```

### Response Format
```json
[
  {
    "timestamp": "2025-11-26T22:04:06.761328",
    "type": "info|success|error|result",
    "message": "Log message",
    "link": "https://example.com/result"
  }
]
```

### Modes

**Simulate**
- Returns example dorks and Google search links
- No actual searches performed
- No blocking/rate-limiting
- Use for testing UI

**Live**
- Performs real Google searches
- Requires: `authorization_confirm: "I confirm I have authorization"`
- May hit rate limits (429 errors)
- Solution: Use SerpAPI (see below)

### Optional Fields

```json
{
  "extra": {
    "serpapi_key": "your-serpapi-api-key",  // Use SerpAPI for better results
    "target_override": "custom_target"      // Optional override
  }
}
```

---

## 📦 Modules Reference

### 1. **files** - Search for exposed files
Dorks: `site:TARGET filetype:pdf|txt|doc|xls|ppt|zip|tar|mp4|jpg|png`

Example:
```bash
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "module": "files",
    "target": "binapentakemnaker.bni.co.id",
    "mode": "simulate"
  }'
```

### 2. **mails** - Search for exposed email addresses
Dorks: `site:TARGET intext:@gmail|@hotmail|@yandex|etc`

### 3. **numbers** - Search for phone numbers / WhatsApp
Dorks: `site:TARGET intext:Whatsapp PHONECODE`

### 4. **person** - General person/org search
Dorks: `intext:TARGET` (flexible for names, orgs)

---

## 🛠️ Manual Commands

### Start Backend
```bash
cd ~/BL4CKOPS_REVEALED
source bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd ~/Downloads/bl4ckops-osint-gui-customization-main
npm run dev
# Frontend will open on http://localhost:3001
```

### Start Tor (if needed)
```bash
sudo tor &
# or
sudo systemctl start tor
```

### View Logs
```bash
# Backend logs
tail -f ~/BL4CKOPS_REVEALED/backend.log

# Frontend logs
tail -f ~/Downloads/bl4ckops-osint-gui-customization-main/frontend.log
```

---

## ⚠️ Known Limitations & Solutions

### Problem: Live searches return "429 Too Many Requests"

**Why**: Google blocks automated scripts

**Solutions** (in order of effectiveness):

1. **Use SerpAPI** (Best)
   - Get API key: https://serpapi.com
   - Pass: `"extra": {"serpapi_key": "your-key"}`
   - Reliable & no blocking

2. **Increase Pause Time**
   - Use: `"pause_seconds": 10.0`
   - Backend will wait 10s between queries
   - Slower but may work

3. **Use Residential Proxy Rotation**
   - Can implement free proxy list
   - Contact for integration

4. **Tor (Browser Only)**
   - Tor for browser privacy ✓
   - NOT for backend searches (would increase latency)

### Problem: Frontend won't load

**Solution**:
```bash
# Clear build cache
rm -rf ~/Downloads/bl4ckops-osint-gui-customization-main/.next

# Reinstall deps
cd ~/Downloads/bl4ckops-osint-gui-customization-main
npm install --legacy-peer-deps

# Restart
npm run dev
```

### Problem: "Address already in use" on port 8000

**Solution**:
```bash
# Kill old process
pkill -f "uvicorn.*8000"

# Wait 2s and restart
sleep 2
cd ~/BL4CKOPS_REVEALED && . bin/activate
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

---

## 🔐 Security Notes

1. **Backend runs NORMAL internet** (no Tor)
   - Faster for searches
   - Only use against authorized targets

2. **Browser can use Tor**
   - Setup independently
   - Doesn't affect backend speed
   - Use for viewing results anonymously

3. **Never mix Tor + VPN**
   - Can reduce privacy
   - Choose one or the other

4. **Authorization requirement**
   - Live mode requires explicit confirmation
   - Ensures user intent

---

## 📞 Architecture

```
┌─────────────────────────────────────────┐
│  Browser (Chrome/Firefox/Opera)         │
│  ├─ Can use Tor proxy (127.0.0.1:9050)  │
│  └─ Views UI at http://localhost:3001   │
└────────────┬────────────────────────────┘
             │ HTTP Requests
             ▼
┌─────────────────────────────────────────┐
│  Frontend (Next.js on 3001)              │
│  └─ React UI for OSINT modules          │
└────────────┬────────────────────────────┘
             │ JSON API Calls
             ▼
┌─────────────────────────────────────────┐
│  Backend (FastAPI on 8000)               │
│  ├─ googlesearch library (normal net)   │
│  ├─ SerpAPI optional (for reliability)  │
│  └─ Tor: NOT used here                  │
└────────────┬────────────────────────────┘
             │ Internet Searches
             ▼
     Google / SerpAPI
```

---

## ✨ Features

- ✓ 4 OSINT modules (files, mails, numbers, person)
- ✓ Simulate & Live modes
- ✓ Clean JSON API
- ✓ Beautiful React terminal UI
- ✓ LAN-accessible frontend
- ✓ Rate limiting controls
- ✓ Authorization checks
- ✓ Colored terminal logs
- ✓ Clickable result links
- ✓ Optional SerpAPI integration
- ✓ Optional Tor for browser

---

## 📅 Recent Changes

- ✓ Fixed favicon build error (was blocking startup)
- ✓ Removed Tor from backend (now browser-only)
- ✓ Backend runs on normal internet (faster searches)
- ✓ Added `TOR_BROWSER_SETUP.md` guide
- ✓ All 4 modules tested and working
- ✓ Frontend at http://localhost:3001 or http://192.168.1.9:3001

---

## 🎯 Next Steps

1. Open http://localhost:3001 in browser
2. Try simulate mode first (test UI)
3. For live searches: either increase pause_seconds or get SerpAPI key
4. Setup Tor in Firefox/Chrome if you want browser anonymity
5. Read `TOR_BROWSER_SETUP.md` for detailed Tor instructions

---

**Status**: ✅ READY TO USE
**Last Updated**: 2025-11-27
**Version**: 2.0 (Cleaned, Tor moved to browser layer)
