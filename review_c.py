#!/usr/bin/env python3
"""
Review all ERDs from batch files against AGENTS.md rules.
Output: subagent_review_c.json with one entry per ERD.

This script verifies the existing ha_domain, device_class, unit_of_measurement
against AGENTS.md rules and flags any discrepancies.
"""

import json
import re
import glob as globmod
from datetime import datetime, timezone

# ── Filter patterns (from AGENTS.md §12) ──────────────────────────────────────
FILTER_PATTERNS = [
    re.compile(r'(?i)diagnostic'),
    re.compile(r'(?i)fault'),
    re.compile(r'(?i)reset\s+reason'),
    re.compile(r'(?i)program\s+counter'),
    re.compile(r'(?i)fault\s+code'),
    re.compile(r'(?i)linux\s+diagnostics'),
    re.compile(r'(?i)configuration\s+hash'),
    re.compile(r'(?i)schedule\s+hash'),
    re.compile(r'(?i)sha\s*-?\s*256'),
    re.compile(r'(?i)boot\s+loader\s+version'),
    re.compile(r'(?i)supported\s+image\s+types'),
    re.compile(r'(?i)engineering\s+revision'),
    re.compile(r'(?i)\bmatter\b'),
    re.compile(r'(?i)\balexa\b'),
    re.compile(r'(?i)voice\s+module'),
    re.compile(r'(?i)onboarding'),
    re.compile(r'(?i)pairing\s+code'),
    re.compile(r'(?i)service\s+mode'),
    re.compile(r'(?i)push\s+notification'),
    re.compile(r'(?i)\ballowed\b'),
    re.compile(r'(?i)\bavailable\b'),
    re.compile(r'(?i)modification\s+available'),
    re.compile(r'(?i)action\s+available'),
    re.compile(r'(?i)supported\s+feature'),
    re.compile(r'(?i)supported\s+state'),
    re.compile(r'(?i)supported\s+equipment'),
    re.compile(r'(?i)clock\s+time'),
    re.compile(r'(?i)\bntp\b'),
    re.compile(r'(?i)time\s+zone'),
    re.compile(r'(?i)daylight\s+saving'),
    re.compile(r'(?i)wifi\s+status'),
    re.compile(r'(?i)signal\s+strength'),
    re.compile(r'(?i)ble\s+master'),
    re.compile(r'(?i)electrical\s+pricing'),
    re.compile(r'(?i)demand\s+response'),
    re.compile(r'(?i)time\s+of\s+use'),
    re.compile(r'(?i)still\s+frame'),
    re.compile(r'(?i)image\s+upload'),
    re.compile(r'(?i)\bcamera\b'),
    re.compile(r'(?i)sound\s+level'),
    re.compile(r'(?i)sound\s+theme'),
    re.compile(r'(?i)usage\s+profile'),
    re.compile(r'(?i)current\s+report'),
    re.compile(r'(?i)feature\s+configuration'),
    re.compile(r'(?i)cycle\s+definition'),
    re.compile(r'(?i)latched\s+key'),
    re.compile(r'(?i)dip\s+switch'),
    re.compile(r'(?i)most\s+recent\s+cycle'),
    re.compile(r'(?i)\bunused\b'),
    re.compile(r'(?i)\breserved\b'),
    re.compile(r'(?i)\bissue\b'),
    re.compile(r'(?i)\bfailure\b'),
]


def is_reserved_or_padding(name):
    lower = name.lower()
    return 'reserved' in lower or 'padding' in lower or 'unused' in lower


def is_clock_time_erd(data_fields):
    if len(data_fields) != 3:
        return False
    types = [f['type'] for f in data_fields]
    offsets = [f['offset'] for f in data_fields]
    if offsets != [0, 1, 2] or types != ['u8', 'u8', 'u8']:
        return False
    names_lower = [f['name'].lower() for f in data_fields]
    has_hours = any('hours' in n for n in names_lower)
    has_minutes = any('minutes' in n for n in names_lower)
    has_seconds = any('seconds' in n for n in names_lower)
    return has_hours and has_minutes and has_seconds


def is_version_erd(data_fields):
    if len(data_fields) != 4:
        return False
    types = [f['type'] for f in data_fields]
    offsets = [f['offset'] for f in data_fields]
    if offsets != [0, 1, 2, 3] or types != ['u8', 'u8', 'u8', 'u8']:
        return False
    names_lower = [f['name'].lower() for f in data_fields]
    version_kw = {'critical', 'major', 'minor', 'non-critical', 'noncritical'}
    found = set()
    for n in names_lower:
        for kw in version_kw:
            if kw in n:
                found.add(kw)
    return 'critical' in found and ('major' in found or 'minor' in found)


def should_filter(name):
    for pattern in FILTER_PATTERNS:
        if pattern.search(name):
            return True, pattern.pattern
    return False, None


def get_unit_from_name(name):
    lower = name.lower()
    if 'temp' in lower and ('°f' in lower or 'fahrenheit' in lower):
        return '°F'
    if 'temp' in lower and ('°c' in lower or 'celsius' in lower):
        return '°C'
    if 'temp' in lower:
        return None
    if 'volt' in lower:
        return 'V'
    if 'current' in lower and 'report' not in lower:
        return 'A'
    if 'power' in lower:
        return 'W'
    if 'energy' in lower:
        return 'kWh'
    if 'humidity' in lower:
        return '%'
    if 'pressure' in lower:
        return 'hPa'
    if 'illuminance' in lower or 'light' in lower:
        return 'lx'
    if 'distance' in lower:
        return 'mm'
    if 'battery' in lower and 'charging' in lower:
        return '%'
    if 'battery' in lower:
        return '%'
    if 'speed' in lower and 'rpm' in lower:
        return 'rpm'
    if 'speed' in lower:
        return '%'
    if 'cfm' in lower or 'airflow' in lower:
        return 'CFM'
    if 'gal' in lower or 'gallon' in lower:
        return 'gal'
    if 'steps' in lower:
        return 'steps'
    if 'minute' in lower or 'min' in lower:
        return 'min'
    if 'second' in lower or 'secs' in lower:
        return 's'
    if 'hour' in lower:
        return 'h'
    return None


def get_device_class_from_name(name, field_type):
    lower = name.lower()
    if 'temperature' in lower or 'temp' in lower:
        return 'temperature'
    if 'battery' in lower and 'charging' in lower:
        return 'battery_charging'
    if 'battery' in lower:
        return 'battery'
    if 'door' in lower:
        return 'door'
    if 'moisture' in lower:
        return 'moisture'
    if 'voltage' in lower:
        return 'voltage'
    if 'current' in lower and 'report' not in lower:
        return 'current'
    if 'power' in lower:
        return 'power'
    if 'energy' in lower:
        return 'energy'
    if 'humidity' in lower:
        return 'humidity'
    if 'pressure' in lower:
        return 'pressure'
    if 'illuminance' in lower:
        return 'illuminance'
    if 'distance' in lower:
        return 'distance'
    if 'plug' in lower:
        return 'plug'
    if field_type == 'enum':
        return 'enum'
    return None


def is_on_off_enum(values):
    if not values:
        return False
    vals = list(values.values())
    lower_vals = [v.lower() for v in vals]
    return set(lower_vals) == {'on', 'off'} or \
           set(lower_vals) == {'enabled', 'disabled'} or \
           set(lower_vals) == {'enable', 'disable'}


def is_descriptive_enum(values):
    if not values:
        return False
    vals = list(values.values())
    lower_vals = [v.lower() for v in vals]
    on_off_terms = {'on', 'off', 'enabled', 'disabled', 'enable', 'disable', 'true', 'false', 'yes', 'no'}
    if all(v in on_off_terms for v in lower_vals):
        return False
    return True


def strip_paired_suffix(name):
    if name.endswith('Request'):
        return name[:-len('Request')]
    if name.endswith('Status'):
        return name[:-len('Status')]
    return name


def verify_erd(erd):
    """Verify a single ERD against AGENTS.md rules. Returns review dict."""
    erd_id = erd['id']
    name = erd['name']
    data_fields = erd.get('data', [])
    operations = erd.get('operations', [])
    ha_domain = erd.get('ha_domain')
    device_class = erd.get('device_class')
    unit_of_measurement = erd.get('unit_of_measurement')
    paired_erd = erd.get('paired_erd')
    confidence = erd.get('confidence')

    filtered = False
    filter_reason = None
    issues = []

    # ── 1. Check filter patterns ──
    filt, filt_pattern = should_filter(name)
    if filt:
        filtered = True
        filter_reason = filt_pattern
        issues.append(f"Filtered: matches pattern '{filt_pattern}'")

    # ── 2. Handle multi-field ERDs ──
    if len(data_fields) > 1:
        if is_clock_time_erd(data_fields):
            # Clock Time → single dotted-time sensor
            if ha_domain != 'sensor':
                issues.append(f"Clock Time ERD → should be sensor, was {ha_domain}")
                ha_domain = 'sensor'
            if device_class is not None:
                issues.append("Clock Time ERD → device_class should be null (time-of-day, not measurement)")
                device_class = None
            issues.append("Clock Time ERD → single dotted-time sensor")
            return {
                'id': erd_id, 'name': name,
                'ha_domain': ha_domain, 'device_class': device_class,
                'unit_of_measurement': unit_of_measurement,
                'confidence': confidence or 'medium',
                'filtered': filtered, 'filter_reason': filter_reason,
                'reasoning': '; '.join(issues)
            }

        if is_version_erd(data_fields):
            # Version ERD → single dotted-version sensor
            if ha_domain != 'sensor':
                issues.append(f"Version ERD → should be sensor, was {ha_domain}")
                ha_domain = 'sensor'
            if device_class is not None:
                issues.append("Version ERD → device_class should be null (identifier, not measurement)")
                device_class = None
            issues.append("Version ERD → single dotted-version sensor")
            return {
                'id': erd_id, 'name': name,
                'ha_domain': ha_domain, 'device_class': device_class,
                'unit_of_measurement': unit_of_measurement,
                'confidence': confidence or 'medium',
                'filtered': filtered, 'filter_reason': filter_reason,
                'reasoning': '; '.join(issues)
            }

        # General multi-field: no device_class at ERD level
        if device_class is not None:
            issues.append(f"Multi-field ERD ({len(data_fields)} fields) → device_class should be null at ERD level; sub-fields carry metadata")
            device_class = None

        # If ha_domain is None for multi-field, infer from sub-fields
        if ha_domain is None:
            sub_types = [f['type'] for f in data_fields if not is_reserved_or_padding(f.get('name', ''))]
            if any(t == 'bool' for t in sub_types):
                ha_domain = 'binary_sensor'
            elif any(t == 'enum' for t in sub_types):
                ha_domain = 'sensor'
            elif any(t in ('u8', 'u16', 'u32', 'i8', 'i16', 'i32') for t in sub_types):
                ha_domain = 'sensor'
            elif any(t == 'string' for t in sub_types):
                ha_domain = 'sensor'
            else:
                ha_domain = 'sensor'
            issues.append(f"Multi-field ERD → inferred ha_domain from sub-fields: {ha_domain}")
        else:
            issues.append(f"Multi-field ERD ({len(data_fields)} fields)")

        return {
            'id': erd_id, 'name': name,
            'ha_domain': ha_domain, 'device_class': device_class,
            'unit_of_measurement': unit_of_measurement,
            'confidence': confidence or 'medium',
            'filtered': filtered, 'filter_reason': filter_reason,
            'reasoning': '; '.join(issues)
        }

    # ── 3. Single-field ERDs ──
    if len(data_fields) == 1:
        field = data_fields[0]
        field_type = field['type']
        field_name = field['name']

        # Raw type
        if field_type == 'raw':
            if ha_domain is None:
                ha_domain = None
            issues.append("Raw type → typically filtered/internal")
            return {
                'id': erd_id, 'name': name,
                'ha_domain': ha_domain, 'device_class': None,
                'unit_of_measurement': None,
                'confidence': confidence or 'low',
                'filtered': filtered, 'filter_reason': filter_reason,
                'reasoning': '; '.join(issues)
            }

        # Bool type
        if field_type == 'bool':
            # Check if paired
            if paired_erd:
                # Paired bool → switch (controllable)
                if ha_domain != 'switch':
                    issues.append(f"Bool + paired ERD → should be switch (controllable), was {ha_domain}")
                    ha_domain = 'switch'
                issues.append("Bool + paired ERD → switch (writable toggle)")
            elif 'write' in operations:
                # Writable bool → switch
                if ha_domain != 'switch':
                    issues.append(f"Bool + write → should be switch, was {ha_domain}")
                    ha_domain = 'switch'
                issues.append("Bool + write → switch (writable toggle)")
            else:
                # Read-only (read/publish only) → binary_sensor
                if ha_domain != 'binary_sensor':
                    issues.append(f"Bool read-only → should be binary_sensor, was {ha_domain}")
                    ha_domain = 'binary_sensor'
                issues.append("Bool read-only → binary_sensor")

        # Enum type
        elif field_type == 'enum':
            values = field.get('values', {})
            num_values = len(values)

            if num_values == 2:
                if is_on_off_enum(values):
                    # On/Off style → switch (writable) or binary_sensor (read-only)
                    if 'write' in operations:
                        expected = 'switch'
                    else:
                        expected = 'binary_sensor'
                    if ha_domain != expected:
                        device_class = None  # Reset device_class when domain changes
                    ha_domain = expected
                    if device_class is None:
                        device_class = 'enum'
                    issues.append(f"2-value On/Off enum → {ha_domain}")
                elif is_descriptive_enum(values):
                    # Descriptive labels → select (writable) or sensor (read-only)
                    if 'write' in operations:
                        expected = 'select'
                    else:
                        expected = 'sensor'
                    if ha_domain != expected:
                        device_class = None  # Reset device_class when domain changes
                    ha_domain = expected
                    if device_class is None:
                        device_class = 'enum'
                    issues.append(f"2-value descriptive enum → {ha_domain}")
                else:
                    # Other 2-value enum
                    if 'write' in operations:
                        expected = 'switch'
                    else:
                        expected = 'binary_sensor'
                    if ha_domain != expected:
                        device_class = None  # Reset device_class when domain changes
                    ha_domain = expected
                    if device_class is None:
                        device_class = 'enum'
                    issues.append(f"2-value enum → {ha_domain}")
            elif num_values > 2:
                # Multi-value enum → select (writable) or sensor (read-only)
                if 'write' in operations:
                    expected = 'select'
                else:
                    expected = 'sensor'
                if ha_domain != expected:
                    device_class = None  # Reset device_class when domain changes
                ha_domain = expected
                if device_class is None:
                    device_class = 'enum'
                issues.append(f"{num_values}-value enum → {ha_domain}")
            elif num_values == 1:
                # Single-value enum with write → button (one-shot command)
                if 'write' in operations:
                    if ha_domain != 'button':
                        issues.append(f"Single-value enum + write → should be button (one-shot), was {ha_domain}")
                    ha_domain = 'button'
                    if device_class is None:
                        device_class = 'restart'
                    issues.append("Single-value enum + write → button (one-shot command)")
                else:
                    if ha_domain != 'sensor':
                        issues.append(f"Single-value enum read-only → should be sensor, was {ha_domain}")
                    ha_domain = 'sensor'
                    if device_class is None:
                        device_class = 'enum'
                    issues.append("Single-value enum read-only → sensor")
            else:
                # No values defined
                if ha_domain is None:
                    ha_domain = 'sensor'
                if device_class is None:
                    device_class = 'enum'
                issues.append("Enum with no values defined")

        # Numeric types
        elif field_type in ('u8', 'u16', 'u32', 'i8', 'i16', 'i32'):
            if 'write' in operations:
                expected = 'number'
            else:
                expected = 'sensor'
            if ha_domain != expected:
                issues.append(f"{field_type} numeric → should be {expected}, was {ha_domain}")
            ha_domain = expected

            # Device class
            if device_class is None:
                dc = get_device_class_from_name(field_name, field_type)
                if dc:
                    device_class = dc

            # Unit of measurement
            if unit_of_measurement is None:
                uom = get_unit_from_name(field_name)
                if uom:
                    unit_of_measurement = uom

            # Number domain: almost NEVER device_class (except temperature)
            if ha_domain == 'number' and device_class and device_class != 'temperature':
                device_class = None
                issues.append("Number domain → no device_class (except temperature)")

            issues.append(f"{field_type} numeric → {ha_domain}")

        # String type
        elif field_type == 'string':
            if ha_domain != 'sensor':
                issues.append(f"String type → should be sensor, was {ha_domain}")
            ha_domain = 'sensor'
            if device_class is None:
                device_class = None
            issues.append("String type → sensor")

        else:
            if ha_domain is None:
                ha_domain = 'sensor'
            if device_class is None:
                device_class = None
            issues.append(f"Unknown type '{field_type}' → sensor")

    # ── 4. Paired ERD handling ──
    if paired_erd:
        name_base = strip_paired_suffix(name)
        if name_base != name:
            issues.append(f"Paired ERD → stripped '{name}' → '{name_base}'")

    # ── 5. Confidence ──
    if filtered and confidence is None:
        confidence = 'low'
    elif device_class and ha_domain and confidence is None:
        confidence = 'high'
    elif ha_domain and confidence is None:
        confidence = 'medium'

    return {
        'id': erd_id, 'name': name,
        'ha_domain': ha_domain, 'device_class': device_class,
        'unit_of_measurement': unit_of_measurement,
        'confidence': confidence,
        'filtered': filtered, 'filter_reason': filter_reason,
        'reasoning': '; '.join(issues)
    }


def main():
    results = []
    batch_files = sorted(globmod.glob('/home/joshua/public-appliance-api-documentation/batch_*.json'))

    for batch_file in batch_files:
        with open(batch_file) as f:
            erds = json.load(f)
        for erd in erds:
            review = verify_erd(erd)
            results.append(review)

    output_path = '/home/joshua/public-appliance-api-documentation/subagent_review_c.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(results)} entries to {output_path}")

    # Summary stats
    domains = {}
    filtered_count = 0
    changed_count = 0
    for r in results:
        d = r['ha_domain'] or 'none'
        domains[d] = domains.get(d, 0) + 1
        if r['filtered']:
            filtered_count += 1
        if r['reasoning'] and 'should be' in r['reasoning']:
            changed_count += 1

    print(f"\nDomain distribution:")
    for d in sorted(domains.keys()):
        print(f"  {d}: {domains[d]}")
    print(f"\nFiltered: {filtered_count}/{len(results)}")
    print(f"ERDs with changes flagged: {changed_count}/{len(results)}")


if __name__ == '__main__':
    main()