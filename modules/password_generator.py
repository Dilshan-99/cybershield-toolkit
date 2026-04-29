"""
Module 2: Password Generator
Generates strong passwords with strength analysis and entropy calculation.
"""

import random
import string
import math


class PasswordGenerator:
    def __init__(self, length: int = 16, count: int = 5):
        self.length = length
        self.count = count

    def calculate_entropy(self, password: str) -> float:
        charset = 0
        if any(c.islower() for c in password):
            charset += 26
        if any(c.isupper() for c in password):
            charset += 26
        if any(c.isdigit() for c in password):
            charset += 10
        if any(c in string.punctuation for c in password):
            charset += 32
        if charset == 0:
            return 0.0
        return round(len(password) * math.log2(charset), 2)

    def strength_label(self, entropy: float) -> str:
        if entropy < 28:
            return "\033[91mVERY WEAK\033[0m"
        elif entropy < 36:
            return "\033[91mWEAK\033[0m"
        elif entropy < 60:
            return "\033[93mFAIR\033[0m"
        elif entropy < 128:
            return "\033[92mSTRONG\033[0m"
        else:
            return "\033[96mVERY STRONG\033[0m"

    def generate_password(self, use_upper=True, use_digits=True, use_symbols=True) -> str:
        charset = string.ascii_lowercase
        if use_upper:
            charset += string.ascii_uppercase
        if use_digits:
            charset += string.digits
        if use_symbols:
            charset += string.punctuation

        while True:
            pwd = "".join(random.choices(charset, k=self.length))
            # Ensure at least one of each required type
            has_lower = any(c.islower() for c in pwd)
            has_upper = any(c.isupper() for c in pwd) if use_upper else True
            has_digit = any(c.isdigit() for c in pwd) if use_digits else True
            has_sym = any(c in string.punctuation for c in pwd) if use_symbols else True
            if has_lower and has_upper and has_digit and has_sym:
                return pwd

    def generate(self):
        print(f"\n\033[92m[+] Generating {self.count} password(s) of length {self.length}\033[0m")
        print("-" * 65)
        print(f"\033[93m{'#':<4}{'PASSWORD':<35}{'ENTROPY':<12}STRENGTH\033[0m")
        print("-" * 65)

        for i in range(1, self.count + 1):
            pwd = self.generate_password()
            entropy = self.calculate_entropy(pwd)
            strength = self.strength_label(entropy)
            print(f"{i:<4}\033[96m{pwd:<35}\033[0m{entropy:<12}{strength}")

        print("-" * 65)
        print("\033[90m[*] Tip: Use a password manager to store these securely.\033[0m")


if __name__ == "__main__":
    gen = PasswordGenerator(20, 5)
    gen.generate()
