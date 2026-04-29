"""
Module 5: Web Reconnaissance
Gather security-relevant information about a target website.
"""

import urllib.request
import urllib.parse
import urllib.error
import ssl
import socket
from datetime import datetime


class WebRecon:
    def __init__(self, url: str):
        if not url.startswith("http"):
            url = "https://" + url
        self.url = url
        self.parsed = urllib.parse.urlparse(url)
        self.hostname = self.parsed.netloc or self.parsed.path

    def check_http_headers(self):
        """Check security-related HTTP response headers."""
        SECURITY_HEADERS = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy",
            "X-XSS-Protection",
        ]
        print(f"\n\033[96m[+] HTTP Security Headers\033[0m")
        print("-" * 50)
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, context=ctx, timeout=10)
            headers = dict(response.headers)
            status = response.status
            print(f"    Status Code : \033[92m{status}\033[0m")
            print(f"    Server      : {headers.get('Server', 'Not disclosed')}")
            print(f"    X-Powered-By: {headers.get('X-Powered-By', 'Not disclosed')}")
            print()
            for h in SECURITY_HEADERS:
                val = headers.get(h)
                if val:
                    print(f"    \033[92m[✓] {h:<35}\033[0m {val[:60]}")
                else:
                    print(f"    \033[91m[✗] {h:<35}\033[0m MISSING")
        except Exception as e:
            print(f"    \033[91m[-] Error: {e}\033[0m")

    def check_ssl_info(self):
        """Retrieve SSL/TLS certificate information."""
        print(f"\n\033[96m[+] SSL/TLS Certificate Info\033[0m")
        print("-" * 50)
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(
                socket.create_connection((self.hostname, 443), timeout=10),
                server_hostname=self.hostname
            ) as s:
                cert = s.getpeercert()
                subject = dict(x[0] for x in cert.get("subject", []))
                issuer = dict(x[0] for x in cert.get("issuer", []))
                not_after = cert.get("notAfter", "Unknown")
                not_before = cert.get("notBefore", "Unknown")
                san = cert.get("subjectAltName", [])

                print(f"    Common Name : {subject.get('commonName', 'N/A')}")
                print(f"    Issued By   : {issuer.get('organizationName', 'N/A')}")
                print(f"    Valid From  : {not_before}")
                print(f"    Valid Until : \033[93m{not_after}\033[0m")

                domains = [v for k, v in san if k == "DNS"]
                if domains:
                    print(f"    SANs ({len(domains)})  : {', '.join(domains[:5])}")
                    if len(domains) > 5:
                        print(f"               ... and {len(domains)-5} more")
        except ssl.SSLCertVerificationError:
            print("    \033[91m[!] SSL Certificate verification FAILED (possibly self-signed)\033[0m")
        except Exception as e:
            print(f"    \033[91m[-] Could not retrieve SSL info: {e}\033[0m")

    def check_robots_txt(self):
        """Fetch robots.txt to discover hidden paths."""
        print(f"\n\033[96m[+] robots.txt\033[0m")
        print("-" * 50)
        robots_url = f"{self.parsed.scheme}://{self.hostname}/robots.txt"
        try:
            ctx = ssl.create_default_context()
            req = urllib.request.Request(robots_url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, context=ctx, timeout=8)
            content = response.read().decode("utf-8", errors="ignore")
            lines = content.strip().splitlines()
            disallowed = [l for l in lines if l.lower().startswith("disallow")]
            print(f"    \033[92m[✓] Found robots.txt — {len(disallowed)} Disallow rule(s)\033[0m")
            for line in disallowed[:10]:
                print(f"    \033[93m{line}\033[0m")
            if len(disallowed) > 10:
                print(f"    ... and {len(disallowed)-10} more")
        except urllib.error.HTTPError as e:
            print(f"    \033[91m[-] HTTP {e.code} — robots.txt not found\033[0m")
        except Exception as e:
            print(f"    \033[91m[-] {e}\033[0m")

    def dns_lookup(self):
        """Perform DNS resolution and get IP info."""
        print(f"\n\033[96m[+] DNS / IP Lookup\033[0m")
        print("-" * 50)
        try:
            ip = socket.gethostbyname(self.hostname)
            print(f"    Hostname : {self.hostname}")
            print(f"    IP       : \033[92m{ip}\033[0m")
            # Reverse DNS
            try:
                reverse = socket.gethostbyaddr(ip)[0]
                print(f"    Reverse  : {reverse}")
            except Exception:
                print(f"    Reverse  : Not available")
        except socket.gaierror as e:
            print(f"    \033[91m[-] DNS lookup failed: {e}\033[0m")

    def run_all(self):
        print(f"\n\033[92m[+] Web Recon Target: {self.url}")
        print(f"[+] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
        self.dns_lookup()
        self.check_ssl_info()
        self.check_http_headers()
        self.check_robots_txt()
        print(f"\n\033[90m[*] Recon complete.\033[0m")


if __name__ == "__main__":
    recon = WebRecon("https://example.com")
    recon.run_all()
