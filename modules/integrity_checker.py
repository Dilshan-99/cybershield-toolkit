"""
Module 4: File Integrity Checker
Generate, verify, and monitor file checksums to detect tampering.
"""

import os
import hashlib
import json
from datetime import datetime


HASH_ALGORITHMS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


class IntegrityChecker:

    def _hash_file(self, filepath: str, algorithm: str = "sha256") -> str | None:
        algo_func = HASH_ALGORITHMS.get(algorithm.lower())
        if not algo_func:
            print(f"\033[91m[-] Unknown algorithm: {algorithm}\033[0m")
            return None
        try:
            h = algo_func()
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            return h.hexdigest()
        except FileNotFoundError:
            print(f"\033[91m[-] File not found: {filepath}\033[0m")
            return None

    def generate(self, filepath: str, algorithm: str = "sha256"):
        checksum = self._hash_file(filepath, algorithm)
        if not checksum:
            return

        size = os.path.getsize(filepath)
        print(f"\n\033[92m[+] Checksum Generated\033[0m")
        print(f"    File      : {filepath}")
        print(f"    Size      : {size:,} bytes")
        print(f"    Algorithm : {algorithm.upper()}")
        print(f"    Checksum  : \033[96m{checksum}\033[0m")

        # Save to .checksum file
        record = {
            "file": os.path.abspath(filepath),
            "algorithm": algorithm,
            "checksum": checksum,
            "size": size,
            "generated_at": datetime.now().isoformat()
        }
        out_file = filepath + ".checksum"
        with open(out_file, "w") as f:
            json.dump(record, f, indent=2)
        print(f"\033[90m[*] Saved to: {out_file}\033[0m")

    def verify(self, filepath: str, known_checksum: str, algorithm: str = "sha256"):
        current = self._hash_file(filepath, algorithm)
        if not current:
            return

        print(f"\n\033[96m[+] Integrity Verification\033[0m")
        print(f"    File     : {filepath}")
        print(f"    Expected : {known_checksum}")
        print(f"    Computed : {current}")

        if current.lower() == known_checksum.lower():
            print(f"\n\033[92m[✓] MATCH — File is INTACT. No tampering detected.\033[0m")
        else:
            print(f"\n\033[91m[✗] MISMATCH — File may have been TAMPERED or CORRUPTED!\033[0m")

    def monitor_directory(self, dirpath: str):
        """Snapshot all files in a directory, then detect changes on re-run."""
        snapshot_file = os.path.join(dirpath, ".integrity_snapshot.json")

        if not os.path.isdir(dirpath):
            print(f"\033[91m[-] Directory not found: {dirpath}\033[0m")
            return

        print(f"\n\033[96m[+] Scanning directory: {dirpath}\033[0m")
        current_snapshot = {}

        for root, _, files in os.walk(dirpath):
            for fname in files:
                if fname.startswith(".integrity"):
                    continue
                full_path = os.path.join(root, fname)
                checksum = self._hash_file(full_path, "sha256")
                if checksum:
                    current_snapshot[full_path] = {
                        "checksum": checksum,
                        "size": os.path.getsize(full_path),
                        "modified": os.path.getmtime(full_path)
                    }

        if not os.path.exists(snapshot_file):
            # First run — save baseline
            with open(snapshot_file, "w") as f:
                json.dump(current_snapshot, f, indent=2)
            print(f"\033[92m[+] Baseline snapshot saved: {len(current_snapshot)} file(s) indexed.\033[0m")
            print(f"\033[90m[*] Run again to detect changes.\033[0m")
        else:
            # Compare with baseline
            with open(snapshot_file, "r") as f:
                baseline = json.load(f)

            added = [f for f in current_snapshot if f not in baseline]
            removed = [f for f in baseline if f not in current_snapshot]
            modified = [
                f for f in current_snapshot
                if f in baseline and current_snapshot[f]["checksum"] != baseline[f]["checksum"]
            ]

            print(f"\033[93m\n[+] Change Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\033[0m")
            print("-" * 50)

            if not added and not removed and not modified:
                print("\033[92m[✓] No changes detected. All files intact.\033[0m")
            else:
                for f in added:
                    print(f"\033[92m  [ADDED]    {f}\033[0m")
                for f in removed:
                    print(f"\033[91m  [REMOVED]  {f}\033[0m")
                for f in modified:
                    print(f"\033[93m  [MODIFIED] {f}\033[0m")

            # Update snapshot
            with open(snapshot_file, "w") as f:
                json.dump(current_snapshot, f, indent=2)
            print(f"\n\033[90m[*] Snapshot updated.\033[0m")


if __name__ == "__main__":
    checker = IntegrityChecker()
    checker.generate("test.txt", "sha256")
