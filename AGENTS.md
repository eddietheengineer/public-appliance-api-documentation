# Repository Constraints

## `appliance_api_erd_definitions.json`

This file uses a **non-standard compact JSON format**. Standard `json.dumps(indent=2)` will break it. Any modification must preserve the exact formatting rules below.

### Formatting Rules

**Indentation**: 2-space indent per nesting level.

**Primitive arrays** (all elements are strings, numbers, booleans, or null): single line.

```json
"operations": ["read", "publish", "subscribe"],
```

**Object arrays** (elements are objects): opening `[` and first `{` on the same line as the key; sibling objects separated by `}, {` on one line; closing `]` on the same line as the last `}`.

```json
    "data": [{
      "name": "Instantaneous Power",
      "type": "u16",
      "offset": 0,
      "size": 2
    }, {
      "name": "Watt Seconds Since Clear",
      "type": "u32",
      "offset": 2,
      "size": 4
    }],
```

**Objects**: opening `{` on its own line (or on the same line as `[` for array elements); closing `}` on its own line at the parent's indent level.

```json
    "updateClass": {
      "type": "legacy"
    },
```

**ERD objects in the `erds` array**: each ERD is at indent level 2 (4 spaces). Sibling ERDs are separated by `}, {` at indent level 1 (2 spaces).

```json
  "erds": [{
    "name": "Model Number",
    "id": "0x0001",
    ...
    "confidence": "high"
  }, {
    "name": "Serial Number",
    ...
  }]
```

**Trailing commas**: every field except the last in an object has a trailing comma. The last field has no comma.

**Unicode**: non-ASCII characters (e.g. `°F`) must be written as literal UTF-8, **not** escaped (no `\u00b0`). Use `ensure_ascii=False` if using `json.dumps`.

### How to Safely Modify

**Never** use `json.dumps()` with standard formatting — it will reformat the entire file.

**Option A — Surgical text edits** (recommended for adding/removing individual fields):

1. Find the ERD by its `"id"` field.
2. Find the last top-level field of that ERD (indent = 4 spaces, a `"key": value` line).
3. Add a trailing comma to that line if it doesn't have one.
4. Insert the new field(s) on the next line(s) at the same indent (4 spaces), each with a trailing comma.
5. Ensure the file still parses as valid JSON.

**Option B — Full reformat** (if making many changes):

1. Parse the file with `json.load()`.
2. Make all changes in memory.
3. Re-serialize using a custom formatter that follows the rules above.
4. Verify semantic correctness by comparing field values against the source of truth.

**Validation**: after any change, run `python3 -c "import json; json.load(open('appliance_api_erd_definitions.json'))"` to confirm valid JSON.

### Workflow

The CI workflow `.github/workflows/validate-device-classes.yml` runs `validate_device_classes.py` to check that `device_class` values are valid for each ERD's data types. Run this before committing.

# Project Context

## What This Repo Is

This repository documents the **GE Appliances Public Appliance API** — a binary protocol used by GE smart home appliances for local network communication. The API uses **ERDs** (Entity Record Definitions) to define every readable/writable parameter an appliance exposes.

The primary data file is `appliance_api_erd_definitions.json` — a single JSON file containing ~2,200 ERD definitions across all appliance categories. Each ERD specifies:
- `id`: hex identifier (e.g. `"0x0001"`)
- `name`, `description`: human-readable metadata
- `data`: array of fields with `type` (u8/u16/u32/i8/i16/i32/enum/string/bool), `offset`, `size`, and optional `values`/`bits`
- `ha_domain`: the Home Assistant entity domain this ERD maps to (`sensor`, `binary_sensor`, `switch`, `select`, `number`, `button`)
- `device_class`, `unit_of_measurement`, `scaling_factor`, `state_class`: HA entity metadata
- `paired_erd`/`pair_role`: request/status pairing for controllable entities

## Home Assistant MQTT Discovery Pipeline

The repo generates **Home Assistant MQTT discovery JSONL files** from the ERD definitions. This is the bridge between the appliance API documentation and the ESPHome Home Assistant bridge that actually controls appliances.

### Script: `generate_ha_discovery.py`

Copied from [eddietheengineer/home-assistant-bridge-esphome](https://github.com/eddietheengineer/home-assistant-bridge-esphome/blob/develop/scripts/generate_ha_discovery.py). Run it to regenerate the JSONL files:

```bash
python3 generate_ha_discovery.py --erd-definitions appliance_api_erd_definitions.json
```

**What it does:**
1. Reads `appliance_api_erd_definitions.json` (2,199 ERDs)
2. Filters out 2,596 derived entities matching internal metadata patterns (diagnostics, commissioning, firmware hashes, service mode, etc.) via regex on entity names
3. Classifies each ERD's data structure: `single`, `byte_offset`, `bitfield`, `mixed`, `version`, or `multi_board_version`
4. Generates Jinja2 `value_template` and `command_template` strings for each HA entity
5. Outputs category-specific JSONL files into `ha_discovery/`

### Output: `ha_discovery/*.jsonl`

10 JSONL files, **7,577 entities total** (after filtering), organized by appliance category:

| File | Entities | Category Range |
|---|---|---|
| `range.jsonl` | 2,619 | 0x5000–0x5FFF |
| `laundry.jsonl` | 1,753 | 0x2000–0x2FFF |
| `refrigeration.jsonl` | 1,863 | 0x1000–0x1FFF |
| `smallappliance.jsonl` | 693 | 0x9000–0x9FFF |
| `airconditioning.jsonl` | 282 | 0x7000–0x7FFF |
| `dishwasher.jsonl` | 236 | 0x3000–0x3FFF |
| `waterheater.jsonl` | 58 | 0x4000–0x4FFF |
| `common.jsonl` | 28 | 0x0000–0x0FFF |
| `energy.jsonl` | 37 | 0xD000–0xDFFF |
| `waterfilter.jsonl` | 8 | 0x8000–0x8FFF |

### JSONL Line Format (per entity)

Each line is a compact JSON object consumed by the ESPHome bridge's MQTT discovery system:

| Key | Meaning | Example |
|---|---|---|
| `i` | ERD ID as hex string | `"0001"` |
| `n` | Entity name | `"Model Number"` |
| `d` | HA domain | `sensor`, `binary_sensor`, `switch`, `select`, `number`, `button` |
| `ds` | ERD data size in bytes | `32` |
| `vt` | Jinja2 `value_template` — decodes hex MQTT payload → HA value | `{{ {'01': 'UI Locked'}.get(value[:2], 'Unknown') }}` |
| `ct` | Jinja2 `command_template` — encodes HA value → hex for MQTT write | `{{ {'Disabled': '00', 'SteamRefresh': '01'}[value] }}` |
| `u` | Unit of measurement | `"min"`, `"V"`, `"°F"` |
| `dc` | HA device_class | `"enum"`, `"voltage"`, `"restart"`, `"duration"` |
| `sc` | HA state_class | `"measurement"`, `"total"` |
| `sf` | Scaling factor | `100` |
| `p` | Paired ERD ID (for request/status pairs) | `"208d"` |
| `r` | Role: `"request"` or `"status"` | `"status"` |
| `o` | Options array (for `select` domain) | `["Disabled", "SteamRefresh"]` |
| `mn/mx/st` | Min/max/step for `number` domain | `0.0`, `65535.0`, `1.0` |
| `fi` | Field ID for sub-fields in multi-byte ERDs | `"critical_major"` |
| `m` | Mode (`"box"` for number) | `"box"` |
| `pon/poff/son/soff` | Payload on/off, state on/off | `"01"`, `"00"` |

### How the JSONL is consumed

1. **MQTT discovery**: The ESPHome bridge reads these JSONL files at startup. Each line becomes a Home Assistant MQTT discovery message published to `homeassistant/<domain>/<erd_id>/config`.
2. **Value decoding**: When the appliance publishes a hex payload on an ERD topic (e.g., `appliance/0001`), the bridge evaluates the `vt` Jinja2 template against the raw hex string to produce the HA display value.
3. **Command encoding**: When HA sends a command to a `select`/`number`/`switch`, the bridge evaluates the `ct` template to convert the user value back to hex for the appliance protocol.
4. **Multi-field ERDs**: Complex ERDs (version numbers with 4 sub-fields, bit-field sensors) are split into separate entities with `fi` field IDs. The `vt` template slices the correct hex range from the full payload.
5. **Category routing**: Files are split by appliance category (0x0000–0x0FFF = common, etc.) so the bridge can selectively load only relevant entities for a given appliance type.

## Scripts Directory (`scripts/`)

Collection of Python utilities for maintaining and validating the ERD definitions:

- **`ha_constants.py`** — Authoritative definitions of valid HA device classes, units, state classes, and their constraints. Used by all validators.
- **`validate_device_classes.py`** — CI-gated: checks `device_class` values are valid for each ERD's data types. Run before committing.
- **`validate_ha_domain_rules.py`** — Validates HA domain assignments against ERD data types.
- **`validate_pairings.py`** — Validates request/status ERD pairings (bidirectional consistency).
- **`validate_scaling_consistency.py`** — Checks scaling factor consistency across paired ERDs.
- **`validate_ha_completeness.py`** — Ensures all controllable ERDs have HA metadata.
- **`auto_assign_ha_metadata.py`** — Suggests `ha_domain`, `device_class`, `unit_of_measurement` based on ERD names and types.
- **`auto_detect_pairings.py`** — Auto-detects request/status ERD pairings.
- **`auto_detect_scaling.py`** — Auto-detects scaling factors from field names.
- **`annotate_field_metadata.py`** — Adds metadata annotations to ERD fields.
- **`generate_controllable_erds.py`** — Generates `doc/controllable_erds.md` (213 controllable ERDs with their HA domains).
- **`generate_coverage_report.py`** — Coverage analysis of ERD metadata completeness.
- **`sync_upstream.py`** — Syncs ERD definitions from upstream source.
- **`apply_all_suggestions.py`** — Applies auto-detected metadata suggestions to the JSON.
- **`review_field_changes.py`** — Reviews field-level changes between JSON versions.
- **`clean_empty_device_class.py`** — Removes empty `device_class` fields.
- **`format_json.py`** — Formats the ERD JSON file (preserving the non-standard compact format).
- **`validate_json_format.py`** — Validates the ERD JSON format rules.
- **`validator_utils.py`** — Shared utilities for all validators.

## Controllable ERDs

`doc/controllable_erds.md` lists 213 ERDs that can be controlled (have write operations or paired request/status). These map to HA `switch`, `select`, `number`, `button`, and `binary_sensor` domains. Generated by `scripts/generate_controllable_erds.py`.

## Key Design Decisions

- **Filtering is aggressive**: Most raw entity entries are filtered out because they represent internal diagnostics, firmware metadata, commissioning state, or service-mode data not useful to end users in Home Assistant. See `doc/erd_rules.md` for the complete list.
- **Jinja2 templates over Python**: The bridge uses Jinja2 for value/command templates rather than compiled Python, allowing the templates to be generated from data and evaluated at runtime.
- **Hex protocol**: All appliance communication is hex-encoded. Templates handle two's-complement conversion, scaling, enum mapping, and ASCII decoding.
- **Category-based routing**: ERDs are split into 10 category files matching their hex ID range, allowing the bridge to load only relevant entities per appliance type.

## Entity Generation Rules (from ERD JSON analysis)

These rules are derived from patterns in `appliance_api_erd_definitions.json`. They guide how ERD data maps to HA entity types in the JSONL output.

### 1. Multi-field ERDs → one entity per sub-field

When an ERD has more than one data field, each non-reserved sub-field becomes its own JSONL entity:
- **Byte-offset fields** (different `offset`/`size`): each gets its own entity with a `field_id` slug derived from the field name.
- **Bit-field fields** (`bits` key present): each bit becomes its own entity. 1-bit fields → `binary_sensor`; multi-bit fields → `sensor`.
- **Version ERDs** (4 consecutive u8 fields: Critical Major, Critical Minor, Non-Critical Major, Non-Critical Minor): emit a single entity with a dotted-version value template (`1.0.2.3`), not 4 separate entities.
- **Multi-board version ERDs** (version fields prefixed by board name like "UI", "MC"): emit one entity per board prefix, plus optional parametric version entities.
- **Reserved/padding fields** (name contains "reserved", "padding"): skip entirely.
- **Sub-field ha_domain**: When all sub-fields of a multi-field ERD have their own `ha_domain` defined, the top-level `ha_domain` is optional and can be omitted. The JSONL generator uses sub-field domains directly.

### 2. Data type → HA domain mapping

| Data type | Preferred domain | Notes |
|---|---|---|
| `bool` | `binary_sensor`, `switch`, or `button` | Read-only on/off → `binary_sensor`. Writable toggle → `switch`. One-shot command → `button`. If the bool is part of a larger multi-field ERD, each bit gets its own `binary_sensor` entity. |
| `enum` with 2 values (On/Off, Enable/Disable, etc.) | `switch` if writable, `binary_sensor` if read-only | If the enum values are descriptive labels (e.g. Fahrenheit/Celsius, 12-hour/24-hour) rather than on/off states → `select` (writable) or `sensor` with `device_class: "enum"` (read-only). If the enum has >2 values → `select` (writable) or `sensor` with `device_class: "enum"` (read-only). |
| `enum` with >2 values | `select` if writable, `sensor` with `device_class: "enum"` if read-only | |
| `u8`, `u16`, `u32`, `i8`, `i16`, `i32` | `sensor` (read-only), `number` (writable) | Apply `scaling_factor` if present. Signed types need two's-complement handling. |
| `string` | `sensor` | ASCII hex-decoded. Typically model/serial numbers. |
| `raw` | Usually skip | Raw bytes with no semantic meaning. Often padding, hashes, or binary blobs. These should be filtered (see `doc/erd_rules.md`) but must still have valid `ha_domain`/`device_class` metadata in the JSON. |

### 3. Boolean-specific rules

- A `bool`-typed field assigned to `switch` is correct when the field is writable (request/response pattern).
- A `bool`-typed field assigned to `button` is correct when it's a one-shot command (write-and-forget).
### 4. Enum-specific rules

- **2-value enums** (e.g. `{"0": "Off", "1": "On"}`):
  - Writable → `switch` (toggle control)
  - Read-only → `binary_sensor` (state monitoring)
  - **Exception**: If the 2 values are descriptive labels (e.g. Fahrenheit/Celsius, 12-hour/24-hour) rather than on/off states → `select` (writable) or `sensor` with `device_class: "enum"` (read-only).
- **Multi-value enums** (3+ values):
  - Writable → `select` (dropdown control)
  - Read-only → `sensor` with `device_class: "enum"` (labeled display)
- Enum values of `255` labeled "Request Consumed" or "Request processed" are **write-only protocol markers** — they indicate the appliance has accepted the command. These should not appear as selectable options in HA.
### 5. Numeric type rules

- `u8`/`u16`/`u32` (unsigned): map to `sensor` (read-only) or `number` (writable). Set `min`/`max`/`step` based on the type bounds and `scaling_factor`.
- `i8`/`i16`/`i32` (signed): same as above but value templates must handle two's-complement conversion (values ≥ 2^(n-1) are negative).
- Fields with `scaling_factor` > 1: the displayed value is `raw_value / scaling_factor`. The `unit_of_measurement` should match the physical quantity (e.g., `°F`, `V`, `min`).
- `u16`/`u32` in `select` domain with no `values` map is suspicious — these are likely numeric values (temperatures, times, IDs) that should be `sensor` or `number`, not `select`.

### 6. Paired ERD (request/status) merging

Paired ERDs represent the same physical entity from two perspectives — command (request) and state (status). They should be **merged into a single JSONL entity**, not emitted as two separate entries.

- The **controllable domain** (`switch`, `select`, `number`) is the canonical entity. It drives both the HA entity type and the value/command templates.
- The **read-only domain** (`binary_sensor`, `sensor`) side is redundant and should be **dropped** when the pairing is bidirectional (request's `paired_erd` points to status, and status's `paired_erd` points back to request).
- If the pairing is **asymmetric** (request doesn't point back to status), the status ERD carries independent information — keep it as a separate entity.
- When the request side is `sensor` but the status side is `switch`/`select`/`number`, the **status side is the canonical entity** (it's the one that's actually controllable). Invert the merge: keep the status side, drop the request side.
- The merged entity uses the controllable side's `ha_domain`, `device_class`, `unit_of_measurement`, `scaling_factor`, and data structure.
- The merged entity's `value_template` should read from the status side's data (the actual current state), and the `command_template` should write to the request side's data (the command payload).

### 7. String-type rules

- `string` type → `sensor` domain. The value is hex-encoded ASCII. Templates must decode hex byte pairs to characters, skip null bytes, and strip trailing padding (`_`).
- Common string ERDs: Model Number, Serial Number, Pairing Codes. These are read-only identifiers.

### 8. Bit-field rules

- Fields with a `bits` sub-object represent individual bits within a byte/word.
- **1-bit fields** → `binary_sensor` with payload `01`/`00`.
- **Multi-bit fields** → `sensor` with integer value.
- Each bit-field sub-field gets its own entity with a `field_id` slug.
- Reserved bit positions (name contains "reserved") → skip.

### 9. Version and time-of-day ERD rules

- **Simple 4-byte versions** (Critical Major + Critical Minor + Non-Critical Major + Non-Critical Minor at offsets 0-3): single `sensor` entity with dotted-version string (`1.0.2.3`).
- **Multi-board versions** (fields prefixed by board like "UI Critical Major", "MC Critical Major"): one entity per board prefix, plus optional parametric version entities.
- **Time-of-day ERDs** (e.g. Clock Time with Hours/Minutes/Seconds at offsets 0,1,2): single `sensor` entity with dotted time template (`H:M:S`), NOT three separate entities. These are user-facing time displays, not measurements.
- Version ERDs use `device_class: "timestamp"` or no device_class (they're identifiers, not measurements).

### 10. Filtered ERDs (hidden from JSONL output)

See `doc/erd_rules.md` for the complete list of filtered ERDs with reasons and filter patterns.

Rule: **Every ERD must have valid HA metadata regardless of whether it's filtered.** Even filtered ERDs must pass all validator checks (`validate_device_classes.py`, `validate_ha_domain_rules.py`, etc.). Filtering only controls JSONL output — the JSON itself must be correct.


### 11. Entity naming

- Strip "Request" and "Status" suffixes from paired ERD names for the entity name.
- For multi-field ERDs, use the pattern: `{ERD name} - {leaf field name}`.
- Leaf field names: for dot-qualified names like "Allowed Selections.Cyclic Supported", use the last segment ("Cyclic Supported"). Exception: "PM2.5" → keep as-is (the dot is part of the value, not a separator).

### 12. Filtering / exclusion rules

Skip entities whose names match these patterns (internal noise, not user-facing):
- **Diagnostics**: "diagnostic", "fault", "reset reason", "program counter", "fault code", "linux diagnostics"
- **Firmware**: "configuration hash", "schedule hash", "SHA-256", "boot loader version", "supported image types", "engineering revision"
- **Commissioning**: "Matter", "Alexa", "voice module", "onboarding", "pairing code"
- **Service mode**: "service mode"
- **Push notifications**: "push notification"
- **Availability/allowability**: "allowed", "available", "modification available", "action available"
- **Supported features**: "supported feature", "supported state", "supported equipment"
- **Clock/time**: "clock time", "NTP", "time zone", "daylight saving"
- **Network**: "WiFi status", "signal strength", "BLE master"
- **Energy pricing**: "electrical pricing", "demand response", "time of use"
- **Camera**: "still frame", "image upload", "camera"
- **Sound**: "sound level", "sound theme"
- **Usage profile**: "usage profile"
- **Current report**: "current report"
- **Feature configuration**: "feature configuration"
- **Cycle definitions**: "cycle definition"
- **Latched key**: "latched key"
- **DIP switch**: "dip switch"
- **Most recent cycle**: "most recent cycle"
- **Unused/reserved**: "unused", "reserved"
- **Service mode**: "service mode"
- **Operational errors**: "issue", "fault", "failure", "diagnostic"

### 13. Device class assignment

- `enum` device_class: for any sensor whose data type is `enum` or whose values are labeled text (not numeric).
- `temperature`: fields with "temperature" in the name and a numeric type.
- `duration`: **ONLY for timestamp values** — i.e., sensors that report a point in time such as `sensor.last_triggered`, `sensor.last_seen`, `sensor.last_updated`. These are NOT user-input numeric values. **Do NOT use `device_class: "duration"` for timer settings, timeout values, delay minutes, cook times, runtime requests, or any other numeric input that represents a duration the user sets.** These should have `device_class: null` (or no device_class) with `unit_of_measurement` set appropriately (e.g., `"min"`, `"s"`).
- `restart`: for button-type reset commands.
- `door`, `moisture`, `battery`, `battery_charging`, `plug`, `power`: infer from field names matching known appliance states.
- `voltage`, `current`, `power`, `energy`: infer from electrical measurements with appropriate units.
- `timestamp`: for version strings (though `enum` or no device_class may be more appropriate).

### 13a. Number domain device_class rules

The `number` domain represents **user-input numeric values** (writable setpoints, timers, levels). These are fundamentally different from `sensor` domain values which represent **read-only measurements**.

- **`number` domain entities should almost NEVER have a `device_class`**. The `device_class` attribute is meaningful for `sensor` domain entities to tell Home Assistant how to interpret the measurement. For `number` domain, the `unit_of_measurement` and `min`/`max`/`step` fields are what matter.
- **Exceptions**: `device_class: "temperature"` is valid on `number` domain when the user is setting a temperature (e.g., "Desired Temperature", "User Heating Setpoint Request"). This tells Home Assistant to use temperature-appropriate UI controls.
- **Never use `device_class: "duration"` on `number` domain**. A `number` entity with `unit_of_measurement: "min"` that represents a timer setting (e.g., "Timer", "Delay Start Minutes", "Cook Time Adjustment") should have no `device_class`. The `unit_of_measurement: "min"` already conveys the meaning. Using `device_class: "duration"` would incorrectly signal to Home Assistant that this is a timestamp sensor, not a user-input number.
- **Examples of correct `number` domain metadata**:
  - `0x0050` (Timer): `ha_domain: "number"`, `device_class: null`, `unit_of_measurement: "min"` — NOT `device_class: "duration"`
  - `0x1005` (Desired Temperature): `ha_domain: "number"`, `device_class: "temperature"`, `unit_of_measurement: "°F"` — temperature is a valid exception
  - `0x5404` (Advantium Cook Time Adjustment): `ha_domain: "number"`, `device_class: null`, `unit_of_measurement: "s"` — NOT `device_class: "duration"`
  - `0x79a0` (Filter Replacement Interval Reminder Request): `ha_domain: "number"`, `device_class: null`, `unit_of_measurement: null` — no device_class needed

### 13b. Sensor domain device_class rules

- **`device_class: "duration"` is valid on `sensor` domain ONLY when the sensor reports a timestamp** (e.g., `sensor.last_triggered`). It is NOT valid for sensors that report a duration value like "time remaining" or "cycle duration" — those should use `device_class: null` with `unit_of_measurement: "min"` or `"s"`.
- Fields with "time", "minutes", "seconds" in the name and a numeric type should get `device_class: null` (not `duration`) unless they are actually timestamp sensors.


### 14. Unit of measurement

- `°F` / `°C` / `K`: temperature fields.
- `V`: voltage.
- `A`: current.
- `W`, `kW`, `kWh`: power/energy.
- `min`, `h`, `s`: time/duration.
- `%`: percentage.
- `rpm`: rotational speed.
- `CFM`: airflow.
- `steps`: step counts.

### 15. State class

- `total`: cumulative counters (energy, water, gas).
- `total_increasing`: counters that only increase (cycle counts, runtime).
- `measurement`: instantaneous values (temperature, voltage, current).
