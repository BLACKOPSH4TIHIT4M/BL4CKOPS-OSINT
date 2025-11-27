# BL4CKOPS_REVEALED - OSINT Framework 🕵️
## Advanced Open Source Intelligence Gathering Tool
**BL4CKOPS_REVEALED is a comprehensive OSINT framework designed for tactical reconnaissance and intelligence gathering. It provides extensive search capabilities across websites using specialized techniques to discover sensitive files, credentials, API keys, and other valuable information. Powered by Google dork operators and advanced web scraping.**
## Exploited vulnerabilities 🏴‍☠️
**Sensitive Information Exposure CWE-200**
## OSINT Modules (14 Advanced Reconnaissance Tools) ☠️
### Data Dumps 📊
**Indexed files & directories** - Discover exposed files on web servers <br/>
**Database exposures** - Find publicly indexed database files <br/>
**Backup files** - Locate backup archives and recovery files <br/>
**Configuration files** - Uncover exposed config and settings <br/>
**Git repositories** - Find exposed version control data <br/>

### Scrappers 🔍
**Email harvesting** - Extract email addresses from indexed sources <br/>
**Phone number extraction** - Collect phone contacts from web data <br/>
**Person intelligence** - Gather biographical and background data <br/>
**API keys & credentials** - Discover exposed authentication tokens <br/>
**Social media enumeration** - Identify social accounts and profiles <br/>
**Malware signatures** - Track malicious file indicators <br/>

### Advanced Recon 🎯
**Sensitive data detection** - CWE-200 exposure identification <br/>
**Web scraping engine** - Custom HTML parsing and data extraction <br/>
**Dork generator** - Automated Google search operator construction <br/>
## Installation & Deployment 💡

**1. Clone & Setup:**
```bash
git clone https://github.com/BLACKOPSH4TIHIT4M/BL4CKOPS_REVEALED.git
cd BL4CKOPS_REVEALED
source bin/activate
pip install -r requirements.txt
```

**2. Run Backend (FastAPI):**
```bash
python backend/api.py
# Runs on 0.0.0.0:8000
```

**3. Run Frontend (Next.js GUI):**
```bash
cd bl4ckops-osint-gui-customization-main
npm install
npm run dev
# Runs on http://localhost:3004
```

**4. Access GUI:**
Open browser to `http://localhost:3004` (local) or `http://192.168.1.9:3004` (network)

## Required Python Version 📌
` Python 3.8+ ` (tested with 3.13)

## Security & Encryption 🔐
**This repository is encrypted with GPG AES-256 encryption.** Sensitive operational files are protected with a custom password. Access requires decryption before operational deployment.
## Project Information 🚀
**Creator:** BLACKOPSH4TIHIT4M
**Repository:** https://github.com/BLACKOPSH4TIHIT4M/BL4CKOPS_REVEALED
**Framework Version:** 2.0
**Architecture:** 
- Frontend: Next.js 15.3.5 (React + Tailwind CSS)
- Backend: FastAPI + Uvicorn
- Execution: Real-time terminal with color-coded output
- Encryption: GPG AES-256 symmetric encryption

## Deployment Status ✅
- Web GUI: Available on localhost:3004 and LAN (192.168.1.9:3004)
- Backend API: Running on 0.0.0.0:8000
- Repository: Encrypted archive on GitHub
- Status: Production-ready OSINT reconnaissance platform

## ⚠️ Legal & Ethical Notice
**IMPORTANT:** This tool should only be used for:
- Authorized security assessments and penetration testing
- Vulnerability scanning of systems you own or have explicit permission to test
- Educational and training purposes in controlled environments
- Authorized OSINT intelligence gathering

Unauthorized access to computer systems is illegal. Always obtain proper authorization before conducting reconnaissance activities.
