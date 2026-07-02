# Future Improvements

This document outlines proposed scripts and enhancements that have not yet been implemented for the public-appliance-api-documentation repository.

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
