"""
Module 3: File Encryptor / Decryptor
AES-based symmetric file encryption using the cryptography library (Fernet).
"""

import os
import base64
import hashlib
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class FileEncryptor:
    KEY_FILE = ".cybershield.key"

    def __init__(self):
        if not CRYPTO_AVAILABLE:
            print("\033[91m[-] 'cryptography' library not found.")
            print("    Install with: pip install cryptography\033[0m")

    def _load_or_create_key(self) -> bytes:
        if os.path.exists(self.KEY_FILE):
            with open(self.KEY_FILE, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.KEY_FILE, "wb") as f:
                f.write(key)
            print(f"\033[93m[!] New encryption key generated: {self.KEY_FILE}")
            print("    KEEP THIS FILE SAFE. Without it, you cannot decrypt!\033[0m")
            return key

    def _derive_key_from_password(self, password: str) -> bytes:
        """Derive a Fernet-compatible key from a user password."""
        digest = hashlib.sha256(password.encode()).digest()
        return base64.urlsafe_b64encode(digest)

    def encrypt_file(self, filepath: str):
        if not CRYPTO_AVAILABLE:
            return
        if not os.path.isfile(filepath):
            print(f"\033[91m[-] File not found: {filepath}\033[0m")
            return

        use_password = input("  Use password instead of key file? (y/n): ").strip().lower()
        if use_password == "y":
            pwd = input("  Enter password: ").strip()
            key = self._derive_key_from_password(pwd)
        else:
            key = self._load_or_create_key()

        fernet = Fernet(key)

        with open(filepath, "rb") as f:
            original = f.read()

        encrypted = fernet.encrypt(original)
        out_path = filepath + ".enc"

        with open(out_path, "wb") as f:
            f.write(encrypted)

        # Show file size comparison
        original_size = len(original)
        encrypted_size = len(encrypted)

        print(f"\n\033[92m[+] Encryption successful!\033[0m")
        print(f"    Input  : {filepath} ({original_size:,} bytes)")
        print(f"    Output : {out_path} ({encrypted_size:,} bytes)")
        print(f"\033[90m[*] Algorithm: AES-128-CBC via Fernet (PKCS7 padding + HMAC-SHA256)\033[0m")

    def decrypt_file(self, filepath: str):
        if not CRYPTO_AVAILABLE:
            return
        if not os.path.isfile(filepath):
            print(f"\033[91m[-] File not found: {filepath}\033[0m")
            return

        use_password = input("  Was this encrypted with a password? (y/n): ").strip().lower()
        if use_password == "y":
            pwd = input("  Enter password: ").strip()
            key = self._derive_key_from_password(pwd)
        else:
            key = self._load_or_create_key()

        fernet = Fernet(key)

        with open(filepath, "rb") as f:
            encrypted = f.read()

        try:
            decrypted = fernet.decrypt(encrypted)
        except Exception:
            print("\033[91m[-] Decryption failed. Wrong key or corrupted file.\033[0m")
            return

        # Remove .enc extension
        out_path = filepath.replace(".enc", "") if filepath.endswith(".enc") else filepath + ".dec"

        with open(out_path, "wb") as f:
            f.write(decrypted)

        print(f"\n\033[92m[+] Decryption successful!\033[0m")
        print(f"    Input  : {filepath}")
        print(f"    Output : {out_path} ({len(decrypted):,} bytes)")


if __name__ == "__main__":
    enc = FileEncryptor()
    enc.encrypt_file("test.txt")
