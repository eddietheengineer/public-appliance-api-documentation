#!/usr/bin/env python3
"""
Validate that all ERDs with ha_domain have complete and consistent Home Assistant metadata.
Exits with code 1 and prints errors if any issues are found.

Errors (exit 1):
  - Sensors with unit-implying device_class but no unit_of_measurement
  - Single-field ERDs where field name unit contradicts unit_of_measurement
  - Invalid state_class values

Warnings (print but exit 0):
  - ERDs with ha_domain but missing confidence or comment
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validator_utils import emit_error, emit_warning, is_reserved_field, extract_unit_hint, get_field_unit
from ha_constants import (
    UNIT_IMPLYING_DEVICE_CLASSES,
    VALID_STATE_CLASSES,
    ERD_DEFINITIONS_FILE,
)


def main():
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as e:
        print(f"ERROR: Cannot read {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    error_count = 0
    warning_count = 0
    defs_file = str(ERD_DEFINITIONS_FILE)

    for erd in data.get('erds', []):
        if not isinstance(erd, dict):
            continue
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')

        if not ha_domain:
            continue

        device_class = erd.get('device_class') or ''
        unit_of_measurement = erd.get('unit_of_measurement') or ''
        state_class = erd.get('state_class') or ''
        confidence = erd.get('confidence')
        comment = erd.get('comment')
        fields = erd.get('data', [])

        if ha_domain in ('sensor', 'number') and device_class in UNIT_IMPLYING_DEVICE_CLASSES and not unit_of_measurement:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): device_class='{device_class}' implies a "
                f"unit but unit_of_measurement is missing",
                file=defs_file
            )

        if state_class and state_class not in VALID_STATE_CLASSES:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): state_class='{state_class}' is invalid. "
                f"Valid values: {sorted(VALID_STATE_CLASSES)}",
                file=defs_file
            )

        non_reserved = [d for d in fields
                        if isinstance(d, dict) and not is_reserved_field(d.get('name', ''))]
        if unit_of_measurement and len(non_reserved) == 1:
            fname = non_reserved[0].get('name', '')
            hint = extract_unit_hint(fname)
            if hint:
                field_unit = get_field_unit(hint)
                if field_unit and field_unit != unit_of_measurement:
                    error_count += 1
                    emit_error(
                        f"ERD {erd_id} ({name}): unit_of_measurement='{unit_of_measurement}' "
                        f"contradicts field name unit '{field_unit}' "
                        f"(field: '{fname}')",
                        file=defs_file
                    )

        if not confidence:
            warning_count += 1
            emit_warning(f"ERD {erd_id} ({name}): missing 'confidence' field", file=defs_file)
        if not comment:
            warning_count += 1
            emit_warning(f"ERD {erd_id} ({name}): missing 'comment' field", file=defs_file)

    if error_count > 0:
        print(f"Found {error_count} error(s) and {warning_count} warning(s).")
        sys.exit(1)
    else:
        print(f"All HA metadata completeness checks passed. ({warning_count} warnings)")
        sys.exit(0)


if __name__ == '__main__':
    main()
