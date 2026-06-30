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
import re
import sys
from pathlib import Path

UNIT_IMPLYING_DEVICE_CLASSES = {
    'temperature', 'voltage', 'current', 'power', 'energy', 'humidity',
    'pressure', 'atmospheric_pressure', 'speed', 'frequency', 'battery',
    'illuminance', 'signal_strength', 'weight', 'volume', 'volume_storage',
    'volume_flow_rate', 'water', 'gas', 'distance', 'duration',
    'precipitation', 'wind_speed',
}

VALID_STATE_CLASSES = {'measurement', 'total', 'total_increasing'}

UNIT_KEYWORD_MAP = {
    'volts': 'V',
    'amps': 'A',
    'watts': 'W',
    'fahrenheit': '°F',
    'degf': '°F',
    'celsius': '°C',
    'degc': '°C',
    'percent': '%',
    'hertz': 'Hz',
    'minutes': 'min',
    'seconds': 's',
}


def is_reserved_field(name: str) -> bool:
    return 'reserved' in name.lower()


def extract_unit_hint(field_name: str) -> str:
    m = re.search(r'\(([^)]+)\)', field_name)
    if not m:
        return ''
    hint = m.group(1).strip().lower()
    hint = re.sub(r'x\s*\d+', '', hint).strip()
    return hint


def get_field_unit(hint: str) -> str:
    for keyword, unit in UNIT_KEYWORD_MAP.items():
        if keyword in hint:
            return unit
    return ''


def main():
    defs_path = Path(__file__).parent / 'appliance_api_erd_definitions.json'
    with open(defs_path) as f:
        data = json.load(f)

    errors = []
    warnings = []

    for erd in data.get('erds', []):
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

        if device_class in UNIT_IMPLYING_DEVICE_CLASSES and not unit_of_measurement:
            errors.append(
                f"ERD {erd_id} ({name}): device_class='{device_class}' implies a "
                f"unit but unit_of_measurement is missing"
            )

        if state_class and state_class not in VALID_STATE_CLASSES:
            errors.append(
                f"ERD {erd_id} ({name}): state_class='{state_class}' is invalid. "
                f"Valid values: {sorted(VALID_STATE_CLASSES)}"
            )

        non_reserved = [d for d in fields if not is_reserved_field(d.get('name', ''))]
        if unit_of_measurement and len(non_reserved) == 1:
            fname = non_reserved[0].get('name', '')
            hint = extract_unit_hint(fname)
            if hint:
                field_unit = get_field_unit(hint)
                if field_unit and field_unit != unit_of_measurement:
                    errors.append(
                        f"ERD {erd_id} ({name}): unit_of_measurement='{unit_of_measurement}' "
                        f"contradicts field name unit '{field_unit}' "
                        f"(field: '{fname}')"
                    )

        if not confidence:
            warnings.append(f"ERD {erd_id} ({name}): missing 'confidence' field")
        if not comment:
            warnings.append(f"ERD {erd_id} ({name}): missing 'comment' field")

    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  WARNING: {w}")
        print()

    if errors:
        print(f"Found {len(errors)} error(s):")
        for err in errors:
            print(f"  ERROR: {err}")
        sys.exit(1)
    else:
        print("All HA metadata completeness checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
