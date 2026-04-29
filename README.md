# 🛡️ CyberShield Toolkit

> A modular Python-based Cyber Security Toolkit for learning, practice, and ethical security research.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 Features

| # | Module | Description |
|---|--------|-------------|
| 1 | 🔍 **Port Scanner** | Multi-threaded TCP port scanner with service detection |
| 2 | 🔑 **Password Generator** | Cryptographically strong passwords with entropy analysis |
| 3 | 🔐 **File Encryptor** | AES-based file encryption/decryption (password or key file) |
| 4 | ✅ **Integrity Checker** | SHA-256 checksum generation, verification & directory monitoring |
| 5 | 🌐 **Web Recon** | HTTP headers, SSL cert info, DNS lookup, robots.txt analysis |
| 6 | 📡 **Network Info** | IP geolocation, reverse DNS, ISP/org lookup |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/cybershield-toolkit.git
cd cybershield-toolkit
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the toolkit
```bash
python toolkit.py
```

---

## 🔧 Usage Examples

### Port Scanner
```
Target host/IP: scanme.nmap.org
Port range: 1-1000

PORT      STATE       SERVICE
22        OPEN        SSH
80        OPEN        HTTP
443       OPEN        HTTPS
```

### Password Generator
```
Length: 20   Count: 3

#   PASSWORD                            ENTROPY    STRENGTH
1   X9!kLm@2#pQr$5&nWvYz                131.1      VERY STRONG
2   aB3%uT8*eR1^iO6(sN4)                131.1      VERY STRONG
```

### Web Recon
```
Target: https://example.com

[✓] Strict-Transport-Security     max-age=31536000
[✗] Content-Security-Policy       MISSING
[✓] X-Frame-Options               DENY
```

### File Integrity Monitor
```
[ADDED]    /docs/new_report.pdf
[MODIFIED] /config/settings.json
[REMOVED]  /temp/cache.tmp
```

---

## 📁 Project Structure

```
cybershield-toolkit/
│
├── toolkit.py                  # Main entry point
├── requirements.txt
├── README.md
│
└── modules/
    ├── port_scanner.py         # Module 1
    ├── password_generator.py   # Module 2
    ├── file_encryptor.py       # Module 3
    ├── integrity_checker.py    # Module 4
    ├── web_recon.py            # Module 5
    └── network_info.py         # Module 6
```

---

## ⚙️ Requirements

- Python 3.10+
- `cryptography` library (for file encryption)
- All other modules use Python standard library only

---

## ⚠️ Disclaimer

> This toolkit is intended for **educational purposes** and **authorized security testing only**.
> Always get **written permission** before scanning or testing systems you do not own.
> The author is not responsible for any misuse of this tool.

---

## 📚 Concepts Demonstrated

- TCP socket programming & threading
- Symmetric encryption (AES via Fernet)
- Cryptographic hashing (MD5, SHA-1, SHA-256, SHA-512)
- HMAC & password-derived keys (PBKDF)
- HTTP header security analysis
- SSL/TLS certificate inspection
- DNS resolution & reverse lookups
- REST API consumption (GeoIP)
- CLI design with ANSI color codes

---

## 🤝 Contributing

Pull requests welcome! Please open an issue first to discuss changes.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with 🐍 Python | Designed for learning Cyber Security*
