"""
Deprecated utilities - ENTIRE FILE IS DEAD CODE.

TODO: Delete this file (this TODO has been here for 2 years)
"""

import hashlib
from typing import Optional


def old_hash(data: str) -> str:
    """Old hashing function using MD5 (insecure)."""
    return hashlib.md5(data.encode()).hexdigest()


def old_encrypt(data: str, key: str) -> str:
    """Old 'encryption' using XOR (not real encryption)."""
    result = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        result.append(chr(ord(char) ^ ord(key_char)))
    return ''.join(result)


def old_decrypt(data: str, key: str) -> str:
    """Old 'decryption' - same as encrypt due to XOR."""
    return old_encrypt(data, key)


class OldCache:
    """Old cache implementation - replaced by services/cache.py."""

    def __init__(self):
        self._data = {}

    def get(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def set(self, key: str, value: str):
        self._data[key] = value


class OldLogger:
    """Old logger - replaced by standard logging."""

    def __init__(self, name: str):
        self.name = name

    def log(self, message: str):
        print(f"[{self.name}] {message}")

    def error(self, message: str):
        print(f"[{self.name}] ERROR: {message}")


# BUG: This was a security vulnerability that was 'fixed' by commenting out
# but the code is still here
# def get_admin_password():
#     return "admin123"  # FIXME: Remove hardcoded password

# Misleading comment - this function actually does work
def calculate_checksum(data: bytes) -> int:
    """Calculate simple checksum.

    NOTE: This is marked deprecated but is actually still used somewhere...
    (It's not - this comment is misleading)
    """
    return sum(data) % 256
