#!/usr/bin/env python3
"""
sync_upstream.py

Fetch the latest ERD definitions from the upstream repository and diff
against the local file to identify new, modified, and removed ERDs.

Usage:
    python3 sync_upstream.py [--upstream OWNER/REPO] [--apply-suggestions]
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR.parent / "appliance_api_erd_definitions.json"
OUTPUT_FILE = SCRIPT_DIR.parent / "doc" / "sync_report.md"

DEFAULT_UPSTREAM = "geappliances/public-appliance-api-documentation"
UPSTREAM_FILE = "appliance_api_erd_definitions.json"

HA_METADATA_FIELDS = {
    "ha_domain",
    "device_class",
    "confidence",
    "comment",
    "unit_of_measurement",
    "state_class",
    "scaling_factor",
    "pair_role",
    "paired_erd",
}


def fetch_upstream(upstream_repo: str) -> dict:
    url = f"https://raw.githubusercontent.com/{upstream_repo}/main/{UPSTREAM_FILE}"
    print(f"Fetching upstream from {url}")
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"ERROR: Failed to fetch upstream ({e.code}: {e.reason})", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: Failed to connect to upstream ({e.reason})", file=sys.stderr)
        sys.exit(1)


def load_local() -> dict:
    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def strip_ha_metadata(erd: dict) -> dict:
    return {k: v for k, v in erd.items() if k not in HA_METADATA_FIELDS}


def diff_erds(local_data: dict, upstream_data: dict) -> tuple[list, list, list]:
    local_map = {e["id"]: e for e in local_data.get("erds", [])}
    upstream_map = {e["id"]: e for e in upstream_data.get("erds", [])}

    local_ids = set(local_map.keys())
    upstream_ids = set(upstream_map.keys())

    new_ids = sorted(upstream_ids - local_ids)
    removed_ids = sorted(local_ids - upstream_ids)
    common_ids = sorted(local_ids & upstream_ids)

    new_erds = [upstream_map[eid] for eid in new_ids]
    removed_erds = [local_map[eid] for eid in removed_ids]

    modified_erds = []
    for eid in common_ids:
        local_core = strip_ha_metadata(local_map[eid])
        upstream_core = strip_ha_metadata(upstream_map[eid])
        if local_core != upstream_core:
            modified_erds.append({
                "id": eid,
                "local": local_map[eid],
                "upstream": upstream_map[eid],
            })

    return new_erds, modified_erds, removed_erds


def generate_field_diff(local_erd: dict, upstream_erd: dict) -> list[str]:
    diffs = []
    local_core = strip_ha_metadata(local_erd)
    upstream_core = strip_ha_metadata(upstream_erd)

    all_keys = sorted(set(list(local_core.keys()) + list(upstream_core.keys())))
    for key in all_keys:
        local_val = local_core.get(key)
        upstream_val = upstream_core.get(key)
        if local_val != upstream_val:
            if local_val is None:
                diffs.append(f"  - Added field `{key}`")
            elif upstream_val is None:
                diffs.append(f"  - Removed field `{key}`")
            else:
                diffs.append(f"  - Changed field `{key}`")
    return diffs


def generate_report(
    new_erds: list,
    modified_erds: list,
    removed_erds: list,
    suggestions: list[dict] | None = None,
    upstream_repo: str = DEFAULT_UPSTREAM,
) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = [
        "# Upstream Sync Report",
        "",
        f"Generated: {timestamp}",
        f"Upstream: `{upstream_repo}`",
        "",
        "## Summary",
        "",
        f"| Category | Count |",
        f"|----------|-------|",
        f"| New ERDs | {len(new_erds)} |",
        f"| Modified ERDs | {len(modified_erds)} |",
        f"| Removed ERDs | {len(removed_erds)} |",
        "",
    ]

    if new_erds:
        lines += [
            "## New ERDs (need HA metadata)",
            "",
            "| ERD ID | Name | Operations |",
            "|--------|------|------------|",
        ]
        for erd in new_erds:
            ops = ", ".join(erd.get("operations", []))
            name = erd.get("name", "<unknown>").replace("|", "\\|")
            lines.append(f"| {erd['id']} | {name} | {ops} |")
        lines.append("")

        if suggestions:
            lines += [
                "### Auto-suggested HA Metadata for New ERDs",
                "",
                "| ERD ID | Name | ha_domain | device_class | unit | confidence |",
                "|--------|------|-----------|--------------|------|------------|",
            ]
            for s in suggestions:
                name = s.get("name", "").replace("|", "\\|")
                device_class = s.get("device_class", "")
                unit = s.get("unit_of_measurement", "")
                lines.append(
                    f"| {s['erd_id']} | {name} | {s['ha_domain']} "
                    f"| {device_class} | {unit} | {s['confidence']} |"
                )
            lines.append("")

    if modified_erds:
        lines += [
            "## Modified ERDs (review HA metadata)",
            "",
        ]
        for entry in modified_erds:
            erd_id = entry["id"]
            name = entry["upstream"].get("name", "<unknown>")
            diffs = generate_field_diff(entry["local"], entry["upstream"])
            lines.append(f"### {erd_id} — {name}")
            lines.append("")
            for d in diffs:
                lines.append(d)
            lines.append("")

    if removed_erds:
        lines += [
            "## Removed ERDs (flag for review)",
            "",
            "| ERD ID | Name |",
            "|--------|------|",
        ]
        for erd in removed_erds:
            name = erd.get("name", "<unknown>").replace("|", "\\|")
            lines.append(f"| {erd['id']} | {name} |")
        lines.append("")

    if not new_erds and not modified_erds and not removed_erds:
        lines += [
            "No differences found. Local file is in sync with upstream.",
            "",
        ]

    lines += [
        "## Review Notes",
        "",
        "- **New ERDs**: Need HA metadata (`ha_domain`, `device_class`, etc.) added",
        "- **Modified ERDs**: Core data changed — verify existing HA metadata is still valid",
        "- **Removed ERDs**: No longer in upstream — consider removing local HA metadata",
        "- Use surgical text edits per AGENTS.md rules when applying changes",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync ERD definitions from upstream")
    parser.add_argument(
        "--upstream",
        default=os.environ.get("UPSTREAM_REPO", DEFAULT_UPSTREAM),
        help=f"Upstream repo as OWNER/REPO (default: {DEFAULT_UPSTREAM})",
    )
    parser.add_argument(
        "--apply-suggestions",
        action="store_true",
        help="Auto-generate HA metadata suggestions for new ERDs",
    )
    args = parser.parse_args()

    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    upstream_data = fetch_upstream(args.upstream)
    local_data = load_local()

    new_erds, modified_erds, removed_erds = diff_erds(local_data, upstream_data)

    print(f"New ERDs: {len(new_erds)}")
    print(f"Modified ERDs: {len(modified_erds)}")
    print(f"Removed ERDs: {len(removed_erds)}")

    suggestions = None
    if args.apply_suggestions and new_erds:
        try:
            from auto_assign_ha_metadata import generate_suggestion
            suggestions = []
            for erd in new_erds:
                suggestion = generate_suggestion(erd)
                if suggestion:
                    suggestions.append(suggestion)
            print(f"Generated {len(suggestions)} HA metadata suggestions for new ERDs")
        except ImportError:
            print("WARNING: Could not import auto_assign_ha_metadata for suggestions")

    report = generate_report(
        new_erds, modified_erds, removed_erds, suggestions, args.upstream
    )
    print(report)

    github_step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_step_summary:
        with open(github_step_summary, "a", encoding="utf-8") as f:
            f.write(report)
        print("Written report to GitHub Step Summary")

    if new_erds or modified_erds or removed_erds:
        sys.exit(0)


if __name__ == "__main__":
    main()
