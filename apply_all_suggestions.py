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

SCRIPT_DIR = Path(__file__).parent
ERD_DEFINITIONS_FILE = SCRIPT_DIR / "appliance_api_erd_definitions.json"

# Import detection scripts
from auto_assign_ha_metadata import generate_suggestion as ha_suggestion
from auto_detect_pairings import extract_base_name, normalize_base
from auto_detect_scaling import extract_scaling_hint


def load_erd_definitions() -> dict:
    with ERD_DEFINITIONS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def save_erd_definitions(data: dict) -> None:
    """Save ERD definitions with custom formatting per AGENTS.md rules."""
    formatted = format_erd_json(data)
    with ERD_DEFINITIONS_FILE.open("w", encoding="utf-8") as f:
        f.write(formatted)


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
        if erd.get("ha_domain"):
            continue
        suggestion = ha_suggestion(erd)
        if suggestion:
            suggestions[erd["id"]] = suggestion
    return suggestions


def collect_pairing_suggestions(erds: list[dict]) -> dict:
    """Collect pairing suggestions."""
    paired_ids = {e["id"] for e in erds if "pair_role" in e}
    unpaired = [e for e in erds if "pair_role" not in e]
    
    candidates_by_base = {}
    for erd in unpaired:
        result = extract_base_name(erd["name"])
        if not result:
            continue
        base, suffix = result
        from auto_detect_pairings import SUFFIX_TO_ROLE
        role = SUFFIX_TO_ROLE[suffix]
        norm = normalize_base(base)
        candidates_by_base.setdefault(norm, []).append({
            "id": erd["id"],
            "name": erd["name"],
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
        if "scaling_factor" in erd:
            continue
        for field in erd.get("data", []):
            hint = extract_scaling_hint(field.get("name", ""))
            if hint is not None:
                suggestions[erd["id"]] = hint
                break
    return suggestions


def apply_suggestions(
    data: dict,
    ha_suggestions: dict,
    pairing_suggestions: dict,
    scaling_suggestions: dict,
) -> dict:
    """Apply all suggestions to ERD data."""
    erds = data["erds"]
    
    for erd in erds:
        erd_id = erd["id"]
        
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
    
    return data


def run_validators() -> tuple[bool, list[str]]:
    """Run all validators and return (success, errors)."""
    validators = [
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
            errors.append(f"{validator}: {result.stdout.strip()}")
    
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
    
    # Step 2: Load data
    data = load_erd_definitions()
    erds = data["erds"]
    
    # Step 3: Collect suggestions
    print("Collecting suggestions...")
    ha_suggestions = collect_ha_suggestions(erds)
    pairing_suggestions = collect_pairing_suggestions(erds)
    scaling_suggestions = collect_scaling_suggestions(erds)
    
    print(f"\nSuggestions collected:")
    print(f"  HA metadata: {len(ha_suggestions)}")
    print(f"  Pairings: {len(pairing_suggestions) // 2} pairs")
    print(f"  Scaling factors: {len(scaling_suggestions)}")
    
    if args.dry_run:
        print("\n[DRY RUN] No changes applied")
        return
    
    # Step 4: Apply suggestions
    print("\nApplying suggestions...")
    data = apply_suggestions(data, ha_suggestions, pairing_suggestions, scaling_suggestions)
    
    # Step 5: Save
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
    print(f"Total changes: {len(ha_suggestions) + len(pairing_suggestions) + len(scaling_suggestions)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
