"""
Module 1: Port Scanner
Scans open ports on a target host with service detection.
"""

import socket
import threading
from datetime import datetime


# Common port-to-service mapping
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}


class PortScanner:
    def __init__(self, target: str, start_port: int = 1, end_port: int = 1024):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.lock = threading.Lock()

    def resolve_host(self) -> str | None:
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror:
            return None

    def scan_port(self, ip: str, port: int):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")
                with self.lock:
                    self.open_ports.append((port, service))
            sock.close()
        except Exception:
            pass

    def scan(self):
        print(f"\n\033[92m[+] Resolving target: {self.target}\033[0m")
        ip = self.resolve_host()
        if not ip:
            print(f"\033[91m[-] Could not resolve host: {self.target}\033[0m")
            return

        print(f"\033[92m[+] Target IP     : {ip}\033[0m")
        print(f"\033[92m[+] Port Range    : {self.start_port} - {self.end_port}\033[0m")
        print(f"\033[92m[+] Scan Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        print("-" * 50)

        threads = []
        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(ip, port))
            threads.append(t)
            t.start()
            # Limit concurrent threads
            if len(threads) >= 100:
                for thread in threads:
                    thread.join()
                threads = []

        for thread in threads:
            thread.join()

        print(f"\n\033[93m{'PORT':<10}{'STATE':<12}{'SERVICE'}\033[0m")
        print("-" * 35)

        if self.open_ports:
            for port, service in sorted(self.open_ports):
                print(f"\033[92m{port:<10}{'OPEN':<12}{service}\033[0m")
        else:
            print("\033[91m[-] No open ports found in range.\033[0m")

        print(f"\n\033[96m[+] Scan complete. {len(self.open_ports)} open port(s) found.\033[0m")
        print(f"\033[90m[*] Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")


if __name__ == "__main__":
    target = input("Target: ")
    scanner = PortScanner(target, 1, 1024)
    scanner.scan()
