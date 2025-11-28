# pw_auditor/__init__.py
"""Public API for pw_auditor package.

This file re-exports the main `audit` function so users can do:
    from pw_auditor import audit
"""
from .auditor import audit  # re-export for convenience

__all__ = ["audit"]
