#!/usr/bin/env python3
"""
Annotate per-field HA metadata in appliance_api_erd_definitions.json.

For each ERD with ha_domain and multiple non-reserved data fields, detects
per-field overrides for ha_domain, device_class, unit_of_measurement,
state_class, and scaling_factor, adding them to field dicts where they
differ from the parent-level value.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import (
    DEVICE_CLASS_KEYWORDS,
    DEVICE_CLASS_EXCLUSIONS,
    UNIT_KEYWORD_MAP,
    BINARY_SENSOR_KEYWORDS,
    TOTAL_STATE_CLASSES,
    MEASUREMENT_DEVICE_CLASSES,
    ERD_DEFINITIONS_FILE,
)
from format_json import format_erd_json, save_erd_definitions
from validator_utils import is_reserved_field, get_field_unit, detect_device_class_from_name, extract_unit_hint


def detect_field_device_class(field: dict, parent_domain: str = "") -> str:
    """Detect device_class for a specific field, considering type and values."""
    field_type = field.get("type", "")
    name = field.get("name", "")

    # Enum with <=2 values → empty (binary_sensor handles this)
    if field_type == "enum":
        values = field.get("values", {})
        if isinstance(values, dict):
            if len(values) <= 2:
                return ""
            return "enum"
        elif isinstance(values, list):
            if len(values) <= 2:
                return ""
            return "enum"

    # Enum with >2 values
    if field_type == "enum":
        return "enum"

    # Detect from name keywords
    dc = detect_device_class_from_name(name)

    # For number domain, skip duration — it's a number input, not a time sensor
    if parent_domain == "number" and dc == "duration":
        return ""

    return dc


def detect_field_ha_domain(field: dict, parent_domain: str) -> str | None:
    """Detect if a field needs a different ha_domain than the parent."""
    field_type = field.get("type", "")
    name = field.get("name", "")

    # Bool type → binary_sensor if parent is sensor
    if field_type == "bool" and parent_domain == "sensor":
        return "binary_sensor"

    # Enum with exactly 2 values containing on/off/true/false/enabled/disabled
    # Use issubset to require BOTH values to be recognized binary keywords
    if field_type == "enum" and parent_domain == "sensor":
        values = field.get("values", {})
        if isinstance(values, dict):
            if len(values) == 2:
                val_set = set(v.lower() for v in values.values())
                if val_set.issubset(BINARY_SENSOR_KEYWORDS):
                    return "binary_sensor"
        elif isinstance(values, list):
            if len(values) == 2:
                val_set = set(str(v).lower() for v in values)
                if val_set.issubset(BINARY_SENSOR_KEYWORDS):
                    return "binary_sensor"

    return None


def detect_field_state_class(field_device_class: str, parent_state_class: str, field_name: str = "") -> str | None:
    """Detect if a field needs a different state_class than the parent."""
    if not field_device_class:
        return None

    name_lower = field_name.lower()

    if field_device_class in TOTAL_STATE_CLASSES:
        # Min/max limits are measurements, not cumulative totals
        if any(kw in name_lower for kw in ("min", "max", "limit")):
            if parent_state_class != "measurement":
                return "measurement"
            return None
        if parent_state_class != "total":
            return "total"
        return None

    if field_device_class in MEASUREMENT_DEVICE_CLASSES:
        if parent_state_class != "measurement":
            return "measurement"
        return None

    return None


def detect_field_scaling_factor(field_name: str, parent_scaling: int | None) -> int | None:
    """Detect if a field needs a different scaling_factor than the parent."""
    name_lower = field_name.lower()

    # Use word-boundary-aware checks to avoid false positives
    import re as _re
    for factor_str, factor in [("x 1000", 1000), ("x 100", 100), ("x 10", 10)]:
        if _re.search(r'(?<!\w)' + re.escape(factor_str) + r'(?!\w)', name_lower):
            if factor != parent_scaling:
                return factor
    # Also check compact forms like x1000, x100, x10
    for factor_str, factor in [("x1000", 1000), ("x100", 100), ("x10", 10)]:
        if _re.search(r'(?<!\w)' + re.escape(factor_str) + r'(?!\w)', name_lower):
            if factor != parent_scaling:
                return factor
    return None


def annotate_erd(erd: dict) -> int:
    """Annotate fields within an ERD. Returns number of fields annotated."""
    ha_domain = erd.get("ha_domain")
    if not ha_domain:
        return 0

    data = erd.get("data", [])
    non_reserved = [f for f in data
                    if isinstance(f, dict) and not is_reserved_field(f.get("name", ""))]

    # Only process ERDs with multiple non-reserved fields
    if len(non_reserved) < 2:
        return 0

    parent_device_class = erd.get("device_class", "")
    parent_unit = erd.get("unit_of_measurement", "")
    parent_state_class = erd.get("state_class", "")
    parent_scaling = erd.get("scaling_factor")

    annotated = 0

    for field in non_reserved:
        name = field.get("name", "")
        field_type = field.get("type", "")
        changes = {}

        # --- ha_domain ---
        field_domain = detect_field_ha_domain(field, ha_domain)
        if field_domain and field_domain != ha_domain:
            changes["ha_domain"] = field_domain

        # --- device_class ---
        field_dc = detect_field_device_class(field, ha_domain)
        if field_dc != parent_device_class:
            changes["device_class"] = field_dc
        elif field_dc != field.get("device_class"):
            # Field has a device_class that doesn't match parent or detected value — remove it
            changes["device_class"] = ""

        # --- unit_of_measurement ---
        hint = extract_unit_hint(name)
        field_unit = get_field_unit(hint)
        if field_unit and field_unit != parent_unit:
            changes["unit_of_measurement"] = field_unit

        # --- state_class ---
        if field_dc:
            field_sc = detect_field_state_class(field_dc, parent_state_class, name)
            if field_sc and field_sc != parent_state_class:
                changes["state_class"] = field_sc

        # --- scaling_factor ---
        field_scaling = detect_field_scaling_factor(name, parent_scaling)
        if field_scaling is not None:
            changes["scaling_factor"] = field_scaling

        if changes:
            # Insert new keys after existing standard keys, before offset/size
            # We need to maintain key order: name, type, [new keys], offset, size, ...
            new_field = {}
            for k, v in field.items():
                if k in changes:
                    new_field[k] = changes[k]
                else:
                    new_field[k] = v
            # Add any changes not already in field
            for k, v in changes.items():
                if k not in new_field:
                    new_field[k] = v
            field.clear()
            field.update(new_field)
            annotated += 1

    return annotated


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Annotate per-field HA metadata in ERD definitions"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing",
    )
    args = parser.parse_args()
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    total_annotated = 0
    erds_processed = 0
    changes = []

    for erd in data.get("erds", []):
        if not isinstance(erd, dict):
            continue
        erd_id = erd.get("id", "<unknown>")
        erd_name = erd.get("name", "<unknown>")
        count = annotate_erd(erd)
        if count > 0:
            total_annotated += count
            erds_processed += 1
            for field in erd.get("data", []):
                if not isinstance(field, dict):
                    continue
                field_name = field.get("name", "")
                if any(k in field for k in ["ha_domain", "device_class", "unit_of_measurement", "state_class", "scaling_factor"]):
                    added = {k: v for k, v in field.items()
                             if k in ("ha_domain", "device_class", "unit_of_measurement", "state_class", "scaling_factor")}
                    changes.append(f"  {erd_id} ({erd_name}) → {field_name}: {added}")

    if args.dry_run:
        print(f"Would annotate {total_annotated} field(s) across {erds_processed} ERD(s):")
        for c in changes:
            print(c)
        return

    save_erd_definitions(data)

    print(f"Annotated {total_annotated} field(s) across {erds_processed} ERD(s).")
    for c in changes:
        print(c)


if __name__ == "__main__":
    main()
