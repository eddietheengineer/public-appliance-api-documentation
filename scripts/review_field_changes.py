#!/usr/bin/env python3
"""
Review per-field HA metadata changes between two versions of the ERD definitions.

Compares the JSON from the base branch (feat/add-validation-scripts) against
the current working tree, producing a compact per-ERD summary of what changed.

Usage:
    python3 review_field_changes.py              # review all changes
    python3 review_field_changes.py --id 0x0005  # review a specific ERD
    python3 review_field_changes.py --summary    # show aggregate statistics
    python3 review_field_changes.py --ids        # list all changed ERD IDs
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import argparse
import json
import subprocess
from ha_constants import ERD_DEFINITIONS_FILE

SCRIPT_DIR = Path(__file__).parent
METADATA_KEYS = {"ha_domain", "device_class", "unit_of_measurement", "state_class", "scaling_factor"}


def load_json(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: Failed to load {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def load_base_json() -> dict:
    """Load the base version from git (feat/add-validation-scripts branch)."""
    result = subprocess.run(
        ["git", "show", "feat/add-validation-scripts:appliance_api_erd_definitions.json"],
        capture_output=True, text=True, cwd=str(SCRIPT_DIR.parent),
    )
    if result.returncode != 0:
        print(f"ERROR: Could not load base JSON from git:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        print(f"ERROR: Failed to parse base JSON from git: {exc}", file=sys.stderr)
        sys.exit(1)


def erds_by_id(data: dict) -> dict:
    return {e["id"]: e for e in data.get("erds", []) if isinstance(e, dict)}


def diff_field(old: dict, new: dict) -> list:
    """Return list of (key, old_val, new_val) for changed metadata fields."""
    changes = []
    for key in METADATA_KEYS:
        old_val = old.get(key)
        new_val = new.get(key)
        if old_val != new_val:
            changes.append((key, old_val, new_val))
    return changes


def diff_erd(old_erd: dict, new_erd: dict) -> list:
    """Compare two ERDs field-by-field. Returns list of (field_name, changes)."""
    old_fields = {f["name"]: f for f in old_erd.get("data", []) if isinstance(f, dict)}
    new_fields = {f["name"]: f for f in new_erd.get("data", []) if isinstance(f, dict)}

    results = []
    all_names = sorted(set(list(old_fields.keys()) + list(new_fields.keys())))

    for name in all_names:
        old_f = old_fields.get(name)
        new_f = new_fields.get(name)

        if old_f is None:
            results.append((name, [("added", None, new_f)]))
            continue
        if new_f is None:
            results.append((name, [("removed", old_f, None)]))
            continue

        changes = diff_field(old_f, new_f)
        if changes:
            results.append((name, changes))

    return results


def format_value(val) -> str:
    if val is None:
        return "<none>"
    if isinstance(val, str):
        return f'"{val}"'
    return str(val)


def review_all(base_data: dict, new_data: dict) -> None:
    base_erds = erds_by_id(base_data)
    new_erds = erds_by_id(new_data)

    changed_erds = []
    for erd_id, new_erd in sorted(new_erds.items(), key=lambda x: x[0]):
        old_erd = base_erds.get(erd_id)
        if not old_erd:
            changed_erds.append((erd_id, new_erd, None, [("NEW ERD", None, new_erd)]))
            continue

        field_diffs = diff_erd(old_erd, new_erd)
        if field_diffs:
            changed_erds.append((erd_id, new_erd, old_erd, field_diffs))

    total_fields_changed = sum(len(diffs) for _, _, _, diffs in changed_erds)

    print(f"Changed ERDs: {len(changed_erds)}")
    print(f"Total field changes: {total_fields_changed}")
    print()

    for erd_id, new_erd, old_erd, field_diffs in changed_erds:
        name = new_erd.get("name", "<unknown>")
        print(f"{'=' * 72}")
        print(f"  {erd_id}  {name}")
        ha_domain = new_erd.get("ha_domain", "")
        if ha_domain:
            print(f"  domain={ha_domain}  device_class={new_erd.get('device_class', '')}  "
                  f"unit={new_erd.get('unit_of_measurement', '')}  state_class={new_erd.get('state_class', '')}")

        for field_name, changes in field_diffs:
            print(f"  └─ {field_name}")
            for change in changes:
                if len(change) == 3:
                    key, old_val, new_val = change
                    if key == "added":
                        print(f"     + added: {new_val}")
                    elif key == "removed":
                        print(f"     - removed: {old_val}")
                    else:
                        print(f"     {key}: {format_value(old_val)} -> {format_value(new_val)}")
                else:
                    print(f"     {change}")
        print()


def review_one(base_data: dict, new_data: dict, erd_id: str) -> None:
    base_erds = erds_by_id(base_data)
    new_erds = erds_by_id(new_data)

    new_erd = new_erds.get(erd_id)
    old_erd = base_erds.get(erd_id)

    if not new_erd:
        print(f"ERD {erd_id} not found in current data")
        return

    name = new_erd.get("name", "<unknown>")
    print(f"{'=' * 72}")
    print(f"  {erd_id}  {name}")
    ha_domain = new_erd.get("ha_domain", "")
    if ha_domain:
        print(f"  domain={ha_domain}  device_class={new_erd.get('device_class', '')}  "
              f"unit={new_erd.get('unit_of_measurement', '')}  state_class={new_erd.get('state_class', '')}")

    if old_erd:
        field_diffs = diff_erd(old_erd, new_erd)
        if field_diffs:
            for field_name, changes in field_diffs:
                print(f"  └─ {field_name}")
                for change in changes:
                    if len(change) == 3:
                        key, old_val, new_val = change
                        if key == "added":
                            print(f"     + added: {new_val}")
                        elif key == "removed":
                            print(f"     - removed: {old_val}")
                        else:
                            print(f"     {key}: {format_value(old_val)} -> {format_value(new_val)}")
                    else:
                        print(f"     {change}")
        else:
            print("  (no field-level changes)")
    else:
        print("  (NEW ERD)")
    print()


def show_summary(base_data: dict, new_data: dict) -> None:
    base_erds = erds_by_id(base_data)
    new_erds = erds_by_id(new_data)

    counts = {k: 0 for k in METADATA_KEYS}
    changed_erds = 0
    total_field_changes = 0

    for erd_id, new_erd in new_erds.items():
        old_erd = base_erds.get(erd_id)
        if not old_erd:
            continue

        field_diffs = diff_erd(old_erd, new_erd)
        if field_diffs:
            changed_erds += 1
            total_field_changes += len(field_diffs)
            for _, changes in field_diffs:
                for change in changes:
                    if len(change) == 3 and change[0] in counts:
                        counts[change[0]] += 1

    print(f"ERDs with field-level changes: {changed_erds}")
    print(f"Total field changes: {total_field_changes}")
    print()
    for key in METADATA_KEYS:
        print(f"  {key}: {counts[key]}")
    print()

    # Show top changed ERDs by number of field changes
    top_erds = []
    for erd_id, new_erd in new_erds.items():
        old_erd = base_erds.get(erd_id)
        if not old_erd:
            continue
        field_diffs = diff_erd(old_erd, new_erd)
        if field_diffs:
            top_erds.append((erd_id, new_erd.get("name", ""), len(field_diffs)))

    top_erds.sort(key=lambda x: -x[2])
    print("Top 20 ERDs by number of field changes:")
    for erd_id, name, n in top_erds[:20]:
        print(f"  {erd_id}  {n:3d} fields  {name}")


def list_ids(base_data: dict, new_data: dict) -> None:
    base_erds = erds_by_id(base_data)
    new_erds = erds_by_id(new_data)

    for erd_id, new_erd in sorted(new_erds.items(), key=lambda x: x[0]):
        old_erd = base_erds.get(erd_id)
        if not old_erd:
            print(erd_id)
            continue
        field_diffs = diff_erd(old_erd, new_erd)
        if field_diffs:
            print(erd_id)


def main():
    parser = argparse.ArgumentParser(description="Review per-field HA metadata changes")
    parser.add_argument("--id", help="Review a specific ERD by ID (e.g. 0x0005)")
    parser.add_argument("--summary", action="store_true", help="Show aggregate statistics")
    parser.add_argument("--ids", action="store_true", help="List all changed ERD IDs")
    args = parser.parse_args()

    print("Loading base JSON from git...", file=sys.stderr)
    base_data = load_base_json()
    print(f"  Base: {len(base_data.get('erds', []))} ERDs", file=sys.stderr)

    print("Loading current JSON...", file=sys.stderr)
    new_data = load_json(ERD_DEFINITIONS_FILE)
    print(f"  Current: {len(new_data.get('erds', []))} ERDs", file=sys.stderr)

    if args.id:
        review_one(base_data, new_data, args.id)
    elif args.summary:
        show_summary(base_data, new_data)
    elif args.ids:
        list_ids(base_data, new_data)
    else:
        review_all(base_data, new_data)


if __name__ == "__main__":
    main()
