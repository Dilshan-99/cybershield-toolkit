"""
Module 6: Network Info Lookup
Get IP address, hostname, and basic network information.
"""

import socket
import urllib.request
import json


class NetworkInfo:
    def __init__(self, target: str):
        self.target = target.strip()

    def lookup(self):
        print(f"\n\033[96m[+] Network Info: {self.target}\033[0m")
        print("-" * 50)

        # Resolve to IP
        try:
            ip = socket.gethostbyname(self.target)
            print(f"    IP Address : \033[92m{ip}\033[0m")
        except socket.gaierror:
            ip = self.target  # might already be an IP
            print(f"    Target     : {self.target}")

        # Reverse DNS
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            print(f"    Hostname   : {hostname}")
        except Exception:
            print(f"    Hostname   : Not available")

        # GeoIP via ipinfo.io (free, no key needed)
        try:
            url = f"https://ipinfo.io/{ip}/json"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            response = urllib.request.urlopen(req, timeout=8)
            data = json.loads(response.read().decode())

            print(f"    City       : {data.get('city', 'N/A')}")
            print(f"    Region     : {data.get('region', 'N/A')}")
            print(f"    Country    : {data.get('country', 'N/A')}")
            print(f"    Org/ISP    : {data.get('org', 'N/A')}")
            print(f"    Timezone   : {data.get('timezone', 'N/A')}")

            loc = data.get("loc", "")
            if loc:
                lat, lon = loc.split(",")
                print(f"    Location   : {lat}°N, {lon}°E")
                print(f"    Maps       : https://maps.google.com/?q={loc}")

        except Exception as e:
            print(f"    \033[91m[-] GeoIP lookup failed: {e}\033[0m")


if __name__ == "__main__":
    net = NetworkInfo("google.com")
    net.lookup()
