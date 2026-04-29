#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════╗
║      CyberShield Toolkit v1.0             ║
║      Python Cyber Security Toolkit        ║
╚═══════════════════════════════════════════╝
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.port_scanner import PortScanner
from modules.password_generator import PasswordGenerator
from modules.file_encryptor import FileEncryptor
from modules.integrity_checker import IntegrityChecker
from modules.web_recon import WebRecon
from modules.network_info import NetworkInfo


def banner():
    print("""
\033[92m
 ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██╗  ██╗██╗███████╗██╗     ██████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗███████║██║█████╗  ██║     ██║  ██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║  ██║██║███████╗███████╗██████╔╝
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝
\033[0m
\033[96m                    Python Cyber Security Toolkit v1.0
                    github.com/Dilshan-99/cybershield-toolkit\033[0m
    """)


def menu():
    print("""
\033[93m╔══════════════════════════════════════╗
║           MAIN MENU                  ║
╠══════════════════════════════════════╣
║  [1] 🔍 Port Scanner                 ║
║  [2] 🔑 Password Generator           ║
║  [3] 🔐 File Encryptor/Decryptor     ║
║  [4] ✅ File Integrity Checker       ║
║  [5] 🌐 Web Reconnaissance           ║
║  [6] 📡 Network Info Lookup          ║
║  [0] ❌ Exit                         ║
╚══════════════════════════════════════╝\033[0m
""")


def main():
    banner()

    while True:
        menu()
        choice = input("\033[96m[CyberShield]> \033[0m").strip()

        if choice == "1":
            target = input("  Target host/IP: ").strip()
            port_range = input("  Port range (e.g. 1-1000) [default: 1-1024]: ").strip() or "1-1024"
            start, end = map(int, port_range.split("-"))
            scanner = PortScanner(target, start, end)
            scanner.scan()

        elif choice == "2":
            length = input("  Password length [default: 16]: ").strip() or "16"
            count = input("  How many passwords? [default: 5]: ").strip() or "5"
            gen = PasswordGenerator(int(length), int(count))
            gen.generate()

        elif choice == "3":
            print("  [1] Encrypt file   [2] Decrypt file")
            sub = input("  Choice: ").strip()
            filepath = input("  File path: ").strip()
            enc = FileEncryptor()
            if sub == "1":
                enc.encrypt_file(filepath)
            elif sub == "2":
                enc.decrypt_file(filepath)

        elif choice == "4":
            print("  [1] Generate checksum   [2] Verify checksum   [3] Monitor directory")
            sub = input("  Choice: ").strip()
            checker = IntegrityChecker()
            if sub == "1":
                path = input("  File path: ").strip()
                algo = input("  Algorithm (md5/sha1/sha256) [default: sha256]: ").strip() or "sha256"
                checker.generate(path, algo)
            elif sub == "2":
                path = input("  File path: ").strip()
                known = input("  Known checksum: ").strip()
                algo = input("  Algorithm [default: sha256]: ").strip() or "sha256"
                checker.verify(path, known, algo)
            elif sub == "3":
                path = input("  Directory path: ").strip()
                checker.monitor_directory(path)

        elif choice == "5":
            url = input("  Target URL (e.g. https://example.com): ").strip()
            recon = WebRecon(url)
            recon.run_all()

        elif choice == "6":
            target = input("  Website or IP address: ").strip()
            net = NetworkInfo(target)
            net.lookup()

        elif choice == "0":
            print("\n\033[92m[+] Stay safe. Stay ethical. Goodbye!\033[0m\n")
            sys.exit(0)

        else:
            print("\033[91m[-] Invalid option. Try again.\033[0m")

        input("\n\033[90mPress Enter to continue...\033[0m")


if __name__ == "__main__":
    main()
