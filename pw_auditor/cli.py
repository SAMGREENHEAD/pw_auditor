# pw_auditor/cli.py
"""Command-line interface for pw-auditor.

Usage:
    pw-auditor "P@ssw0rd123"
    pw-auditor -f passwords.txt
    cat passwords.txt | pw-auditor
"""

from __future__ import annotations
import argparse
import json
import sys
from typing import Iterable
from .auditor import audit


def _process_passwords(pw_iter: Iterable[str]) -> None:
    """Helper: process an iterable of password strings and print JSON results."""
    for pw in pw_iter:
        pw = pw.strip("\n\r")
        if not pw:
            continue
        try:
            result = audit(pw)
            # Print compact JSON lines for scriptability
            print(json.dumps(result, ensure_ascii=False))
        except Exception as exc:  # defensive: CLI should not crash for single bad input
            print(json.dumps({"error": str(exc), "password": pw}), file=sys.stderr)


def main(argv: list | None = None) -> int:
    """CLI entry point returning process exit code (0 on success)."""
    parser = argparse.ArgumentParser(prog="pw-auditor", description="Offline Password Strength Auditor")
    parser.add_argument("password", nargs="?", help="Password to audit (shell-escape if it contains spaces)")
    parser.add_argument("-f", "--file", help="File containing passwords (one per line)")

    args = parser.parse_args(argv)

    # Disallow using password argument and file at the same time
    if args.password and args.file:
        parser.error("Provide either a password argument or -f/--file, not both.")
        return 2

    # Single password
    if args.password:
        _process_passwords([args.password])
        return 0

    # File input
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                _process_passwords(fh)
        except FileNotFoundError:
            print(f"File not found: {args.file}", file=sys.stderr)
            return 2
        return 0

    # Piped input from stdin (non-interactive)
    if not sys.stdin.isatty():
        _process_passwords(sys.stdin)
        return 0

    # If nothing provided, show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
