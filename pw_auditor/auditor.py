# pw_auditor/auditor.py
"""High-level password auditor.

Orchestrates entropy calculation and pattern detection, produces a score and
actionable suggestions. Returns a JSON-friendly dict for easy consumption.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
from .entropy import calculate_entropy
from .patterns import detect_patterns


@dataclass
class AuditResult:
    password: str
    entropy_bits: float
    patterns: List[str]
    score: str
    suggestions: List[str]


def _score_from_entropy(entropy: float) -> str:
    """
    Map entropy (bits) to a coarse label. Thresholds are opinionated but practical.
    """
    if entropy < 28:
        return "Very Weak"
    if entropy < 40:
        return "Weak"
    if entropy < 60:
        return "Moderate"
    if entropy < 80:
        return "Strong"
    return "Very Strong"


def _generate_suggestions(entropy: float, patterns: List[str]) -> List[str]:
    """
    Generate human-friendly suggestions based on entropy and detected patterns.
    Deduplicates suggestions before returning.
    """
    suggestions: List[str] = []

    # Entropy-based guidance
    if entropy < 40:
        suggestions.append("Increase length: longer passwords exponentially increase entropy.")
        suggestions.append("Include multiple character classes: lowercase, uppercase, digits, and symbols.")
    else:
        suggestions.append("Password length and character variety look reasonable.")

    # Pattern-based guidance
    if any(p.startswith("contains_year") for p in patterns):
        suggestions.append("Avoid using years or dates (birthdays) in passwords.")
    if any(p == "repeated_chars" for p in patterns):
        suggestions.append("Avoid long runs of the same character (e.g., 'aaaa').")
    if any(p == "repeated_sequence" for p in patterns):
        suggestions.append("Avoid repeated sequences like 'abcabc' or '123123'.")
    if any(p.startswith("keyboard_pattern") for p in patterns):
        suggestions.append("Avoid obvious keyboard patterns such as 'qwerty' or 'asdf'.")
    if any(p.startswith("dictionary_word") for p in patterns):
        suggestions.append("Avoid dictionary words or common substrings; consider passphrases made of unrelated words or a password manager.")
    if any(p == "common_password_list" for p in patterns):
        suggestions.append("This password appears in common password lists — do not use it for any account.")

    # Deduplicate while preserving order
    seen = set()
    out: List[str] = []
    for s in suggestions:
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def audit(password: str) -> Dict[str, object]:
    """
    Audit a password and return a dictionary with:
      - password (string)
      - entropy_bits (float)
      - patterns (list of flags)
      - score (human label)
      - suggestions (list of strings)
    """
    pwd = str(password) if password is not None else ""

    # 1) Entropy
    entropy = calculate_entropy(pwd)

    # 2) Patterns
    patterns = detect_patterns(pwd)

    # 3) Base score from entropy
    score = _score_from_entropy(entropy)

    # 4) Apply conservative downgrades if serious patterns found
    if "common_password_list" in patterns:
        score = "Very Weak"
    elif len(patterns) >= 2 and score in ("Moderate", "Strong"):
        # multiple patterns indicate predictability; be conservative
        score = "Weak"

    # 5) Suggestions
    suggestions = _generate_suggestions(entropy, patterns)

    result = AuditResult(
        password=pwd,
        entropy_bits=entropy,
        patterns=patterns,
        score=score,
        suggestions=suggestions,
    )

    # Return plain dict for JSON friendliness
    return {
        "password": result.password,
        "entropy_bits": result.entropy_bits,
        "patterns": result.patterns,
        "score": result.score,
        "suggestions": result.suggestions,
    }
