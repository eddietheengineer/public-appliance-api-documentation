#!/usr/bin/env python3
"""
apply_all_suggestions.py

Orchestrate the full workflow: sync upstream, detect suggestions, apply to JSON.

Usage:
    python3 apply_all_suggestions.py [--dry-run] [--no-sync]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import ERD_DEFINITIONS_FILE, VALID_DEVICE_CLASSES
from format_json import format_erd_json, save_erd_definitions, load_erd_definitions

# Import detection scripts
from auto_assign_ha_metadata import generate_suggestion as ha_suggestion, detect_button_device_class
from auto_detect_pairings import extract_base_name, normalize_base, SUFFIX_TO_ROLE
from auto_detect_scaling import extract_scaling_hint

SCRIPT_DIR = Path(__file__).parent


def run_sync() -> None:
    """Run upstream sync."""
    print("Running upstream sync...")
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "sync_upstream.py")],
        cwd=SCRIPT_DIR,
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"WARNING: Sync failed: {result.stderr}", file=sys.stderr)


def collect_ha_suggestions(erds: list[dict]) -> dict:
    """Collect HA metadata suggestions for all ERDs."""
    suggestions = {}
    for erd in erds:
        if not isinstance(erd, dict):
            continue
        if erd.get("ha_domain"):
            continue
        erd_id = erd.get("id")
        if not erd_id:
            continue
        suggestion = ha_suggestion(erd)
        if suggestion:
            suggestions[erd_id] = suggestion
    return suggestions


def collect_button_device_class_suggestions(erds: list[dict]) -> dict:
    """Add device_class to button ERDs that are missing it."""
    suggestions = {}
    for erd in erds:
        if not isinstance(erd, dict):
            continue
        if erd.get("ha_domain") != "button":
            continue
        if erd.get("device_class"):
            continue
        erd_id = erd.get("id")
        if not erd_id:
            continue
        erd_name = erd.get("name", "")
        dc = detect_button_device_class(erd_name)
        if dc and dc in VALID_DEVICE_CLASSES.get("button", set()):
            suggestions[erd_id] = {"device_class": dc}
    return suggestions


def collect_pairing_suggestions(erds: list[dict]) -> dict:
    """Collect pairing suggestions."""
    paired_ids = {e.get("id") for e in erds if isinstance(e, dict) and "pair_role" in e}
    unpaired = [e for e in erds if isinstance(e, dict) and "pair_role" not in e]

    candidates_by_base = {}
    for erd in unpaired:
        erd_id = erd.get("id")
        if not erd_id:
            continue
        result = extract_base_name(erd.get("name", ""))
        if not result:
            continue
        base, suffix = result
        role = SUFFIX_TO_ROLE[suffix]
        norm = normalize_base(base)
        candidates_by_base.setdefault(norm, []).append({
            "id": erd_id,
            "name": erd.get("name", ""),
            "base": base,
            "suffix": suffix,
            "role": role,
        })

    suggestions = {}
    for norm_base, group in candidates_by_base.items():
        requests = [c for c in group if c["role"] == "request"]
        statuses = [c for c in group if c["role"] == "status"]

        if len(requests) == 1 and len(statuses) == 1:
            req = requests[0]
            stat = statuses[0]
            suggestions[req["id"]] = {
                "pair_role": "request",
                "paired_erd": stat["id"],
            }
            suggestions[stat["id"]] = {
                "pair_role": "status",
                "paired_erd": req["id"],
            }

    return suggestions


def collect_scaling_suggestions(erds: list[dict]) -> dict:
    """Collect scaling factor suggestions."""
    suggestions = {}
    for erd in erds:
        if not isinstance(erd, dict):
            continue
        if "scaling_factor" in erd:
            continue
        erd_id = erd.get("id")
        if not erd_id:
            continue
        for field in erd.get("data", []):
            if not isinstance(field, dict):
                continue
            hint = extract_scaling_hint(field.get("name", ""))
            if hint is not None:
                suggestions[erd_id] = hint
                break
    return suggestions


def apply_suggestions(
    data: dict,
    ha_suggestions: dict,
    pairing_suggestions: dict,
    scaling_suggestions: dict,
    button_dc_suggestions: dict,
) -> dict:
    """Apply all suggestions to ERD data."""
    erds = data.get("erds", [])

    for erd in erds:
        if not isinstance(erd, dict):
            continue
        erd_id = erd.get("id")
        if not erd_id:
            continue

        # Apply HA metadata
        if erd_id in ha_suggestions:
            suggestion = ha_suggestions[erd_id]
            erd["ha_domain"] = suggestion["ha_domain"]
            if "device_class" in suggestion:
                erd["device_class"] = suggestion["device_class"]
            if "unit_of_measurement" in suggestion:
                erd["unit_of_measurement"] = suggestion["unit_of_measurement"]
            if "state_class" in suggestion:
                erd["state_class"] = suggestion["state_class"]
            erd["confidence"] = suggestion["confidence"]
            erd["comment"] = suggestion["comment"]

        # Apply pairings
        if erd_id in pairing_suggestions:
            pairing = pairing_suggestions[erd_id]
            erd["pair_role"] = pairing["pair_role"]
            erd["paired_erd"] = pairing["paired_erd"]

        # Apply scaling
        if erd_id in scaling_suggestions:
            erd["scaling_factor"] = scaling_suggestions[erd_id]

        # Apply button device classes
        if erd_id in button_dc_suggestions:
            dc_suggestion = button_dc_suggestions[erd_id]
            if "device_class" in dc_suggestion:
                erd["device_class"] = dc_suggestion["device_class"]

    return data


def run_validators() -> tuple[bool, list[str]]:
    """Run all validators and return (success, errors)."""
    validators = [
        "validate_json_format.py",
        "validate_device_classes.py",
        "validate_pairings.py",
        "validate_ha_completeness.py",
        "validate_scaling_consistency.py",
        "validate_ha_domain_rules.py",
    ]

    all_passed = True
    errors = []

    for validator in validators:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / validator)],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            all_passed = False
            output = result.stdout.strip()
            stderr = result.stderr.strip()
            msg = output if output else stderr
            errors.append(f"{validator}: {msg}")

    return all_passed, errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply all suggestions to ERD definitions")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying",
    )
    parser.add_argument(
        "--no-sync",
        action="store_true",
        help="Skip upstream sync step",
    )
    args = parser.parse_args()

    if not ERD_DEFINITIONS_FILE.exists():
        print(f"ERROR: {ERD_DEFINITIONS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    # Step 1: Sync (optional)
    if not args.no_sync:
        run_sync()

    # Step 2: Load data (reload after sync in case file changed)
    data = load_erd_definitions()
    erds = data.get("erds", [])

    if not erds:
        print("WARNING: No ERDs found in definitions file", file=sys.stderr)

    # Step 3: Collect suggestions
    print("Collecting suggestions...")
    ha_suggestions = collect_ha_suggestions(erds)
    pairing_suggestions = collect_pairing_suggestions(erds)
    scaling_suggestions = collect_scaling_suggestions(erds)
    button_dc_suggestions = collect_button_device_class_suggestions(erds)

    print(f"\nSuggestions collected:")
    print(f"  HA metadata: {len(ha_suggestions)}")
    print(f"  Pairings: {len(pairing_suggestions) // 2} pairs")
    print(f"  Scaling factors: {len(scaling_suggestions)}")
    print(f"  Button device classes: {len(button_dc_suggestions)}")

    if args.dry_run:
        print("\n[DRY RUN] No changes applied")
        return

    # Step 4: Apply suggestions
    print("\nApplying suggestions...")
    data = apply_suggestions(data, ha_suggestions, pairing_suggestions, scaling_suggestions, button_dc_suggestions)

    # Step 5: Save (atomic write via shared module)
    save_erd_definitions(data)
    print(f"Saved to {ERD_DEFINITIONS_FILE}")

    # Step 6: Validate
    print("\nRunning validators...")
    all_passed, errors = run_validators()

    if all_passed:
        print("All validators passed!")
    else:
        print("WARNING: Some validators failed:")
        for error in errors:
            print(f"  - {error}")

    # Step 7: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"HA metadata applied: {len(ha_suggestions)}")
    print(f"Pairings applied: {len(pairing_suggestions) // 2} pairs")
    print(f"Scaling factors applied: {len(scaling_suggestions)}")
    print(f"Button device classes applied: {len(button_dc_suggestions)}")
    print(f"Total changes: {len(ha_suggestions) + len(pairing_suggestions) + len(scaling_suggestions) + len(button_dc_suggestions)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
