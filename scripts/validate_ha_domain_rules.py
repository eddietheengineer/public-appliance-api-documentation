#!/usr/bin/env python3
"""
Validate that ERD metadata follows Home Assistant domain-specific rules.
Based on Home Assistant core source code validation logic.

Checks:
  - Sensor/number domains: numeric device_class requires numeric field types (u8/u16/u32/i8/i16/i32)
  - Sensor: non-numeric device_class cannot have unit_of_measurement or state_class
  - Sensor: unit_of_measurement must be valid for device_class
  - Sensor: state_class must be valid for device_class
  - Binary sensor: cannot have unit_of_measurement or state_class; device_class must be valid
  - Number: cannot have state_class; non-numeric device_class is invalid
  - Select: cannot have unit_of_measurement or state_class; device_class must be valid
  - Switch: cannot have unit_of_measurement or state_class; device_class must be valid
  - Button: device_class must be valid (identify/restart/update)

Exits with code 1 and prints errors if any violations are found.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from validator_utils import emit_error, is_reserved_field
from ha_constants import (
    ERD_DEFINITIONS_FILE,
    BINARY_SENSOR_DEVICE_CLASSES,
    NUMERIC_TYPES,
    SENSOR_NON_NUMERIC_DEVICE_CLASSES,
    SENSOR_DEVICE_CLASS_UNITS,
    SENSOR_DEVICE_CLASS_STATE_CLASSES,
    STATE_CLASS_UNITS,
    NUMBER_DEVICE_CLASS_UNITS,
    VALID_DEVICE_CLASSES,
)

def validate_sensor(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate sensor domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement') or None
    state_class = erd.get('state_class') or ''
    fields = erd.get('data', [])

    # Numeric device classes require numeric field types
    if device_class and device_class not in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
        for field in fields:
            if not isinstance(field, dict):
                continue
            if is_reserved_field(field.get('name', '')):
                continue
            ftype = field.get('type', '')
            if ftype and ftype not in NUMERIC_TYPES:
                error_count += 1
                emit_error(
                    f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                    f"requires numeric fields but field '{field.get('name', '')}' has type='{ftype}'",
                    file=defs_file
                )
                break  # one error per ERD is enough

    # Non-numeric device classes cannot have unit_of_measurement or state_class
    if device_class in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
        if unit_of_measurement:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"cannot have unit_of_measurement='{unit_of_measurement}'",
                file=defs_file
            )
        if state_class:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"cannot have state_class='{state_class}'",
                file=defs_file
            )

    # Validate unit_of_measurement for device_class
    if device_class and unit_of_measurement:
        valid_units = SENSOR_DEVICE_CLASS_UNITS.get(device_class)
        # monetary uses any ISO4217 code; skip validation (empty set means skip)
        if valid_units is not None and valid_units and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    # Validate state_class for device_class
    if device_class and state_class:
        valid_state_classes = SENSOR_DEVICE_CLASS_STATE_CLASSES.get(device_class)
        if valid_state_classes is not None and state_class not in valid_state_classes:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"has invalid state_class='{state_class}'. "
                f"Valid state_classes: {sorted([str(sc) for sc in valid_state_classes]) or 'none'}",
                file=defs_file
            )

    # Validate unit_of_measurement for state_class
    if state_class and unit_of_measurement:
        valid_units = STATE_CLASS_UNITS.get(state_class)
        if valid_units is not None and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with state_class='{state_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    return error_count


def validate_binary_sensor(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate binary_sensor domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')

    # binary_sensor cannot have unit_of_measurement
    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    # binary_sensor cannot have state_class
    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor cannot have state_class='{state_class}'",
            file=defs_file
        )

    # Validate device_class
    if device_class and device_class not in BINARY_SENSOR_DEVICE_CLASSES:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor has invalid device_class='{device_class}'. "
            f"Valid device_classes: {sorted(BINARY_SENSOR_DEVICE_CLASSES)}",
            file=defs_file
        )

    return error_count


def validate_number(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate number domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement') or None
    state_class = erd.get('state_class')
    fields = erd.get('data', [])

    # Number domain requires numeric field types
    for field in fields:
        if not isinstance(field, dict):
            continue
        if is_reserved_field(field.get('name', '')):
            continue
        ftype = field.get('type', '')
        if ftype and ftype not in NUMERIC_TYPES:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): number domain requires numeric fields "
                f"but field '{field.get('name', '')}' has type='{ftype}'",
                file=defs_file
            )
            break  # one error per ERD is enough
    """Validate number domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement') or None
    state_class = erd.get('state_class')

    # number cannot have state_class
    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): number cannot have state_class='{state_class}'",
            file=defs_file
        )

    # Validate device_class (cannot be date/enum/timestamp/uptime)
    if device_class and device_class in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): number cannot have device_class='{device_class}'",
            file=defs_file
        )

    # Validate unit_of_measurement for device_class
    if device_class and unit_of_measurement:
        valid_units = NUMBER_DEVICE_CLASS_UNITS.get(device_class)
        # monetary uses any ISO4217 code; skip validation (empty set means skip)
        if valid_units is not None and valid_units and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): number with device_class='{device_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    return error_count


def validate_select(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate select domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have device_class='{device_class}'",
            file=defs_file
        )

    return error_count


def validate_switch(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate switch domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have device_class='{device_class}'",
            file=defs_file
        )

    return error_count


def validate_button(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate button domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        VALID_BUTTON_DEVICE_CLASSES = VALID_DEVICE_CLASSES.get("button", set())
        if device_class not in VALID_BUTTON_DEVICE_CLASSES:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): button has invalid device_class='{device_class}'. "
                f"Valid values: {sorted(VALID_BUTTON_DEVICE_CLASSES)}",
                file=defs_file
            )

    return error_count


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
    defs_file = str(ERD_DEFINITIONS_FILE)

    for erd in data.get('erds', []):
        if not isinstance(erd, dict):
            continue
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')

        if not ha_domain:
            continue

        if ha_domain == 'sensor':
            error_count += validate_sensor(erd, erd_id, name, defs_file)
        elif ha_domain == 'binary_sensor':
            error_count += validate_binary_sensor(erd, erd_id, name, defs_file)
        elif ha_domain == 'number':
            error_count += validate_number(erd, erd_id, name, defs_file)
        elif ha_domain == 'select':
            error_count += validate_select(erd, erd_id, name, defs_file)
        elif ha_domain == 'switch':
            error_count += validate_switch(erd, erd_id, name, defs_file)
        elif ha_domain == 'button':
            error_count += validate_button(erd, erd_id, name, defs_file)

    if error_count > 0:
        print(f"Found {error_count} HA domain rule violation(s).")
        sys.exit(1)
    else:
        print("All HA domain rule checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
