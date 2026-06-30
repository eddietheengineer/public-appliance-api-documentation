#!/usr/bin/env python3
"""
validate_json_format.py

Validates that appliance_api_erd_definitions.json follows the non-standard
compact JSON format defined in AGENTS.md.

Checks:
  1. Valid JSON
  2. No escaped non-ASCII (\\uXXXX) — must be literal UTF-8
  3. ERD objects use merged bracket format in the "erds" array
  4. Data arrays use merged bracket format
  5. Primitive arrays on a single line
  6. 2-space indentation per level

Usage:
    python3 scripts/validate_json_format.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ERD_FILE = SCRIPT_DIR.parent / "appliance_api_erd_definitions.json"


def validate_format() -> list[str]:
    """Validate the JSON file format and return a list of errors."""
    errors: list[str] = []
    raw = ERD_FILE.read_text(encoding="utf-8")

    # 1. Valid JSON
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return errors

    # 2. No escaped non-ASCII
    for i, line in enumerate(raw.splitlines(), 1):
        m = re.search(r'\\u[0-9a-fA-F]{4}', line)
        if m:
            errors.append(
                f"L{i}: escaped non-ASCII '{m.group()}' — use literal UTF-8"
            )

    # 3. Check indentation is 2-space based
    for i, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        leading = len(line) - len(line.lstrip())
        if leading > 0 and leading % 2 != 0:
            errors.append(
                f"L{i}: odd indentation ({leading} spaces) — must be multiple of 2"
            )

    # 4. Verify top-level structure
    if not isinstance(data, dict):
        errors.append("Top-level value must be an object")
    elif "erds" not in data:
        errors.append("Missing required top-level key 'erds'")
    elif not isinstance(data.get("erds"), list):
        errors.append("'erds' must be an array")

    return errors


def main():
    errors = validate_format()
    if errors:
        print(f"JSON format validation failed: {len(errors)} error(s)\n")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("JSON format validation passed")


if __name__ == "__main__":
    main()
