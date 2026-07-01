#!/usr/bin/env python3
"""
Validate that scaling_factor values are consistent with field name patterns.
Exits with code 1 and prints errors if any issues are found.

Errors (exit 1):
  - ERDs with ha_domain and a scaling pattern (x 10/100/1000) in a field name
    but no scaling_factor set
  - ERDs with scaling_factor that contradicts the field name scaling pattern
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validator_utils import emit_error
from ha_constants import ERD_DEFINITIONS_FILE

# Match x followed by a number, but not preceded by a digit or '0x' hex prefix
SCALING_PATTERN = re.compile(r'(?<!\d)(?<!0x)\bx\s*(\d+)\b', re.IGNORECASE)
HEX_REF_PATTERN = re.compile(r'0x[0-9a-fA-F]{2,}')
PLAUSIBLE_SCALING_FACTORS = {10, 100, 1000}


def find_scaling_in_field_name(name: str):
    if HEX_REF_PATTERN.search(name):
        return None
    m = SCALING_PATTERN.search(name)
    if m:
        val = int(m.group(1))
        if val in PLAUSIBLE_SCALING_FACTORS:
            return val
    return None


def main():
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    error_count = 0
    defs_file = str(ERD_DEFINITIONS_FILE)

    for erd in data.get('erds', []):
        if not isinstance(erd, dict):
            continue
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')
        scaling_factor = erd.get('scaling_factor')

        if not ha_domain:
            continue

        field_scalings = []
        for d in erd.get('data', []):
            if not isinstance(d, dict):
                continue
            fname = d.get('name', '')
            sf = find_scaling_in_field_name(fname)
            if sf is not None:
                field_scalings.append((fname, sf))

        if not field_scalings:
            continue

        if scaling_factor is None:
            for fname, sf in field_scalings:
                error_count += 1
                emit_error(
                    f"ERD {erd_id} ({name}): field '{fname}' contains scaling "
                    f"pattern 'x {sf}' but scaling_factor is not set",
                    file=defs_file
                )
        else:
            for fname, sf in field_scalings:
                if sf != scaling_factor:
                    error_count += 1
                    emit_error(
                        f"ERD {erd_id} ({name}): scaling_factor={scaling_factor} "
                        f"contradicts field name pattern 'x {sf}' "
                        f"(field: '{fname}')",
                        file=defs_file
                    )

    if error_count > 0:
        print(f"Found {error_count} scaling consistency error(s).")
        sys.exit(1)
    else:
        print("All scaling factor consistency checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
