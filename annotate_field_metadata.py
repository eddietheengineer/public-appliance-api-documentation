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

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR / "appliance_api_erd_definitions.json"

NUMERIC_TYPES = {"u8", "u16", "u32", "i8", "i16", "i32"}

DEVICE_CLASS_KEYWORDS = {
    "temperature": ["temperature", "temp"],
    "voltage": ["voltage", "volts"],
    "current": ["current"],
    "power": ["power"],
    "humidity": ["humidity"],
    "pressure": ["pressure"],
    "energy": ["energy", "watt seconds", "watt-hours", "wh"],
    "duration": ["duration", "time", "timer", "timeout"],
    "frequency": ["frequency", "hertz"],
    "speed": ["speed", "rpm"],
    "weight": ["weight", "mass"],
    "volume": ["volume", "gallons", "liters"],
    "distance": ["distance"],
    "battery": ["battery"],
    "signal_strength": ["rssi"],
    "illuminance": ["illuminance", "lux"],
}

DEVICE_CLASS_EXCLUSIONS = {
    "power": ["power off", "power on"],
    "current": ["current limit"],
}

UNIT_KEYWORD_MAP = {
    "volts": "V",
    "amps": "A",
    "watts": "W",
    "fahrenheit": "°F",
    "degf": "°F",
    "celsius": "°C",
    "degc": "°C",
    "percent": "%",
    "hertz": "Hz",
    "minutes": "min",
    "seconds": "s",
    "gallons": "gal",
    "liters": "L",
    "hours": "h",
}

BINARY_SENSOR_KEYWORDS = {"on", "off", "true", "false", "enabled", "disabled"}

TOTAL_STATE_CLASSES = {"energy", "gas", "water", "volume"}
MEASUREMENT_DEVICE_CLASSES = {
    "temperature", "voltage", "current", "power", "humidity", "pressure",
    "frequency", "speed", "weight", "distance", "battery", "signal_strength",
    "illuminance", "moisture", "duration",
}


def is_reserved_field(name: str) -> bool:
    return "reserved" in name.lower()


def extract_unit_hint(field_name: str) -> str:
    m = re.search(r"\(([^)]+)\)", field_name)
    if m:
        hint = m.group(1).strip().lower()
        hint = re.sub(r"x\s*\d+", "", hint).strip()
        return hint
    m = re.search(r"in\s+(fahrenheit|celsius)\s*(?:x\s*\d+)?", field_name, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    return ""


def get_field_unit(hint: str) -> str:
    for keyword, unit in UNIT_KEYWORD_MAP.items():
        if keyword in hint:
            return unit
    return ""


def detect_device_class_from_name(name: str) -> str:
    name_lower = name.lower()
    for device_class, keywords in DEVICE_CLASS_KEYWORDS.items():
        for keyword in keywords:
            if keyword in name_lower:
                exclusions = DEVICE_CLASS_EXCLUSIONS.get(device_class, [])
                if any(excl in name_lower for excl in exclusions):
                    continue
                return device_class
    return ""


def detect_field_device_class(field: dict) -> str:
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
    return detect_device_class_from_name(name)


def detect_field_ha_domain(field: dict, parent_domain: str) -> str | None:
    """Detect if a field needs a different ha_domain than the parent."""
    field_type = field.get("type", "")
    name = field.get("name", "")

    # Bool type → binary_sensor if parent is sensor
    if field_type == "bool" and parent_domain == "sensor":
        return "binary_sensor"

    # Enum with exactly 2 values containing on/off/true/false/enabled/disabled
    if field_type == "enum" and parent_domain == "sensor":
        values = field.get("values", {})
        if isinstance(values, dict):
            if len(values) == 2:
                val_set = set(v.lower() for v in values.values())
                if val_set & BINARY_SENSOR_KEYWORDS:
                    return "binary_sensor"
        elif isinstance(values, list):
            if len(values) == 2:
                val_set = set(str(v).lower() for v in values)
                if val_set & BINARY_SENSOR_KEYWORDS:
                    return "binary_sensor"

    return None


def detect_field_state_class(field_device_class: str, parent_state_class: str) -> str | None:
    """Detect if a field needs a different state_class than the parent."""
    if not field_device_class:
        return None

    if field_device_class in TOTAL_STATE_CLASSES:
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

    if "x 1000" in name_lower or "x1000" in name_lower:
        factor = 1000
    elif "x 100" in name_lower or "x100" in name_lower:
        factor = 100
    elif "x 10" in name_lower or "x10" in name_lower:
        factor = 10
    else:
        return None

    if factor != parent_scaling:
        return factor
    return None


def annotate_erd(erd: dict) -> int:
    """Annotate fields within an ERD. Returns number of fields annotated."""
    ha_domain = erd.get("ha_domain")
    if not ha_domain:
        return 0

    data = erd.get("data", [])
    non_reserved = [f for f in data if not is_reserved_field(f.get("name", ""))]

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
        field_dc = detect_field_device_class(field)
        if field_dc != parent_device_class:
            changes["device_class"] = field_dc

        # --- unit_of_measurement ---
        hint = extract_unit_hint(name)
        field_unit = get_field_unit(hint)
        if field_unit and field_unit != parent_unit:
            changes["unit_of_measurement"] = field_unit

        # --- state_class ---
        if field_dc:
            field_sc = detect_field_state_class(field_dc, parent_state_class)
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

    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    total_annotated = 0
    erds_processed = 0
    changes = []

    for erd in data.get("erds", []):
        erd_id = erd.get("id", "<unknown>")
        erd_name = erd.get("name", "<unknown>")
        count = annotate_erd(erd)
        if count > 0:
            total_annotated += count
            erds_processed += 1
            for field in erd.get("data", []):
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

    formatted = format_erd_json(data)

    with ERD_DEFINITIONS_FILE.open("w", encoding="utf-8") as f:
        f.write(formatted)

    # Verify the output is valid JSON
    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        json.load(f)

    print(f"Annotated {total_annotated} field(s) across {erds_processed} ERD(s).")
    for c in changes:
        print(c)


if __name__ == "__main__":
    main()
