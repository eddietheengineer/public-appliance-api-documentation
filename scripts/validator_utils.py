#!/usr/bin/env python3
"""
Shared utilities for all validator scripts.
Provides consistent error/warning emission and CI detection.
"""

import os

IN_GITHUB_ACTIONS = os.environ.get('GITHUB_ACTIONS') == 'true'


def emit_error(message: str, file: str = "", line: int = 0) -> None:
    """Emit an error message, using GitHub Actions annotation format if in CI."""
    if IN_GITHUB_ACTIONS:
        if file and line:
            print(f"::error file={file},line={line}::{message}")
        else:
            print(f"::error::{message}")
    else:
        print(f"  ERROR: {message}")


def emit_warning(message: str, file: str = "", line: int = 0) -> None:
    """Emit a warning message, using GitHub Actions annotation format if in CI."""
    if IN_GITHUB_ACTIONS:
        if file and line:
            print(f"::warning file={file},line={line}::{message}")
        else:
            print(f"::warning::{message}")
    else:
        print(f"  WARNING: {message}")
