#!/usr/bin/env python3
"""
Validate that all ERD pairings are symmetric: if ERD A points to ERD B
via paired_erd, then ERD B must point back to ERD A. Exits with code 1
and prints errors if any asymmetric pairings are found.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validator_utils import emit_error
from ha_constants import ERD_DEFINITIONS_FILE


def main():
    try:
        with open(ERD_DEFINITIONS_FILE) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        emit_error(f"Failed to read {ERD_DEFINITIONS_FILE}: {e}")
        sys.exit(1)

    if not isinstance(data, dict):
        emit_error(f"Expected a JSON object in {ERD_DEFINITIONS_FILE}")
        sys.exit(1)

    erds = {item['id']: item for item in data.get('erds', []) if isinstance(item, dict) and 'pair_role' in item}

    error_count = 0
    seen = set()
    defs_file = str(ERD_DEFINITIONS_FILE)

    for erd_id, item in erds.items():
        if not isinstance(item, dict):
            continue

        partner_id = item.get('paired_erd')
        name = item.get('name', '<unknown>')
        role = item.get('pair_role', '<unknown>')

        if not partner_id:
            continue

        if partner_id not in erds:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}, {role}): paired_erd='{partner_id}' "
                f"does not exist in the ERD definitions",
                file=defs_file
            )
            continue

        partner = erds[partner_id]
        if not isinstance(partner, dict):
            continue

        partner_name = partner.get('name', '<unknown>')
        partner_role = partner.get('pair_role', '<unknown>')

        pair_key = tuple(sorted([erd_id, partner_id]))
        if pair_key in seen:
            continue
        seen.add(pair_key)

        if partner.get('paired_erd') != erd_id:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}, {role}) -> {partner_id} ({partner_name}, {partner_role}), "
                f"but {partner_id} -> {partner.get('paired_erd', '<none>')}",
                file=defs_file
            )

    if error_count > 0:
        print(f"Found {error_count} asymmetric ERD pairing(s).")
        sys.exit(1)
    else:
        print("All ERD pairings are symmetric.")
        sys.exit(0)


if __name__ == '__main__':
    main()
