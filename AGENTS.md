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

# Project Context

## What This Repo Is

This repository documents the **GE Appliances Public Appliance API** — a binary protocol used by GE smart home appliances for local network communication. The API uses **ERDs** (Entity Record Definitions) to define every readable/writable parameter an appliance exposes.

The primary data file is `appliance_api_erd_definitions.json` — a single JSON file containing ~2,200 ERD definitions across all appliance categories. Each ERD specifies:
- `id`: hex identifier (e.g. `"0x0001"`)
- `name`, `description`: human-readable metadata
- `data`: array of fields with `type` (u8/u16/u32/i8/i16/i32/enum/string/bool), `offset`, `size`, and optional `values`/`bits`
- `operations`: array of API operations (`read`, `write`, `publish`, `subscribe`)
- `updateClass`: update class metadata

**The source JSON contains NO Home Assistant metadata.** All HA domain, device_class, unit_of_measurement, and other metadata is assigned during the review process and stored in the flattened review file.

## Review Workflow

### Step 1: Generate Flattened Review File

```bash
python3 scripts/generate_flattened_review.py
```

This reads `appliance_api_erd_definitions.json` and `appliance_api.json`, producing `erd_flattened.json` with one entry per sub-field (~15,423 entries from ~2,200 ERDs). Each entry has:
- Source fields: `erd_id`, `erd_name`, `erd_description`, `erd_operations`, `erd_updateClass`, `field_name`, `field_type`, `field_offset`, `field_size`, `field_values`, `field_bits`
- Generated: `erd_features` (from `appliance_api.json` feature API mappings)
- Empty `review` section for the agent to fill in

### Step 2: Review Each Entry

For each entry in `erd_flattened.json`, fill in the `review` section:

```json
"review": {
  "ha_domain": "sensor",
  "device_class": "temperature",
  "unit_of_measurement": "°F",
  "scaling_factor": null,
  "state_class": "measurement",
  "paired_erd": null,
  "pair_role": null,
  "filtered": false,
  "filter_reason": null,
  "reasoning": "read-only temperature sensor"
}
```

Follow the Entity Generation Rules below to determine each field.

### Step 3: Apply Review to Source JSON

After review, a script merges the `review` data back into `appliance_api_erd_definitions.json`, adding `ha_domain`, `device_class`, `unit_of_measurement`, `scaling_factor`, `state_class`, `paired_erd`, `pair_role` to the appropriate ERD/field entries.

### Step 4: Generate JSONL

```bash
python3 generate_ha_discovery.py --erd-definitions appliance_api_erd_definitions.json
```

## Home Assistant MQTT Discovery Pipeline

The repo generates **Home Assistant MQTT discovery JSONL files** from the ERD definitions. This is the bridge between the appliance API documentation and the ESPHome Home Assistant bridge that actually controls appliances.

### Script: `generate_ha_discovery.py`

Copied from [eddietheengineer/home-assistant-bridge-esphome](https://github.com/eddietheengineer/home-assistant-bridge-esphome/blob/develop/scripts/generate_ha_discovery.py). Run it to regenerate the JSONL files:

```bash
python3 generate_ha_discovery.py --erd-definitions appliance_api_erd_definitions.json
```

**What it does:**
1. Reads `appliance_api_erd_definitions.json` (2,199 ERDs)
2. Filters out entities matching internal metadata patterns (diagnostics, commissioning, firmware hashes, service mode, etc.) via regex on entity names
3. Classifies each ERD's data structure: `single`, `byte_offset`, `bitfield`, `mixed`, `version`, or `multi_board_version`
4. Generates Jinja2 `value_template` and `command_template` strings for each HA entity
5. Outputs category-specific JSONL files into `ha_discovery/`

### Output: `ha_discovery/*.jsonl`

10 JSONL files organized by appliance category.

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
5. **Category routing**: Files are split by appliance category (0x0000–0x0FFF = common, etc.) so the bridge can selectively load only relevant entities per appliance type.

## Scripts Directory (`scripts/`)

Collection of Python utilities for maintaining and validating the ERD definitions:

- **`generate_flattened_review.py`** — Generates `erd_flattened.json` from source JSON for review.
- **`ha_constants.py`** — Authoritative definitions of valid HA device classes, units, state classes, and their constraints.
- **`validate_json_format.py`** — Validates the ERD JSON format rules.
- **`format_json.py`** — Formats the ERD JSON file (preserving the non-standard compact format).
- **`validator_utils.py`** — Shared utilities for validators.

## Key Design Decisions

- **Filtering is aggressive**: Most raw entity entries are filtered out because they represent internal diagnostics, firmware metadata, commissioning state, or service-mode data not useful to end users in Home Assistant.
- **Jinja2 templates over Python**: The bridge uses Jinja2 for value/command templates rather than compiled Python, allowing the templates to be generated from data and evaluated at runtime.
- **Hex protocol**: All appliance communication is hex-encoded. Templates handle two's-complement conversion, scaling, enum mapping, and ASCII decoding.
- **Category-based routing**: ERDs are split into 10 category files matching their hex ID range, allowing the bridge to load only relevant entities per appliance type.
- **Review-first workflow**: HA metadata is not in the source JSON. It is assigned during review via the flattened review file, then merged back into the source.

## Entity Generation Rules

These rules guide how ERD data maps to HA entity types in the JSONL output. They are applied during the review process to fill in the `review` section of each entry in `erd_flattened.json`.

### 1. Multi-field ERDs → one entity per sub-field

When an ERD has more than one data field, each non-reserved sub-field becomes its own JSONL entity:
- **Byte-offset fields** (different `offset`/`size`): each gets its own entity with a `field_id` slug derived from the field name.
- **Bit-field fields** (`bits` key present): each bit becomes its own entity. 1-bit fields → `binary_sensor`; multi-bit fields → `sensor`.
- **Version ERDs** (4 consecutive u8 fields: Critical Major, Critical Minor, Non-Critical Major, Non-Critical Minor): emit a single entity with a dotted-version value template (`1.0.2.3`), not 4 separate entities.
- **Multi-board version ERDs** (version fields prefixed by board name like "UI", "MC"): emit one entity per board prefix, plus optional parametric version entities.
- **Reserved/padding fields** (name contains "reserved", "padding"): skip entirely.

### 2. Data type → HA domain mapping

| Data type | Preferred domain | Notes |
|---|---|---|
| `bool` | `binary_sensor`, `switch`, or `button` | Read-only on/off → `binary_sensor`. Writable toggle → `switch`. One-shot command → `button`. |
| `enum` with 2 values (On/Off, Enable/Disable, etc.) | `switch` if writable, `binary_sensor` if read-only | If the enum values are descriptive labels (e.g. Fahrenheit/Celsius, 12-hour/24-hour) rather than on/off states → `select` (writable) or `sensor` with `device_class: "enum"` (read-only). **Note**: "descriptive labels" means values that are not simple on/off states — e.g. "12 Hour Time"/"24 Hour Time"/"No Clock Display" or "Normal"/"Boost". If values are "On"/"Off", "Locked"/"Not Locked", "Enabled"/"Disabled" → treat as On/Off pair, use `switch`/`binary_sensor`. |
| `enum` with >2 values | `select` if writable, `sensor` with `device_class: "enum"` if read-only | |
| `u8`, `u16`, `u32`, `i8`, `i16`, `i32` | `sensor` (read-only), `number` (writable) | Signed types need two's-complement handling. |
| `string` | `sensor` | ASCII hex-decoded. Typically model/serial numbers. |
| `raw` | Usually skip | Raw bytes with no semantic meaning. These should be filtered. |

**Determining writability**: Check `erd_operations`. If `"write"` is in the operations array, the field is writable. If only `"read"`, `"publish"`, `"subscribe"` — it is read-only.

### 3. Boolean-specific rules

- Writable bools should almost always be `switch`, not `binary_sensor`.
- Read-only bools → `binary_sensor`.
- **One-shot commands**: Use `button` only for true one-shot commands (e.g., "Restart", "Factory Reset") that don't have a paired status ERD. If the ERD has a `values` map or paired status, it's a toggle → `switch`, not `button`.

### 4. Enum-specific rules

- **2-value enums** (e.g. `{"0": "Off", "1": "On"}`):
  - Writable → `switch` (toggle control)
  - Read-only → `binary_sensor` (state monitoring)
  - **Exception**: If the 2 values are descriptive labels (e.g. Fahrenheit/Celsius, 12-hour/24-hour) rather than on/off states → `select` (writable) or `sensor` with `device_class: "enum"` (read-only).
  - **Clarification**: "descriptive labels" means values that are not simple on/off states — e.g. "12 Hour Time"/"24 Hour Time"/"No Clock Display" or "Normal"/"Boost". If values are "On"/"Off", "Locked"/"Not Locked", "Enabled"/"Disabled" → treat as On/Off pair, use `switch`/`binary_sensor`.
- **Multi-value enums** (3+ values):
  - Writable → `select` (dropdown control)
  - Read-only → `sensor` with `device_class: "enum"` (labeled display)
- Enum values of `255` labeled "Request Consumed" or "Request processed" are **write-only protocol markers** — they indicate the appliance has accepted the command. These should not appear as selectable options in HA.

### 5. Numeric type rules

- `u8`/`u16`/`u32` (unsigned): map to `sensor` (read-only) or `number` (writable).
- `i8`/`i16`/`i32` (signed): same as above but value templates must handle two's-complement conversion (values ≥ 2^(n-1) are negative).
- `u16`/`u32` in `select` domain with no `values` map is suspicious — these are likely numeric values (temperatures, times, IDs) that should be `sensor` or `number`, not `select`.

### 6. Paired ERD (request/status) merging

Paired ERDs represent the same physical entity from two perspectives — command (request) and state (status). They should be **merged into a single JSONL entity**, not emitted as two separate entries.

- Paired ERDs are typically named with "Request" and "Status" suffixes, or have sequential IDs (e.g., `0x1004` and `0x1005`).
- The **controllable domain** (`switch`, `select`, `number`) is the canonical entity.
- The **read-only domain** (`binary_sensor`, `sensor`) side is redundant and should be **dropped** when the pairing is bidirectional.
- When the request side is `sensor` but the status side is `switch`/`select`/`number`, the **status side is the canonical entity**.
- Record the pairing in the `review.paired_erd` and `review.pair_role` fields.

### 7. String-type rules

- `string` type → `sensor` domain. The value is hex-encoded ASCII. Templates must decode hex byte pairs to characters, skip null bytes, and strip trailing padding (`_`).
- Common string ERDs: Model Number, Serial Number. These are read-only identifiers.

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
- **Operational errors**: "issue", "fault", "failure", "diagnostic"

**Ambiguous patterns — explicit examples**: The following patterns have caused disagreement in reviews. Use these examples to guide decisions:

- **Matter**: Filter ERDs whose names start with "Matter" and describe commissioning/internal protocol (e.g., "Matter Device On-Off Request", "Matter Fabric Count"). **Do NOT filter** Matter thermostat cluster ERDs that represent user-facing setpoints (e.g., "Matter Thermostat Cluster Occupied Cooling Setpoint Request").
- **Push notification**: Filter ERDs containing "push notification" (e.g., "Push Notification Count"). **Do NOT filter** ERDs that describe user-facing notification states.
- **Available**: Filter ERDs where "available" describes availability of internal features (e.g., "Image Capture Currently Available"). **Do NOT filter** ERDs where "available" describes user-facing feature availability (e.g., "Modification Available" for firmware updates).
- **Fault**: Filter ERDs where "fault" describes actual fault conditions (e.g., "Fault Code", "Fault Detected"). **Do NOT filter** ERDs where "fault" appears in a diagnostic context (e.g., "Fault Code History" is diagnostics, but "Fault Status" may be user-facing).
- **Raw type**: ERDs with `raw` type data fields should be filtered entirely — raw bytes have no semantic meaning for Home Assistant. This includes padding, hashes, and binary blobs.

**Gray area**: If an ERD name matches a filter pattern but you're unsure, **keep it**. It's better to have an extra entity in Home Assistant than to miss a user-facing feature.

### 11. Entity naming

- Strip "Request" and "Status" suffixes from paired ERD names for the entity name.
- For multi-field ERDs, use the pattern: `{ERD name} - {leaf field name}`.
- Leaf field names: for dot-qualified names like "Allowed Selections.Cyclic Supported", use the last segment ("Cyclic Supported"). Exception: "PM2.5" → keep as-is (the dot is part of the value, not a separator).

### 12. Device class assignment

- `enum` device_class: for any sensor whose data type is `enum` or whose values are labeled text (not numeric).
- `temperature`: fields with "temperature" in the name and a numeric type. **Note**: `device_class: "temperature"` tells Home Assistant to group temperature sensors together on graphs, use temperature-appropriate UI formatting (1 decimal place for °F), and enables temperature-specific automation triggers. Without it, HA treats the sensor as a generic number.
- `duration`: **ONLY for timestamp values** — i.e., sensors that report a point in time such as `sensor.last_triggered`, `sensor.last_seen`, `sensor.last_updated`. These are NOT user-input numeric values. **Do NOT use `device_class: "duration"` for timer settings, timeout values, delay minutes, cook times, runtime requests, or any other numeric input that represents a duration the user sets.** These should have `device_class: null` with `unit_of_measurement` set appropriately (e.g., `"min"`, `"s"`).
- `restart`: for button-type reset commands.
- `door`, `moisture`, `battery`, `battery_charging`, `plug`, `power`: infer from field names matching known appliance states.
- `voltage`, `current`, `power`, `energy`: infer from electrical measurements with appropriate units.
- `timestamp`: for version strings (though `enum` or no device_class may be more appropriate).

### 13. Number domain device_class rules

The `number` domain represents **user-input numeric values** (writable setpoints, timers, levels).

- **`number` domain entities should almost NEVER have a `device_class`**. The `device_class` attribute is meaningful for `sensor` domain entities to tell Home Assistant how to interpret the measurement. For `number` domain, the `unit_of_measurement` and `min`/`max`/`step` fields are what matter.
- **Exceptions**: `device_class: "temperature"` is valid on `number` domain when the user is setting a temperature (e.g., "Desired Temperature", "User Heating Setpoint Request").
- **Never use `device_class: "duration"` on `number` domain**. A `number` entity with `unit_of_measurement: "min"` that represents a timer setting should have no `device_class`.

### 14. Sensor domain device_class rules

- **`device_class: "duration"` is valid on `sensor` domain ONLY when the sensor reports a timestamp** (e.g., `sensor.last_triggered`). It is NOT valid for sensors that report a duration value like "time remaining" or "cycle duration" — those should use `device_class: null` with `unit_of_measurement: "min"` or `"s"`.

### 15. Percentage and speed sensors

- Sensors reporting percentages (fan speed, pump speed, light level, brightness, current limiting, etc.) should have `unit_of_measurement: "%"`.
- **Do NOT use `unit_of_measurement: "rpm"` for percentage-based fan speed controls**. If the ERD describes fan speed as a percentage (e.g., "0 = OFF to X = Max Speed"), use `unit_of_measurement: "%"`. Use `"rpm"` only when the sensor reports actual rotational speed from a physical RPM measurement.

### 16. Sensors with no standard HA device_class

Some sensor types don't map to any Home Assistant `device_class`. These are valid and should have `device_class: null`:
- **Turbidity sensors**: Raw NTU measurements.
- **Light level sensors**: Raw light level readings (not lux meters).
- **Protocol request/response markers**: ERDs with a single u8 field where value 255 means "request consumed".
- **Internal notifications**: ERDs containing reserved bytes and expiry notifications.
- **Heartbeat ticks**: Protocol-level heartbeat counters.
- **Device indices/UIDs**: Identifiers used to index into other ERDs or sessions.

### 17. Multi-field ERDs

ERDs with multiple sub-fields should have **no `device_class` at the ERD level**. Metadata belongs on individual sub-fields.

### 18. Unit of measurement

- `°F` / `°C` / `K`: temperature fields.
- `V`: voltage.
- `A`: current.
- `W`, `kW`, `kWh`: power/energy.
- `min`, `h`, `s`: time/duration.
- `%`: percentage.
- `rpm`: rotational speed.
- `CFM`: airflow.
- `steps`: step counts.

### 19. State class

- `total`: cumulative counters (energy, water, gas).
- `total_increasing`: counters that only increase (cycle counts, runtime).
- `measurement`: instantaneous values (temperature, voltage, current).

### 20. JSON formatter behavior

**`format_erd_json()` preserves key and data field order exactly as they exist in the input dict.** It does NOT reorder anything.

**Never modify data field order in the dict before calling `format_erd_json()`.** If you need to reorder data fields, do it before any modifications, not after.

### 21. `raw` type fields

ERDs with `raw` type data fields contain unstructured bytes (padding, hashes, binary blobs). These are expected and should be filtered.

### 22. String sub-fields in multi-field ERDs

The generator (`generate_ha_discovery.py`) supports `string` type sub-fields within multi-field ERDs. When a multi-field ERD has a `string` type field, the `_byte_subfield_value_template()` function generates a Jinja2 template that slices the correct hex range, converts to ASCII, skips null bytes, and strips trailing `_` padding.