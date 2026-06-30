#!/usr/bin/env python3
"""
generate_controllable_erds.py

Reads appliance_api_erd_definitions.json, identifies ERDs that can be
controlled (i.e. Request ERDs that have a paired Status ERD), and writes
controllable_erds.md with a formatted markdown table.

Usage:
    python3 generate_controllable_erds.py
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR.parent / "appliance_api_erd_definitions.json"
OUTPUT_FILE = SCRIPT_DIR / "controllable_erds.md"

CONTROLLABLE_DOMAINS = ("switch", "select", "number", "button")


def base_name(name: str) -> str:
    """Strip trailing 'Status' or 'Request' suffix and normalize."""
    n = name.strip()
    n = re.sub(r"\s+Status$", "", n, flags=re.IGNORECASE)
    n = re.sub(r"\s+Request$", "", n, flags=re.IGNORECASE)
    return n.lower().strip()


def clean_description(desc: str) -> str:
    """Collapse newlines/whitespace and escape pipe characters for markdown tables."""
    # Replace newlines and extra whitespace with a single space
    cleaned = re.sub(r"\s*\n\s*", " ", desc.strip())
    # Escape pipe characters so they don't break the table
    cleaned = cleaned.replace("|", "\\|")
    return cleaned


def find_paired_request_ids(erds: list) -> dict:
    """
    Return a mapping of request ERD id -> list of paired status ERD ids.
    A pair is defined as ERDs whose names share the same base and end with
    'Request' and 'Status' respectively.
    """
    by_base: dict[str, list] = {}
    for e in erds:
        b = base_name(e["name"])
        by_base.setdefault(b, []).append(e)

    paired: dict[str, list[str]] = {}
    for group in by_base.values():
        request_erds = [e for e in group if e["name"].lower().endswith("request")]
        status_erds = [e for e in group if e["name"].lower().endswith("status")]
        if request_erds and status_erds:
            for req in request_erds:
                paired[req["id"]] = [s["id"] for s in status_erds]

    return paired


def build_rows(erds: list, paired: dict) -> list[dict]:
    """Build table row data for all controllable (paired Request) ERDs."""
    rows = []
    for e in erds:
        if e.get("ha_domain") in CONTROLLABLE_DOMAINS and e["id"] in paired:
            status_ids = ", ".join(paired[e["id"]])
            name = re.sub(r"\s+Request$", "", e["name"], flags=re.IGNORECASE)
            rows.append(
                {
                    "name": name,
                    "request_id": e["id"],
                    "status_ids": status_ids,
                    "ha_domain": e.get("ha_domain", ""),
                    "writable": "Yes" if "write" in e.get("operations", []) else "No",
                    "description": clean_description(e.get("description", "")),
                }
            )

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
    paired = find_paired_request_ids(erds)
    rows = build_rows(erds, paired)
    write_markdown(rows, OUTPUT_FILE)


if __name__ == "__main__":
    main()
