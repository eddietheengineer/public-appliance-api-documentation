# Scripts

All scripts operate on `../appliance_api_erd_definitions.json` in the repo root.
Run from this directory: `python3 <script>.py`

---

## Orchestrator

### `apply_all_suggestions.py`

Runs the full workflow: sync upstream, detect suggestions, apply to JSON, validate.

```
python3 apply_all_suggestions.py [--dry-run] [--no-sync]
```

- Syncs with upstream GE Appliances ERD definitions
- Runs all detection scripts and applies suggestions
- Runs all validators after applying changes
- Use `--dry-run` to preview changes, `--no-sync` to skip upstream sync

---

## Detection Scripts

These are imported by `apply_all_suggestions.py` but can also be run standalone to generate review reports in `../doc/`.

### `auto_assign_ha_metadata.py`

Suggests `ha_domain`, `device_class`, `unit_of_measurement`, and `state_class` for ERDs without HA metadata, based on data types and field name keywords.

### `auto_detect_pairings.py`

Finds unpaired ERDs with matching base names (e.g. `Foo Request` / `Foo Status`) and suggests `pair_role` and `paired_erd` metadata.

### `auto_detect_scaling.py`

Infers `scaling_factor` from field name patterns (e.g. `x 10`, `x 100`, `x 1000`).

---

## Maintenance Scripts

### `annotate_field_metadata.py`

For multi-field ERDs, detects per-field overrides of `ha_domain`, `device_class`, `unit_of_measurement`, `state_class`, and `scaling_factor` where individual fields differ from the parent ERD values.

**When to run:** After adding new multi-field ERDs with mixed field types.

### `clean_empty_device_class.py`

Removes `device_class: ""` entries from field definitions (the generator treats missing and empty the same).

**When to run:** After bulk metadata changes that leave empty device_class values.

### `review_field_changes.py`

Compares current ERD definitions against the base branch (`feat/add-validation-scripts`) and shows per-ERD field-level changes.

```
python3 review_field_changes.py              # review all changes
python3 review_field_changes.py --id 0x0005  # review a specific ERD
python3 review_field_changes.py --summary    # show aggregate statistics
```

**When to run:** After bulk changes to verify correctness.

### `sync_upstream.py`

Fetches the latest ERD definitions from upstream (`geappliances/public-appliance-api-documentation`) and diffs against the local file to identify new, modified, and removed ERDs.

```
python3 sync_upstream.py [--upstream OWNER/REPO] [--apply-suggestions]
```

**When to run:** Before syncing with upstream changes.

---

## Report Generators

### `generate_controllable_erds.py`

Lists all ERDs with `write` operations in controllable domains (`switch`, `select`, `number`, `button`, `binary_sensor`), showing paired status ERDs where applicable. Writes to `../doc/controllable_erds.md`.

### `generate_coverage_report.py`

Summarizes HA metadata completeness across all ERDs (domain distribution, metadata field coverage, confidence levels). Writes to `../doc/coverage_report.md`.

---

## Validators

These are called by `apply_all_suggestions.py` but can also be run standalone. Each exits with code 1 on failure.

### `validate_device_classes.py`

Validates that every `ha_domain`/`device_class` combination is valid for Home Assistant.

### `validate_ha_domain_rules.py`

Validates domain-specific rules (e.g. binary_sensor cannot have `unit_of_measurement`, sensor with `device_class=temperature` must have `unit_of_measurement`).

### `validate_ha_completeness.py`

Validates that ERDs with `ha_domain` have complete metadata (no missing `confidence` or `comment`, no contradictory unit hints in field names).

### `validate_pairings.py`

Validates that all `paired_erd` references are symmetric (if A points to B, B must point back to A).

### `validate_scaling_consistency.py`

Validates that `scaling_factor` values match field name patterns (e.g. field named `Temperature (°F x 10)` must have `scaling_factor: 10`).

### `validate_json_format.py`

Validates that `appliance_api_erd_definitions.json` follows the non-standard compact JSON format (valid JSON, no escaped non-ASCII, 2-space indentation, correct top-level structure).
