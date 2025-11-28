# pw_auditor/patterns.py
"""Pattern detection utilities.

Detects common weak patterns:
  - years (e.g., 1999, 2024)
  - repeated characters (e.g., 'aaaa')
  - repeated sequences (e.g., 'abcabc', '123123')
  - simple keyboard walks (qwerty, asdf, etc.)
  - dictionary substrings (from bundled common_words.txt)
  - exact common password matches (from bundled common_passwords.txt)

Returns a list of compact flags that the auditor uses to generate suggestions.
"""

from __future__ import annotations
import re
from typing import List
import importlib.resources as pkg_resources

# Small curated list of obvious keyboard patterns
_KEYBOARD_PATTERNS = [
    "qwerty", "asdf", "zxcv", "1qaz", "qaz", "wasd", "12345", "54321"
]


def detect_patterns(password: str) -> List[str]:
    """
    Detect known weak patterns and return a list of string flags.

    Flags examples:
        - "contains_year"
        - "repeated_chars"
        - "repeated_sequence"
        - "keyboard_pattern:qwerty"
        - "dictionary_word:password"
        - "common_password_list"
    """
    pwd = password or ""
    flags: List[str] = []
    lower = pwd.lower()

    # Year detection (1900-2099)
    if re.search(r"(19|20)\d{2}", pwd):
        flags.append("contains_year")

    # Repeated characters, e.g., 'aaa' or '111'
    if re.search(r"(.)\1{2,}", pwd):
        flags.append("repeated_chars")

    # Repeated sequence, e.g., 'abcabc', '123123'
    if re.search(r"(.{2,})\1{1,}", pwd):
        flags.append("repeated_sequence")

    # Keyboard patterns (simple substring match)
    for seq in _KEYBOARD_PATTERNS:
        if seq in lower:
            flags.append(f"keyboard_pattern:{seq}")

    # Dictionary words (substring match) — load bundled list if available
    try:
        wordlist_resource = pkg_resources.files("pw_auditor").joinpath("data").joinpath("common_words.txt")
        wordlist = set()
        with wordlist_resource.open("r", encoding="utf-8") as wf:
            for line in wf:
                token = line.strip().lower()
                if token:
                    wordlist.add(token)
    except Exception:
        wordlist = set()

    # Prefer longer words first to avoid short false positives
    for w in sorted(wordlist, key=len, reverse=True):
        if len(w) < 3:
            continue
        if w in lower:
            flags.append(f"dictionary_word:{w}")
            break  # stop after first significant dictionary hit

    # Common password list (exact match)
    try:
        common_pw_resource = pkg_resources.files("pw_auditor").joinpath("data").joinpath("common_passwords.txt")
        common_passwords = set()
        with common_pw_resource.open("r", encoding="utf-8") as cf:
            for line in cf:
                token = line.strip()
                if token:
                    common_passwords.add(token)
    except Exception:
        common_passwords = set()

    if password in common_passwords:
        flags.append("common_password_list")

    return flags
