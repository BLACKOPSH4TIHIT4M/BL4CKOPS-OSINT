# Setup Tor untuk Browser (Chrome/Firefox/Opera)

## Overview
Backend OSINT berjalan dengan internet normal (tanpa proxy).
Browser Anda dapat dikonfigurasi dengan Tor untuk anonimitas saat browsing.

---

## Option 1: Tor Browser (Rekomendasi)

### Install Tor Browser
```bash
# Download dari https://www.torproject.org/download/
# atau via apt (Kali Linux):
sudo apt install torbrowser-launcher

# Jalankan
torbrowser-launcher
```

### Hasil
- Automatic Tor routing untuk semua traffic
- Tidak perlu konfigurasi manual
- IP anonim otomatis

---

## Option 2: Firefox + Tor Proxy (Manual)

### Prerequisites
Pastikan Tor daemon sudah berjalan:
```bash
sudo systemctl start tor
# atau
sudo tor &
```

Verifikasi Tor listening pada port 9050:
```bash
netstat -ln | grep 9050
# Output: tcp 0 0 127.0.0.1:9050 0.0.0.0:* LISTEN
```

### Konfigurasi Firefox

1. **Buka Firefox Settings**
   - Menu (≡) → Settings → Network Settings

2. **Configure Proxy**
   - Scroll ke bawah ke "Network Settings"
   - Klik "Settings..."
   - Pilih: **Manual proxy configuration**

3. **Masukkan Tor Proxy**
   - **SOCKS Host**: `127.0.0.1`
   - **Port**: `9050`
   - **SOCKS v5**: ✓ (checked)
   - **Proxy DNS when using SOCKS v5**: ✓ (checked)

4. **Verifikasi**
   - Buka https://check.torproject.org
   - Jika berhasil: "Congratulations! Your browser is configured to use Tor."

### Test Backend (Dari Browser)
```
http://localhost:3001  (localhost)
atau
http://192.168.1.9:3001  (LAN IP)
```

---

## Option 3: Chrome/Chromium + SwitchyOmega Plugin

### Install Plugin
1. Chrome Web Store: search "SwitchyOmega" atau "Proxy SwitchyOmega"
2. Add to Chrome

### Setup Proxy Profile
1. Click plugin icon → Options
2. Create "Tor Proxy" profile:
   - Protocol: SOCKS5
   - Server: 127.0.0.1
   - Port: 9050
3. Save & Apply

### Test
- Plugin icon → Switch to "Tor Proxy" profile
- Visit https://check.torproject.org

---

## Option 4: Opera + Built-in VPN (Alternative)

Opera memiliki built-in VPN gratis (bukan Tor, tapi anonim):

1. Menu → Settings → Privacy & security
2. Enable "VPN"
3. Pilih region

**Note**: VPN Opera lebih cepat tapi kurang privat dari Tor.

---

## Verify Tor Connection

### Dari Terminal
```bash
# Check Tor is running
ps aux | grep tor | grep -v grep

# Check Tor port open
netstat -ln | grep 9050

# Test via curl with Tor
curl --socks5 127.0.0.1:9050 https://check.torproject.org/api/ip
```

### Expected Output
```json
{
  "IsTor": true,
  "IP": "x.x.x.x"  (NOT your real IP)
}
```

---

## Backend Status

✓ Backend tetap menggunakan internet NORMAL (tidak via Tor)
✓ Browser dapat dikonfigurasi untuk Tor secara independen
✓ Frontend UI berjalan di: http://localhost:3001

## Commands Reference

```bash
# Start Tor daemon (if not running)
sudo tor &

# Start Backend
cd ~/BL4CKOPS_REVEALED && . bin/activate && \
  uvicorn backend.api:app --host 0.0.0.0 --port 8000

# Start Frontend
cd ~/Downloads/bl4ckops-osint-gui-customization-main && \
  npm run dev

# Check Backend
curl http://127.0.0.1:8000/health

# Check Frontend
open http://localhost:3001
```

---

## Troubleshooting

**Q: Tor tidak connect di Firefox?**
- Pastikan `sudo tor` sedang berjalan di terminal lain
- Restart Firefox
- Check: `netstat -ln | grep 9050`

**Q: Backend lambat dengan Tor?**
- Backend TIDAK menggunakan Tor (jalankan normal)
- Tor hanya untuk browser Anda

**Q: SOCKS proxy 127.0.0.1:9050 "connection refused"?**
- Start Tor: `sudo tor`
- Tunggu sampai "Bootstrapped 100%"

**Q: IP di check.torproject.org masih sama?**
- Clear browser cache
- Disconnect/reconnect Tor
- Restart browser

---

## Security Notes

1. **Tor Browser** adalah cara paling aman
2. Jangan mix Tor + VPN (bisa malah reduce privacy)
3. Disable JavaScript di Tor untuk extra protection
4. Use separate browser profile/container untuk sensitive work
5. Backend OSINT berjalan normal (tidak private) - gunakan untuk authorized targets saja

---

Generated: 2025-11-27
Status: ✓ Tor proxy ready for browser routing
