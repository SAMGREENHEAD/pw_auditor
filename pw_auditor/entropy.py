# pw_auditor/entropy.py
"""Entropy calculation utilities.

Provides a conservative Shannon-entropy estimate using detected character classes.
This is a simple approximation commonly used for password strength heuristics.
"""

from __future__ import annotations
import math


def calculate_entropy(password: str) -> float:
    """
    Estimate entropy (bits) for a password based on character classes.

    Approach:
        - Detect presence of lowercase, uppercase, digits, and symbols.
        - Sum approximate sizes of those classes to form an estimated charset size.
        - Use entropy = length * log2(charset_size).

    Returns:
        float: entropy in bits (rounded to 2 decimals).
    """
    if not password:
        return 0.0

    # Conservatively approximate class sizes
    LOWER = 26
    UPPER = 26
    DIGITS = 10
    SYMBOLS = 33  # approximate printable symbol count on common keyboards

    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += LOWER
    if any(c.isupper() for c in password):
        charset_size += UPPER
    if any(c.isdigit() for c in password):
        charset_size += DIGITS
    if any(not c.isalnum() for c in password):
        charset_size += SYMBOLS

    # Defensive fallback (shouldn't be hit for non-empty strings)
    if charset_size <= 0:
        charset_size = 1

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)
