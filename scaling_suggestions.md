# Scaling Factor Suggestions

Generated: 2026-06-30 15:53:55 UTC

**Total suggestions: 7**

| ERD ID | Name | Suggested scaling_factor | Field Name |
|--------|------|--------------------------|------------|
| 0x1160 | POE Water Flow Rate | 100 | Water Valve Flow Rate GallonsX100/Minute |
| 0x130e | Mixing Spraying Data Request | 10 | Top Spray Time In SecondsX10 |
| 0x14c5 | Secondary Feature Pan Filtered Temperature Resolved | 100 | Secondary Feature Pan Filtered Temperature Resolved (fahrenheit x 100) |
| 0x7116 | Estimated External Thermostat Target Setpoint Temperature | 10 | Estimated Target Setpoint Temperature °Fx10 |
| 0x7117 | Target Dew Point temperature | 10 | Target Dew Point temperature °Fx10 |
| 0x746e | Heat Pump Lockout Temperature Status | 10 | Heat Pump Lockout Temperature Status.Heat Pump Lockout Temperature in Fahrenheit x 10 |
| 0x746f | Heat Pump Lockout Temperature Request | 10 | Heat Pump Lockout Temperature in Fahrenheit x 10 |

## Review Notes

- Scaling factors are inferred from field name patterns like `x 100`, `Fx10`, `GallonsX100`
- Only ERDs **missing** a `scaling_factor` are included
- All suggestions should be reviewed before applying to the JSON file
- Use surgical text edits per AGENTS.md rules when applying suggestions
