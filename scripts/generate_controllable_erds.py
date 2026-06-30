#!/usr/bin/env python3
"""
generate_controllable_erds.py

Reads appliance_api_erd_definitions.json, identifies ERDs that can be
controlled (i.e. have pair_role='request' with a valid paired_erd), and
writes controllable_erds.md with a formatted markdown table.

Includes all controllable domains: switch, select, number, button,
and binary_sensor with write operations.

Usage:
    python3 generate_controllable_erds.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR.parent / "appliance_api_erd_definitions.json"
OUTPUT_FILE = SCRIPT_DIR.parent / "doc" / "controllable_erds.md"

CONTROLLABLE_DOMAINS = ("switch", "select", "number", "button", "binary_sensor")


def clean_name(name: str) -> str:
    """Strip pair-role suffixes from display name."""
    n = name.strip()
    # Handle slash-separated suffixes: "Status/Actual", "Requested/Desired"
    n = re.sub(r"\s+-\s+(?:Status|Request|Requested|Desired|Actual|Setting|Current)/\w+$", "", n, flags=re.IGNORECASE)
    # Handle simple suffixes
    n = re.sub(r"\s+(?:Status|Request|Requested|Desired|Actual|Setting|Current)$", "", n, flags=re.IGNORECASE)
    return n.strip().rstrip("- ").strip()


def clean_description(desc: str) -> str:
    """Collapse newlines/whitespace and escape pipe characters for markdown tables."""
    cleaned = re.sub(r"\s*\n\s*", " ", desc.strip())
    cleaned = cleaned.replace("|", "\\|")
    return cleaned


def find_controllable_erds(erds: list) -> list[dict]:
    """
    Return list of controllable ERD info dicts.
    An ERD is controllable if:
    - Its ha_domain is in CONTROLLABLE_DOMAINS
    - It has 'write' in operations
    If it has pair_role='request' with a valid paired_erd, the status ERD is listed.
    """
    erd_by_id = {e["id"]: e for e in erds}
    rows = []

    for e in erds:
        if e.get("ha_domain") not in CONTROLLABLE_DOMAINS:
            continue
        if "write" not in e.get("operations", []):
            continue

        name = clean_name(e["name"])
        status_ids = ""

        # If paired, show the status ERD
        if e.get("pair_role") == "request":
            paired_id = e.get("paired_erd")
            if paired_id and paired_id in erd_by_id:
                status_ids = paired_id
        elif e.get("pair_role") == "status":
            # Status ERD that is also writable — show its paired request
            paired_id = e.get("paired_erd")
            if paired_id and paired_id in erd_by_id:
                status_ids = f"{paired_id} (paired request)"

        rows.append({
            "name": name,
            "request_id": e["id"],
            "status_ids": status_ids if status_ids else "—",
            "ha_domain": e.get("ha_domain", ""),
            "writable": "Yes",
            "description": clean_description(e.get("description", "")),
        })

    rows.sort(key=lambda r: int(r["request_id"], 16))
    return rows


def write_markdown(rows: list[dict], output_path: Path) -> None:
    """Write the controllable ERDs markdown table to output_path."""
    lines = [
        "# Controllable ERDs",
        "",
        "The following ERDs can be controlled because they have a paired Request and Status ERD.",
        "",
        "| Name | Request ERD | Status ERD(s) | HA Domain | Writable | Description |",
        "| ---- | ----------- | ------------- | --------- | -------- | ----------- |",
    ]

    for r in rows:
        lines.append(
            f"| {r['name']} | {r['request_id']} | {r['status_ids']} "
            f"| {r['ha_domain']} | {r['writable']} | {r['description']} |"
        )

    lines += [
        "",
        f"*Total: {len(rows)} controllable ERDs*",
        "",
    ]

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written {len(rows)} rows to {output_path}")


def main() -> None:
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    erds = data["erds"]
    rows = find_controllable_erds(erds)
    write_markdown(rows, OUTPUT_FILE)


if __name__ == "__main__":
    main()
