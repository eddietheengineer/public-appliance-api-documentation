#!/usr/bin/env python3
"""
Validate that all ha_domain/device_class combinations in the ERD definitions
are valid for Home Assistant. Exits with code 1 and prints errors if any
invalid combinations are found.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validator_utils import emit_error
from ha_constants import VALID_DEVICE_CLASSES, SENSOR_NON_NUMERIC_DEVICE_CLASSES, ERD_DEFINITIONS_FILE


def main():
    try:
        with open(ERD_DEFINITIONS_FILE) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        emit_error(f"Failed to load {ERD_DEFINITIONS_FILE}: {e}")
        sys.exit(1)

    error_count = 0
    defs_file = str(ERD_DEFINITIONS_FILE)

    for erd in data.get('erds', []):
        if not isinstance(erd, dict):
            continue

        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')
        device_class = erd.get('device_class')

        if not ha_domain:
            continue

        if not device_class:
            continue

        valid = VALID_DEVICE_CLASSES.get(ha_domain)
        if valid is None:
            continue

        if device_class not in valid:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): ha_domain='{ha_domain}' with "
                f"device_class='{device_class}' is invalid. "
                f"Valid values for '{ha_domain}': {sorted(valid)}",
                file=defs_file
            )

    if error_count > 0:
        print(f"Found {error_count} invalid device_class combination(s).")
        sys.exit(1)
    else:
        print("All ha_domain/device_class combinations are valid.")
        sys.exit(0)


if __name__ == '__main__':
    main()
