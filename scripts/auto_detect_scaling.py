#!/usr/bin/env python3
"""
auto_detect_scaling.py

Infer scaling factors from field names.
Outputs a markdown report with suggestions for human review.

Usage:
    python3 auto_detect_scaling.py
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR.parent / "appliance_api_erd_definitions.json"
OUTPUT_FILE = SCRIPT_DIR / "scaling_suggestions.md"


def extract_scaling_hint(field_name: str) -> int | None:
    if re.search(r'0x[0-9a-fA-F]', field_name):
        return None

    if re.search(r'index\s+\d+', field_name, re.IGNORECASE):
        return None

    m = re.search(r'[°]?\s*[FCfc]x(\d+)', field_name)
    if m:
        return int(m.group(1))

    m = re.search(r'(?<=[\s(])[xX]\s*(\d+)', field_name)
    if m:
        val = int(m.group(1))
        if val > 1:
            return val

    m = re.search(
        r'(?:s|ns|ts|ms|us|oz|gal|ml|volts|amps|watts|fahrenheit|celsius|percent|degrees?)X(\d+)',
        field_name,
        re.IGNORECASE,
    )
    if m:
        val = int(m.group(1))
        if val > 1:
            return val

    return None


def generate_report(suggestions: list[dict]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Scaling Factor Suggestions",
        "",
        f"Generated: {timestamp}",
        "",
        f"**Total suggestions: {len(suggestions)}**",
        "",
    ]

    if not suggestions:
        lines += [
            "No ERDs with detectable scaling hints were found that are missing a `scaling_factor`.",
            "",
        ]
    else:
        lines += [
            "| ERD ID | Name | Suggested scaling_factor | Field Name |",
            "|--------|------|--------------------------|------------|",
        ]

        for s in suggestions:
            field_name = s["field_name"].replace("|", "\\|")
            lines.append(
                f"| {s['erd_id']} | {s['name']} "
                f"| {s['suggested_factor']} | {field_name} |"
            )

        lines.append("")

    lines += [
        "## Review Notes",
        "",
        "- Scaling factors are inferred from field name patterns like `x 100`, `Fx10`, `GallonsX100`",
        "- Only ERDs **missing** a `scaling_factor` are included",
        "- All suggestions should be reviewed before applying to the JSON file",
        "- Use surgical text edits per AGENTS.md rules when applying suggestions",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)

    erds = data["erds"]
    unscaled = [e for e in erds if "scaling_factor" not in e]

    print(f"Total ERDs: {len(erds)}")
    print(f"Already scaled: {len(erds) - len(unscaled)}")
    print(f"Unscaled: {len(unscaled)}")

    suggestions = []
    for erd in unscaled:
        for field in erd.get("data", []):
            hint = extract_scaling_hint(field.get("name", ""))
            if hint is not None:
                suggestions.append({
                    "erd_id": erd["id"],
                    "name": erd["name"],
                    "suggested_factor": hint,
                    "field_name": field["name"],
                })
                break

    print(f"Generated {len(suggestions)} scaling suggestions")

    report = generate_report(suggestions)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(f"Written suggestions to {OUTPUT_FILE}")

    github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with open(github_step_summary, "a", encoding="utf-8") as f:
            f.write(report)
        print("Written suggestions to GitHub Step Summary")


if __name__ == "__main__":
    main()
