# Hacker Tool - Fake Web Exploit with Reverse Shell

A social engineering tool that hosts a fake web page (e.g. CAPTCHA or update prompt) to trick victims into executing a reverse shell payload. The page uses clipboard hijacking to preload the reverse shell command, which the victim unknowingly pastes and runs.

**Author:** xaiqttt  
**Year:** 2025

---

## Features

- Fake web exploit page (e.g. fake CAPTCHA)
- Clipboard hijacking to preload reverse shell payload
- Auto-updates `config.js` with listener IP and port
- HTTP server with visit logging (IP + User-Agent)
- Netcat reverse shell listener

---

## Requirements

- **Python 3.x** (built-in libraries only)
- **Netcat (`nc`)** installed on your system

---

## Usage

```bash
python3 run.py
