# HA Metadata Suggestions

Generated: 2026-06-30 15:41:32 UTC

**Total suggestions: 41**

## High Confidence (28)

| ERD ID | Name | ha_domain | device_class | unit | state_class | confidence | comment |
|--------|------|-----------|--------------|------|-------------|------------|---------|
| 0x1176 | Water Filter 1 Status Details | sensor |  |  |  | high | Auto-suggested: Water Filter 1 Status Details |
| 0x1177 | Water Filter 2 Status Details | sensor |  |  |  | high | Auto-suggested: Water Filter 2 Status Details |
| 0x1178 | Home Water Filter Platform | sensor |  |  |  | high | Auto-suggested: Home Water Filter Platform |
| 0x1179 | Home Water Filter 0 Type Information | sensor |  |  |  | high | Auto-suggested: Home Water Filter 0 Type Information |
| 0x117a | Home Water Filter 1 Type Information | sensor |  |  |  | high | Auto-suggested: Home Water Filter 1 Type Information |
| 0x117b | Home Water Filter 2 Type Information | sensor |  |  |  | high | Auto-suggested: Home Water Filter 2 Type Information |
| 0x141f | Barcode Scan History | sensor |  |  |  | high | Auto-suggested: Barcode Scan History |
| 0x14bd | Variable Cube Size Setting Data 0 | sensor |  |  |  | high | Auto-suggested: Variable Cube Size Setting Data 0 |
| 0x14bf | Variable Cube Size Status 0 | sensor |  |  |  | high | Auto-suggested: Variable Cube Size Status 0 |
| 0x14c0 | Variable Cube Size Setting Data 2 | sensor |  |  |  | high | Auto-suggested: Variable Cube Size Setting Data 2 |
| 0x14c2 | Variable Cube Size Status 2 | sensor |  |  |  | high | Auto-suggested: Variable Cube Size Status 2 |
| 0x14c4 | Dimmable Lighting 0 Warmth Percentage Setting | sensor |  |  |  | high | Auto-suggested: Dimmable Lighting 0 Warmth Percentage Setting |
| 0x14c5 | Secondary Feature Pan Filtered Temperature Resolved | sensor | temperature | °F | measurement | high | Auto-suggested: Secondary Feature Pan Filtered Temperature Resolved (device_class inferred from name keyword, unit inferred from field name pattern, state_class inferred from device_class) |
| 0x14c7 | System Power Off Status | binary_sensor |  |  |  | high | Auto-suggested: System Power Off Status |
| 0x14c8 | Scanned Barcode Result | sensor |  |  |  | high | Auto-suggested: Scanned Barcode Result |
| 0x2339 | Commercial Remote Free Mode Status | sensor |  |  |  | high | Auto-suggested: Commercial Remote Free Mode Status |
| 0x3088 | Analog Door Latch AD Counts | sensor |  |  |  | high | Auto-suggested: Analog Door Latch AD Counts |
| 0x5052 | Cook Cam Image Capture Signal | sensor |  |  |  | high | Auto-suggested: Cook Cam Image Capture Signal |
| 0x5054 | Cook Cam Image Upload Enabled Setting Status | binary_sensor |  |  |  | high | Auto-suggested: Cook Cam Image Upload Enabled Setting Status |
| 0x512c | Local Available Cook Modes Cavity 1 | sensor |  |  |  | high | Auto-suggested: Local Available Cook Modes Cavity 1 |
| 0x630b | Voice Diagnostics - Wake Word and Command Counts | sensor |  |  |  | high | Auto-suggested: Voice Diagnostics - Wake Word and Command Counts |
| 0x630c | Voice Diagnostics - Total Android Platform Voice Command Activations | sensor |  |  |  | high | Auto-suggested: Voice Diagnostics - Total Android Platform Voice Command Activations |
| 0x630d | Voice Diagnostics - Total Appliance Specific Voice Command Activations | sensor |  |  |  | high | Auto-suggested: Voice Diagnostics - Total Appliance Specific Voice Command Activations |
| 0x630f | Voice Features Enable Status | binary_sensor |  |  |  | high | Auto-suggested: Voice Features Enable Status |
| 0x746e | Heat Pump Lockout Temperature Status | sensor | temperature | °F | measurement | high | Auto-suggested: Heat Pump Lockout Temperature Status (device_class inferred from name keyword, unit inferred from field name pattern, state_class inferred from device_class) |
| 0x7470 | Input Current Limiting Status | sensor |  |  |  | high | Auto-suggested: Input Current Limiting Status |
| 0x7472 | Heat Source Optimization Status | sensor |  |  |  | high | Auto-suggested: Heat Source Optimization Status |
| 0x9140 | Water Level Tone Setting Current State | binary_sensor |  |  |  | high | Auto-suggested: Water Level Tone Setting Current State |

## Medium Confidence (13)

| ERD ID | Name | ha_domain | device_class | unit | state_class | confidence | comment |
|--------|------|-----------|--------------|------|-------------|------------|---------|
| 0x14be | Variable Cube Size Request 0 | number |  |  |  | medium | Auto-suggested: Variable Cube Size Request 0 |
| 0x14c1 | Variable Cube Size Request 2 | number |  |  |  | medium | Auto-suggested: Variable Cube Size Request 2 |
| 0x14c3 | Dimmable Lighting 0 Warmth Percentage Request | number |  |  |  | medium | Auto-suggested: Dimmable Lighting 0 Warmth Percentage Request |
| 0x14c6 | System Power Off Request | switch |  |  |  | medium | Auto-suggested: System Power Off Request |
| 0x2338 | Commercial Remote Free Mode Request | select |  |  |  | medium | Auto-suggested: Commercial Remote Free Mode Request |
| 0x5053 | Cook Cam Image Upload Enabled Setting Request | switch |  |  |  | medium | Auto-suggested: Cook Cam Image Upload Enabled Setting Request |
| 0x5675 | Start Closed-Loop Cooking Cook Timer | switch |  |  |  | medium | Auto-suggested: Start Closed-Loop Cooking Cook Timer |
| 0x6003 | Wireless Connection State | select |  |  |  | medium | Auto-suggested: Wireless Connection State |
| 0x630e | Voice Feature Enable Request | switch |  |  |  | medium | Auto-suggested: Voice Feature Enable Request |
| 0x746f | Heat Pump Lockout Temperature Request | number |  | °F |  | medium | Auto-suggested: Heat Pump Lockout Temperature Request (unit inferred from field name pattern) |
| 0x7471 | Input Current Limiting Request | number |  |  |  | medium | Auto-suggested: Input Current Limiting Request |
| 0x7473 | Heat Source Optimization Request | select |  |  |  | medium | Auto-suggested: Heat Source Optimization Request |
| 0x9141 | Water Level Tone Setting Requested State | switch |  |  |  | medium | Auto-suggested: Water Level Tone Setting Requested State |

## Review Notes

- **High confidence**: Suggestions based on clear type mappings (bool → binary_sensor, numeric → sensor)
- **Medium confidence**: Suggestions based on writable status or enum heuristics
- **Low confidence**: Suggestions that need manual verification
- All suggestions should be reviewed before applying to the JSON file
- Use surgical text edits per AGENTS.md rules when applying suggestions
