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

SCALING_PATTERN = re.compile(r'(?<!\dx)(?<!0x)\bx\s*(\d+)\b', re.IGNORECASE)
HEX_REF_PATTERN = re.compile(r'0x[0-9a-fA-F]{3,}')
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
    defs_path = Path(__file__).parent / 'appliance_api_erd_definitions.json'
    with open(defs_path) as f:
        data = json.load(f)

    errors = []

    for erd in data.get('erds', []):
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')
        scaling_factor = erd.get('scaling_factor')

        if not ha_domain:
            continue

        field_scalings = []
        for d in erd.get('data', []):
            fname = d.get('name', '')
            sf = find_scaling_in_field_name(fname)
            if sf is not None:
                field_scalings.append((fname, sf))

        if not field_scalings:
            continue

        if scaling_factor is None:
            for fname, sf in field_scalings:
                errors.append(
                    f"ERD {erd_id} ({name}): field '{fname}' contains scaling "
                    f"pattern 'x {sf}' but scaling_factor is not set"
                )
        else:
            for fname, sf in field_scalings:
                if sf != scaling_factor:
                    errors.append(
                        f"ERD {erd_id} ({name}): scaling_factor={scaling_factor} "
                        f"contradicts field name pattern 'x {sf}' "
                        f"(field: '{fname}')"
                    )

    if errors:
        print(f"Found {len(errors)} scaling consistency error(s):")
        for err in errors:
            print(f"  ERROR: {err}")
        sys.exit(1)
    else:
        print("All scaling factor consistency checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
