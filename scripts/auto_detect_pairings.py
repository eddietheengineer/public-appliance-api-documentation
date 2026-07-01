#!/usr/bin/env python3
"""
auto_detect_pairings.py

Find missing request/status pairs and suggest pairing metadata.
Outputs a markdown report with suggestions for human review.

Usage:
    python3 auto_detect_pairings.py
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import ERD_DEFINITIONS_FILE

SCRIPT_DIR = Path(__file__).parent
OUTPUT_FILE = SCRIPT_DIR.parent / "doc" / "pairing_suggestions.md"

SUFFIX_TO_ROLE = {
    "Request": "request",
    "Requested": "request",
    "Desired": "request",
    "Target": "request",
    "Configured": "request",
    "Status": "status",
    "Actual": "status",
    "Current": "status",
    "Setting": "status",
}

ROLE_SUFFIXES = {
    "request": ["Request", "Requested", "Desired", "Target", "Configured"],
    "status": ["Status", "Actual", "Current", "Setting"],
}


def extract_base_name(name: str) -> tuple[str, str] | None:
    # First try slash-separated suffixes: "Base - Status/Actual", "Base - Requested/Desired"
    m = re.search(r"^(.+?)\s+-\s+([A-Za-z]+)/([A-Za-z]+)$", name)
    if m:
        base = m.group(1).strip()
        suffix = m.group(2)  # use first part of slash pair
        if suffix in SUFFIX_TO_ROLE:
            return base, suffix

    for suffix in SUFFIX_TO_ROLE:
        if name.endswith(suffix):
            base = name[:-len(suffix)].strip()
            return base, suffix
    return None


def normalize_base(base: str) -> str:
    return re.sub(r"\s+", " ", base.strip().lower())


def generate_report(suggestions: list[dict]) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Pairing Suggestions",
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
            "| ERD A ID | ERD A Name | Role A | ERD B ID | ERD B Name | Role B | Reason |",
            "|----------|------------|--------|----------|------------|--------|--------|",
        ]

        for s in conf_suggestions:
            reason = s.get("reason", "").replace("|", "\\|")
            lines.append(
                f"| {s['erd_a_id']} | {s['erd_a_name']} | {s['role_a']} "
                f"| {s['erd_b_id']} | {s['erd_b_name']} | {s['role_b']} "
                f"| {reason} |"
            )

        lines.append("")

    lines += [
        "## Review Notes",
        "",
        "- **High confidence**: Exact base name match with one request and one status candidate",
        "- **Medium confidence**: Match found but multiple candidates share the same base name",
        "- **Low confidence**: Fuzzy or partial name match — needs manual verification",
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
    paired_ids = {e["id"] for e in erds if "pair_role" in e}
    unpaired = [e for e in erds if "pair_role" not in e]

    print(f"Total ERDs: {len(erds)}")
    print(f"Already paired: {len(paired_ids)}")
    print(f"Unpaired: {len(unpaired)}")

    candidates_by_base: dict[str, list[dict]] = {}
    for erd in unpaired:
        result = extract_base_name(erd["name"])
        if not result:
            continue
        base, suffix = result
        role = SUFFIX_TO_ROLE[suffix]
        norm = normalize_base(base)
        candidates_by_base.setdefault(norm, []).append({
            "id": erd["id"],
            "name": erd["name"],
            "base": base,
            "suffix": suffix,
            "role": role,
        })

    suggestions = []
    seen = set()

    for norm_base, group in candidates_by_base.items():
        requests = [c for c in group if c["role"] == "request"]
        statuses = [c for c in group if c["role"] == "status"]

        if not requests or not statuses:
            continue

        if len(requests) == 1 and len(statuses) == 1:
            req = requests[0]
            stat = statuses[0]
            pair_key = tuple(sorted([req["id"], stat["id"]]))
            if pair_key in seen:
                continue
            seen.add(pair_key)
            suggestions.append({
                "erd_a_id": req["id"],
                "erd_a_name": req["name"],
                "role_a": "request",
                "erd_b_id": stat["id"],
                "erd_b_name": stat["name"],
                "role_b": "status",
                "confidence": "high",
                "reason": f"Exact base name match: \"{req['base']}\"",
            })
        else:
            for req in requests:
                for stat in statuses:
                    pair_key = tuple(sorted([req["id"], stat["id"]]))
                    if pair_key in seen:
                        continue
                    seen.add(pair_key)
                    suggestions.append({
                        "erd_a_id": req["id"],
                        "erd_a_name": req["name"],
                        "role_a": "request",
                        "erd_b_id": stat["id"],
                        "erd_b_name": stat["name"],
                        "role_b": "status",
                        "confidence": "medium",
                        "reason": f"One of multiple candidates for base \"{req['base']}\"",
                    })

    suggestions.sort(key=lambda s: (
        {"high": 0, "medium": 1, "low": 2}.get(s["confidence"], 3),
        s["erd_a_id"],
    ))

    print(f"Generated {len(suggestions)} pairing suggestions")

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
