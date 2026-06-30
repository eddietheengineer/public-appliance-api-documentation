#!/usr/bin/env python3
"""
Validate that all ERD pairings are symmetric: if ERD A points to ERD B
via paired_erd, then ERD B must point back to ERD A. Exits with code 1
and prints errors if any asymmetric pairings are found.
"""

import json
import sys
from pathlib import Path


def main():
    defs_path = Path(__file__).parent / 'appliance_api_erd_definitions.json'
    with open(defs_path) as f:
        data = json.load(f)

    # Build a lookup of ERDs that have pair_role
    erds = {item['id']: item for item in data.get('erds', []) if 'pair_role' in item}

    errors = []
    seen = set()

    for erd_id, item in erds.items():
        partner_id = item.get('paired_erd')
        name = item.get('name', '<unknown>')
        role = item.get('pair_role', '<unknown>')

        if not partner_id:
            continue

        # Check that the partner ERD exists
        if partner_id not in erds:
            errors.append(
                f"ERD {erd_id} ({name}, {role}): paired_erd='{partner_id}' "
                f"does not exist in the ERD definitions"
            )
            continue

        partner = erds[partner_id]
        partner_name = partner.get('name', '<unknown>')
        partner_role = partner.get('pair_role', '<unknown>')

        # Use a sorted pair key to avoid reporting the same asymmetry twice
        pair_key = tuple(sorted([erd_id, partner_id]))
        if pair_key in seen:
            continue
        seen.add(pair_key)

        # Check that the partner points back
        if partner.get('paired_erd') != erd_id:
            errors.append(
                f"ERD {erd_id} ({name}, {role}) -> {partner_id} ({partner_name}, {partner_role}), "
                f"but {partner_id} -> {partner.get('paired_erd', '<none>')}"
            )

    if errors:
        print(f"Found {len(errors)} asymmetric ERD pairing(s):")
        for err in errors:
            print(f"  ERROR: {err}")
        sys.exit(1)
    else:
        print("All ERD pairings are symmetric.")
        sys.exit(0)


if __name__ == '__main__':
    main()
