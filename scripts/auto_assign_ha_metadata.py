#!/usr/bin/env python3
"""
auto_assign_ha_metadata.py

Suggest Home Assistant metadata for unmapped ERDs based on data types and field names.
Outputs a markdown report with suggestions for human review.

Usage:
    python3 auto_assign_ha_metadata.py
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import (
    ERD_DEFINITIONS_FILE,
    NUMERIC_TYPES,
    DEVICE_CLASS_KEYWORDS,
    DEVICE_CLASS_EXCLUSIONS,
    UNIT_KEYWORD_MAP,
    BINARY_SENSOR_KEYWORDS,
    VALID_DEVICE_CLASSES,
    SENSOR_NON_NUMERIC_DEVICE_CLASSES,
)

OUTPUT_FILE = Path(__file__).parent.parent / "doc" / "ha_metadata_suggestions.md"


def is_reserved_field(name: str) -> bool:
    return name.lower().startswith("reserved")


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


def detect_button_device_class(name: str) -> str:
    """Detect device_class for button domain from ERD name."""
    name_lower = name.lower()
    if any(kw in name_lower for kw in ["reset", "restart", "reboot"]):
        return "restart"
    if "identify" in name_lower:
        return "identify"
    if "update" in name_lower:
        return "update"
    return ""


def infer_ha_domain(erd: dict) -> tuple[str, str]:
    """
    Infer ha_domain from data type and operations.
    Returns (domain, confidence).
    """
    operations = erd.get("operations", [])
    is_writable = "write" in operations
    fields = [f for f in erd.get("data", [])
               if isinstance(f, dict) and not is_reserved_field(f.get("name", ""))]

    if not fields:
        return "", "none"

    primary_field = fields[0]
    field_type = primary_field.get("type", "")

    if field_type == "bool":
        if is_writable:
            return "switch", "medium"
        return "binary_sensor", "high"

    if field_type == "enum":
        if is_writable:
            values = primary_field.get("values", {})
            if isinstance(values, dict) and len(values) == 2:
                val_set = set(v.lower() for v in values.values())
                # Use issubset to require BOTH values to be recognized binary keywords
                if val_set.issubset(BINARY_SENSOR_KEYWORDS):
                    return "switch", "medium"
            return "select", "medium"
        return "sensor", "high"

    if field_type in NUMERIC_TYPES:
        if is_writable:
            return "number", "medium"
        return "sensor", "high"

    if field_type == "string":
        return "sensor", "high"

    return "", "none"


def generate_suggestion(erd: dict) -> dict:
    """Generate HA metadata suggestion for an ERD."""
    erd_id = erd.get("id", "<unknown>")
    name = erd.get("name", "<unknown>")
    fields = [f for f in erd.get("data", [])
               if isinstance(f, dict) and not is_reserved_field(f.get("name", ""))]

    ha_domain, domain_confidence = infer_ha_domain(erd)
    if not ha_domain:
        return None

    suggestion = {
        "erd_id": erd_id,
        "name": name,
        "ha_domain": ha_domain,
        "confidence": domain_confidence,
        "reasons": [],
    }

    if ha_domain in ("sensor", "number"):
        device_class = detect_device_class_from_name(name)
        if device_class and device_class in VALID_DEVICE_CLASSES.get(ha_domain, set()):
            suggestion["device_class"] = device_class
            suggestion["reasons"].append(f"device_class inferred from name keyword")

        unit_of_measurement = ""
        if fields:
            hint = extract_unit_hint(fields[0].get("name", ""))
            if hint:
                unit_of_measurement = get_field_unit(hint)
        if unit_of_measurement:
            suggestion["unit_of_measurement"] = unit_of_measurement
            suggestion["reasons"].append(f"unit inferred from field name pattern")

        if ha_domain == "sensor" and device_class in ("energy", "gas", "water", "volume"):
            suggestion["state_class"] = "total"
            suggestion["reasons"].append(f"state_class inferred from device_class")
        elif ha_domain == "sensor" and device_class and device_class not in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
            suggestion["state_class"] = "measurement"
            suggestion["reasons"].append(f"state_class inferred from device_class")

    if ha_domain == "binary_sensor":
        device_class = detect_device_class_from_name(name)
        if device_class and device_class in VALID_DEVICE_CLASSES.get("binary_sensor", set()):
            suggestion["device_class"] = device_class
            suggestion["reasons"].append(f"device_class inferred from name keyword")

    comment_parts = [f"Auto-suggested: {name}"]
    if suggestion["reasons"]:
        comment_parts.append(f" ({', '.join(suggestion['reasons'])})")
    suggestion["comment"] = "".join(comment_parts)

    return suggestion


def generate_report(suggestions: list[dict]) -> str:
    """Generate markdown report of suggestions."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# HA Metadata Suggestions",
        "",
        f"Generated: {timestamp}",
        "",
        f"**Total suggestions: {len(suggestions)}**",
        "",
    ]

    by_confidence = {"high": [], "medium": [], "low": []}
    for s in suggestions:
        conf = s.get("confidence", "low")
        if conf in by_confidence:
            by_confidence[conf].append(s)

    for conf_level in ("high", "medium", "low"):
        conf_suggestions = by_confidence[conf_level]
        if not conf_suggestions:
            continue

        lines += [
            f"## {conf_level.capitalize()} Confidence ({len(conf_suggestions)})",
            "",
            "| ERD ID | Name | ha_domain | device_class | unit | state_class | confidence | comment |",
            "|--------|------|-----------|--------------|------|-------------|------------|---------|",
        ]

        for s in conf_suggestions:
            device_class = s.get("device_class", "")
            unit = s.get("unit_of_measurement", "")
            state_class = s.get("state_class", "")
            comment = s.get("comment", "").replace("|", "\\|")
            lines.append(
                f"| {s['erd_id']} | {s['name']} | {s['ha_domain']} "
                f"| {device_class} | {unit} | {state_class} "
                f"| {s['confidence']} | {comment} |"
            )

        lines.append("")

    lines += [
        "## Review Notes",
        "",
        "- **High confidence**: Suggestions based on clear type mappings (bool → binary_sensor, numeric → sensor)",
        "- **Medium confidence**: Suggestions based on writable status or enum heuristics",
        "- **Low confidence**: Suggestions that need manual verification",
        "- All suggestions should be reviewed before applying to the JSON file",
        "- Use surgical text edits per AGENTS.md rules when applying suggestions",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    try:
        with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {ERD_DEFINITIONS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    erds = data.get("erds", [])
    unmapped = [e for e in erds if isinstance(e, dict) and not e.get("ha_domain")]

    print(f"Found {len(unmapped)} ERDs without ha_domain")

    suggestions = []
    for erd in unmapped:
        suggestion = generate_suggestion(erd)
        if suggestion:
            suggestions.append(suggestion)

    print(f"Generated {len(suggestions)} suggestions")

    report = generate_report(suggestions)
    print(report)

    github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with open(github_step_summary, "a", encoding="utf-8") as f:
            f.write(report)
        print("Written suggestions to GitHub Step Summary")


if __name__ == "__main__":
    main()
