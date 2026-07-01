#!/usr/bin/env python3
"""
format_json.py

Format appliance_api_erd_definitions.json following the non-standard
compact JSON format defined in AGENTS.md.

Shared by all scripts that modify the JSON file.
"""

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import ERD_DEFINITIONS_FILE


def format_erd_json(data: dict) -> str:
    """Format JSON following AGENTS.md compact format rules."""
    lines = ["{"]

    # Format erds array
    erds = data.get("erds", [])

    for i, erd in enumerate(erds):
        # First ERD: "erds": [{  ; subsequent: }, {
        if i == 0:
            lines.append('  "erds": [{')
        else:
            lines.append("  }, {")

        # Get all keys in order
        keys = list(erd.keys())

        for j, key in enumerate(keys):
            value = erd[key]
            is_last = (j == len(keys) - 1)
            comma = "" if is_last else ","

            # Format value based on type
            if isinstance(value, list):
                if all(isinstance(item, (str, int, float, bool)) or item is None for item in value):
                    # Primitive array: single line
                    formatted_items = [json.dumps(item, ensure_ascii=False) for item in value]
                    lines.append(f'    "{key}": [{", ".join(formatted_items)}]{comma}')
                else:
                    # Object array: special formatting
                    lines.append(f'    "{key}": [{{')
                    for k, item in enumerate(value):
                        if k > 0:
                            lines.append("    }, {")

                        item_keys = list(item.keys())
                        for m, item_key in enumerate(item_keys):
                            item_value = item[item_key]
                            item_is_last = (m == len(item_keys) - 1)
                            item_comma = "" if item_is_last else ","

                            if isinstance(item_value, dict):
                                lines.append(f'      "{item_key}": {{')
                                dict_keys = list(item_value.keys())
                                for n, dict_key in enumerate(dict_keys):
                                    dict_value = item_value[dict_key]
                                    dict_is_last = (n == len(dict_keys) - 1)
                                    dict_comma = "" if dict_is_last else ","
                                    lines.append(f'        "{dict_key}": {json.dumps(dict_value, ensure_ascii=False)}{dict_comma}')
                                lines.append(f'      }}{item_comma}')
                            else:
                                lines.append(f'      "{item_key}": {json.dumps(item_value, ensure_ascii=False)}{item_comma}')

                    lines.append(f'    }}]{comma}')
            elif isinstance(value, dict):
                lines.append(f'    "{key}": {{')
                dict_keys = list(value.keys())
                for k, dict_key in enumerate(dict_keys):
                    dict_value = value[dict_key]
                    dict_is_last = (k == len(dict_keys) - 1)
                    dict_comma = "" if dict_is_last else ","
                    lines.append(f'      "{dict_key}": {json.dumps(dict_value, ensure_ascii=False)}{dict_comma}')
                lines.append(f'    }}{comma}')
            else:
                lines.append(f'    "{key}": {json.dumps(value, ensure_ascii=False)}{comma}')

    # Close last ERD and array
    if erds:
        lines.append("  }]")
    else:
        lines.append('  "erds": []')
    lines.append("}")

    return "\n".join(lines) + "\n"


def save_erd_definitions(data: dict) -> None:
    """Save ERD definitions with custom formatting per AGENTS.md rules.
    
    Writes to a temp file first, validates JSON, then atomically replaces.
    """

    formatted = format_erd_json(data)

    # Write to temp file first, validate, then move
    dir_name = ERD_DEFINITIONS_FILE.parent
    fd, tmp_path = tempfile.mkstemp(suffix=".json", dir=str(dir_name))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(formatted)

        # Verify the output is valid JSON
        with open(tmp_path, encoding="utf-8") as f:
            json.load(f)

        # Atomic replace
        shutil.move(tmp_path, str(ERD_DEFINITIONS_FILE))
    except Exception:
        # Clean up temp file on failure
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise



def load_erd_definitions() -> dict:
    """Load ERD definitions with error handling."""

    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Cannot read {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)
