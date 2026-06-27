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
