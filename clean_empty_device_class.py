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

SCRIPT_DIR = Path(__file__).parent
ERD_FILE = SCRIPT_DIR / "appliance_api_erd_definitions.json"


def remove_empty_device_class(data: dict) -> int:
    """Remove device_class: "" from all fields. Returns count of removals."""
    removed = 0
    for erd in data.get("erds", []):
        for field in erd.get("data", []):
            if field.get("device_class") == "":
                del field["device_class"]
                removed += 1
    return removed


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


def main():
    with ERD_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    removed = remove_empty_device_class(data)
    print(f"Removed {removed} device_class: \"\" entries", file=sys.stderr)

    formatted = format_erd_json(data)
    with ERD_FILE.open("w", encoding="utf-8") as f:
        f.write(formatted)

    # Verify
    with ERD_FILE.open(encoding="utf-8") as f:
        reloaded = json.load(f)

    remaining = sum(
        1 for erd in reloaded.get("erds", [])
        for field in erd.get("data", [])
        if field.get("device_class") == ""
    )
    print(f"Remaining device_class: \"\" entries: {remaining}", file=sys.stderr)
    print(f"JSON valid: True, {len(reloaded.get('erds', []))} ERDs", file=sys.stderr)


if __name__ == "__main__":
    main()
