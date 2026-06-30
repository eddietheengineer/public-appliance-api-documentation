# Future Improvements

This document outlines proposed scripts and enhancements that have not yet been implemented for the public-appliance-api-documentation repository.

## Auto-generation Scripts (High Priority)

### `auto_assign_ha_metadata.py` ✅ Implemented
Suggest Home Assistant metadata for unmapped ERDs based on data types and field names.

**Features:**
- Infer `ha_domain` from data type:
  - `enum` → `sensor` or `select` (if writable)
  - `bool` → `binary_sensor`
  - Numeric types (u8, u16, u32, i8, i16, i32) → `sensor`
- Suggest `device_class` based on field name keywords:
  - "temperature", "temp" → `temperature`
  - "voltage" → `voltage`
  - "current", "amps" → `current`
  - "power", "watts" → `power`
  - "humidity" → `humidity`
- Suggest `unit_of_measurement` from field name patterns:
  - `(volts)` → "V"
  - `(amps)` → "A"
  - `(watts)` → "W"
  - `(degF)`, `(fahrenheit)` → "°F"
  - `(degC)`, `(celsius)` → "°C"
- Output a report of suggestions that can be reviewed and applied

### `auto_detect_pairings.py`
Find missing request/status pairs and suggest pairing metadata.

**Features:**
- Scan for ERDs with matching base names ending in "Request"/"Status"
- Flag unpaired ERDs that should have pairs
- Suggest `paired_erd` and `pair_role` values
- Output report for review

### `auto_detect_scaling.py`
Infer scaling factors from field names.

**Features:**
- Parse field names for patterns like "x 100", "x 10", "Volts x 100"
- Suggest `scaling_factor` values for ERDs missing them
- Output report for review

## Upstream Sync Script (Medium Priority)

### `sync_upstream.py`
Merge changes from the upstream GE Appliances repository.

**Features:**
- Fetch latest `appliance_api_erd_definitions.json` from upstream (geappliances/public-appliance-api-documentation)
- Diff against current file to identify:
  - New ERDs added upstream (need HA metadata)
  - ERDs modified upstream (check if HA metadata still valid)
  - ERDs removed upstream (flag for review)
- Generate a report of changes needing attention
- Optionally auto-apply HA metadata heuristics to new ERDs

## Reporting Scripts (Medium Priority)

### `generate_ha_discovery_preview.py`
Preview what Home Assistant MQTT discovery would generate.

**Features:**
- Run a simplified version of the downstream `generate_ha_discovery.py` logic
- Show what entities would be created for each ERD
- Help validate metadata before committing
- Output as markdown table or JSON

## Interactive Tool (Low Priority)

### `erd_metadata_wizard.py`
Interactive CLI for adding metadata to ERDs.

**Features:**
- Step through ERDs missing metadata
- Show field data and suggest values
- Allow user to accept/reject/modify suggestions
- Write changes back to JSON (preserving format per AGENTS.md rules)

## Implementation Notes

- All auto-generation scripts should output reports for human review before applying changes
- Follow the compact JSON formatting rules documented in AGENTS.md
- Use surgical text edits when possible to preserve formatting
- Integrate with existing validation scripts to ensure generated metadata passes all checks
