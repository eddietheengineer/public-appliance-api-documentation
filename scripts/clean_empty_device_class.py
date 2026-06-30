#!/usr/bin/env python3
"""
Remove device_class: "" entries from ERD field definitions.

The generator treats missing device_class the same as "", so these entries
are just noise. This script removes them while preserving the compact JSON
formatting.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from format_json import (
    ERD_DEFINITIONS_FILE,
    format_erd_json,
    load_erd_definitions,
    save_erd_definitions,
)


def remove_empty_device_class(data: dict) -> int:
    """Remove device_class: "" from all fields. Returns count of removals."""
    removed = 0
    for erd in data.get("erds", []):
        if not isinstance(erd, dict):
            continue
        for field in erd.get("data", []):
            if field.get("device_class") == "":
                del field["device_class"]
                removed += 1
    return removed


def main():
    data = load_erd_definitions()

    removed = remove_empty_device_class(data)
    print(f"Removed {removed} device_class: \"\" entries", file=sys.stderr)

    formatted = format_erd_json(data)
    save_erd_definitions(data)

    # Verify
    reloaded = load_erd_definitions()

    remaining = sum(
        1 for erd in reloaded.get("erds", [])
        if isinstance(erd, dict)
        for field in erd.get("data", [])
        if field.get("device_class") == ""
    )
    print(f"Remaining device_class: \"\" entries: {remaining}", file=sys.stderr)
    print(f"JSON valid: True, {len(reloaded.get('erds', []))} ERDs", file=sys.stderr)


if __name__ == "__main__":
    main()
