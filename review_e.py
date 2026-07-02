#!/usr/bin/env python3
"""
Review all ERDs from batch files and produce subagent_review_e.json.
Applies AGENTS.md rules strictly, aligned with generate_ha_discovery.py behavior.
"""
import json
import glob
import re
import os

BATCH_DIR = "/home/joshua/public-appliance-api-documentation"
OUTPUT = os.path.join(BATCH_DIR, "subagent_review_e.json")

# Filter patterns from generate_ha_discovery.py (authoritative)
_FILTER_PATTERNS = [
    # OS/board-level diagnostics
    re.compile(r"(?i)(linux diagnostics|GEA.*interface diagnostic|non-volatile usage warning|reset reason|seconds since last reset|program counter.*failed assertion|fault code)"),
    # Internal firmware metadata
    re.compile(r"(?i)(configuration hash|schedule hash|SHA-256|boot loader version|supported image types|ready to enter boot|engineering revision setup)"),
    # CSM fault data
    re.compile(r"(?i)csm fault data"),
    # Matter/Alexa commissioning
    re.compile(r"(?i)(Alexa.*registration|Alexa.*status|Matter.*device|Matter.*commissioning|Matter.*onboarding|Matter.*product ID|Matter.*temperature display|Matter.*keypad lockout|voice module)"),
    # Push notifications
    re.compile(r"(?i)push notification"),
    # Min/max bounds for settings
    re.compile(r"(?i)(limit|min.*max|allowable.*range|range data|expiration limit|target temperature range)"),
    # Metadata about which settings can be changed
    re.compile(r"(?i)(modification available|action available|editable|available.*mode|action availability|available.*setting|availability)"),
    # Feature capability flags
    re.compile(r"(?i)(supported.*feature|supported.*state|supported.*equipment|supported.*sound theme|supported.*enhanced|supported.*notification|supported.*setting|supported.*device)"),
    # Request-side mirrors of status ERDs
    re.compile(r"(?i)(requested.*parameter|request.*setting|request.*mask|request.*configuration)"),
    # Appliance clock
    re.compile(r"(?i)(clock time|NTP|time zone|daylight saving|calendar)"),
    # Network diagnostics
    re.compile(r"(?i)(WiFi.*status|network.*status|signal.*strength|BLE.*master|Bluetooth.*master)"),
    # Utility pricing
    re.compile(r"(?i)(electrical.*pricing|demand response|time of use.*pricing|pricing.*structure)"),
    # Camera/image capture
    re.compile(r"(?i)(still frame|image upload|camera.*configuration|camera.*stream|inference ID|cook cam.*upload)"),
    # Sound/beep configuration
    re.compile(r"(?i)(sound level|sound theme|available sound|number of sound level)"),
    # GE cloud feature deployment
    re.compile(r"(?i)(enhanced feature|CEC|core-enhanced-cloud|request enabled enhanced|current enabled enhanced)"),
    # Usage profile
    re.compile(r"(?i)usage profile"),
    # Current report
    re.compile(r"(?i)current report"),
    # Feature configuration
    re.compile(r"(?i)feature configuration"),
    # Cycle definitions
    re.compile(r"(?i)cycle definition"),
    # Latched key status
    re.compile(r"(?i)latched key status"),
    # DIP switch
    re.compile(r"(?i)dip switch"),
    # Most recent cycle
    re.compile(r"(?i)most recent cycle status"),
    # Unused/reserved
    re.compile(r"(?i)(unused|reserved)(\s*\[.*\])?"),
    # Service mode
    re.compile(r"(?i)service mode"),
    # Issue/fault/diagnostic/failure
    re.compile(r"(?i)(issue|\bfault\b|\bfaulted\b|diagnostic|failure)"),
]


def is_filter_match(name):
    """Check if an ERD name matches any filter pattern."""
    for pattern in _FILTER_PATTERNS:
        if pattern.search(name):
            return True, pattern.pattern
    return False, None


def detect_unit_from_name(name_lower):
    """Detect unit of measurement from field name."""
    if "°f" in name_lower or "fahrenheit" in name_lower:
        return "°F"
    if "°c" in name_lower or "celsius" in name_lower:
        return "°C"
    if "voltage" in name_lower:
        return "V"
    if "current" in name_lower and "power" not in name_lower:
        return "A"
    if "power" in name_lower:
        return "W"
    if "energy" in name_lower:
        return "kWh"
    if "percent" in name_lower or "%" in name_lower:
        return "%"
    if "minute" in name_lower or "mins" in name_lower:
        return "min"
    if "min" in name_lower and "minute" not in name_lower:
        return "min"
    if "second" in name_lower or "secs" in name_lower:
        return "s"
    if "hour" in name_lower or "hrs" in name_lower:
        return "h"
    if "temperature" in name_lower:
        return "°F"
    if "humidity" in name_lower:
        return "%"
    if "pressure" in name_lower:
        return "hPa"
    if "illuminance" in name_lower or "lux" in name_lower:
        return "lx"
    if "distance" in name_lower or "depth" in name_lower:
        return "mm"
    if "battery" in name_lower and "charging" not in name_lower:
        return "%"
    if "rpm" in name_lower:
        return "rpm"
    if "gal" in name_lower:
        return "gal"
    if "cfm" in name_lower:
        return "CFM"
    if "steps" in name_lower:
        return "steps"
    return None


def detect_device_class_from_name(name_lower, ha_domain, field_type):
    """Detect device_class from field name."""
    if ha_domain == "number":
        if "temperature" in name_lower:
            return "temperature"
        return None

    if ha_domain == "binary_sensor":
        if "door" in name_lower:
            return "door"
        if "moisture" in name_lower:
            return "moisture"
        if "charging" in name_lower:
            return "battery_charging"
        if "plug" in name_lower:
            return "plug"
        return None

    if ha_domain == "sensor":
        if "temperature" in name_lower:
            return "temperature"
        if "humidity" in name_lower:
            return "humidity"
        if "voltage" in name_lower:
            return "voltage"
        if "current" in name_lower and "power" not in name_lower:
            return "current"
        if "power" in name_lower:
            return "power"
        if "energy" in name_lower:
            return "energy"
        if "pressure" in name_lower:
            return "pressure"
        if "illuminance" in name_lower or "lux" in name_lower:
            return "illuminance"
        if "distance" in name_lower:
            return "distance"
        if "battery" in name_lower and "charging" not in name_lower:
            return "battery"
        if field_type == "enum":
            return "enum"
        return None

    if ha_domain == "select":
        if field_type == "enum":
            return "enum"
        return None

    return None


def is_version_erd(fields):
    """Check if ERD is a simple 4-byte version (Critical Major/Minor, Non-Critical Major/Minor at offsets 0-3)."""
    if len(fields) != 4:
        return False
    types = [f["type"] for f in fields]
    offsets = [f["offset"] for f in fields]
    if types != ["u8", "u8", "u8", "u8"]:
        return False
    if offsets != [0, 1, 2, 3]:
        return False
    names_lower = [f["name"].lower() for f in fields]
    version_keywords = ["critical", "major", "minor", "non-critical", "noncritical", "non critical"]
    all_have_kw = any(kw in " ".join(names_lower) for kw in version_keywords)
    return all_have_kw


def is_clock_time_erd(fields):
    """Check if ERD is clock time (Hours/Minutes/Seconds at offsets 0,1,2)."""
    if len(fields) != 3:
        return False
    types = [f["type"] for f in fields]
    offsets = [f["offset"] for f in fields]
    if types != ["u8", "u8", "u8"]:
        return False
    if offsets != [0, 1, 2]:
        return False
    names_lower = [f["name"].lower() for f in fields]
    time_kw = ["hours", "minutes", "seconds", "hour", "minute", "second"]
    found = sum(1 for n in names_lower for kw in time_kw if kw in n)
    return found >= 3


def is_on_off_enum(field):
    """Check if enum has On/Off style values."""
    vals = field.get("values", {})
    if not vals:
        return False
    vals_lower = {v.lower() for v in vals.values()}
    on_off_pairs = [
        {"on", "off"},
        {"enabled", "disabled"},
        {"active", "inactive"},
        {"yes", "no"},
        {"true", "false"},
    ]
    for pair in on_off_pairs:
        if pair.issubset(vals_lower):
            return True
    return False


def is_descriptive_enum(field):
    """Check if enum has descriptive labels (not On/Off)."""
    vals = field.get("values", {})
    if not vals:
        return False
    if len(vals) == 2 and is_on_off_enum(field):
        return False
    return True


def review_erd(erd, all_erds_by_id):
    """Review a single ERD and return review result."""
    erd_id = erd["id"]
    erd_name = erd["name"]
    fields = erd.get("data", [])
    operations = erd.get("operations", [])
    ha_domain = erd.get("ha_domain")
    paired_erd = erd.get("paired_erd")
    pair_role = erd.get("pair_role")
    single_field = len(fields) == 1
    field = fields[0] if single_field else None

    is_paired = paired_erd is not None
    is_controlling = pair_role in ("controlling", "request")
    is_status = pair_role == "status"

    # Check filter patterns
    name_filtered, filter_pattern = is_filter_match(erd_name)

    # Check if version ERD
    is_version = is_version_erd(fields)
    # Check if clock time ERD
    is_clock_time = is_clock_time_erd(fields)

    # Check for reserved/padding fields
    has_reserved = any("reserved" in f["name"].lower() or "padding" in f["name"].lower() for f in fields)

    # Check for raw fields
    has_raw = any(f["type"] == "raw" for f in fields)

    # Determine filtering
    filtered = False
    filter_reason = None

    # 1. Name matches filter pattern
    if name_filtered:
        filtered = True
        filter_reason = f"Name matches filter pattern: {filter_pattern}"
    # 2. Single field is reserved/padding
    elif single_field and field and ("reserved" in field["name"].lower() or "padding" in field["name"].lower()):
        filtered = True
        filter_reason = "Single field is reserved/padding"
    # 3. Single raw field
    elif single_field and field and field["type"] == "raw":
        filtered = True
        filter_reason = "Single raw field (no semantic meaning)"
    # 4. Multi-field with raw dominating
    elif not single_field and has_raw:
        raw_count = sum(1 for f in fields if f["type"] == "raw")
        non_raw_count = len(fields) - raw_count
        if raw_count > non_raw_count:
            filtered = True
            filter_reason = "Raw fields dominate"

    # 5. Paired status-side ERD (redundant with request side)
    if is_paired and is_status:
        # Check if the request side exists and is not itself filtered
        request_erd = all_erds_by_id.get(paired_erd)
        if request_erd:
            req_name_filtered, _ = is_filter_match(request_erd["name"])
            if not req_name_filtered:
                filtered = True
                filter_reason = "Paired status side - redundant with controllable request side"

    # 6. ERD with ha_domain=None (no valid HA domain)
    if ha_domain is None and not filtered:
        filtered = True
        filter_reason = "ERD has no valid HA domain (ha_domain=None)"

    # 7. Multi-field ERD where all fields are bit-fields or reserved
    if not single_field and not filtered:
        all_bits_or_reserved = all(
            "bits" in f or "reserved" in f["name"].lower()
            for f in fields
        )
        if all_bits_or_reserved:
            filtered = True
            filter_reason = "All fields are bit-fields or reserved (no meaningful data)"

    # Now determine HA domain
    domain = None
    device_class = None
    unit_of_measurement = None
    confidence = "medium"
    reasoning = ""

    if filtered:
        confidence = "low"
        # Still need to determine domain for filtered ERDs
        if single_field and field:
            if field["type"] == "bool":
                domain = "button"  # one-shot
            elif field["type"] == "enum":
                vals = field.get("values", {})
                if vals and len(vals) > 2:
                    domain = "select"
                elif vals and len(vals) == 2 and is_descriptive_enum(field):
                    domain = "select"
                elif vals and len(vals) == 2 and is_on_off_enum(field):
                    domain = "binary_sensor"
                else:
                    domain = "sensor"
            elif field["type"] == "string":
                domain = "sensor"
            elif field["type"] in ("u8", "u16", "u32", "i8", "i16", "i32"):
                domain = "sensor"
            elif field["type"] == "raw":
                domain = None
            else:
                domain = "sensor"
        elif is_paired and is_status:
            # Status side of paired ERD
            request_erd = all_erds_by_id.get(paired_erd)
            if request_erd:
                domain = request_erd.get("ha_domain")
            else:
                domain = "sensor"
        else:
            domain = "sensor"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": True,
            "filter_reason": filter_reason,
            "reasoning": reasoning or f"Filtered ERD: {filter_reason}"
        }

    # Version ERD (4 consecutive u8 at offsets 0-3)
    if is_version:
        domain = "sensor"
        device_class = None
        unit_of_measurement = None
        confidence = "high"
        reasoning = "Version ERD (4 consecutive u8 at offsets 0-3) -> single dotted-version sensor"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Clock time ERD (Hours/Minutes/Seconds at offsets 0,1,2)
    if is_clock_time:
        domain = "sensor"
        device_class = None
        unit_of_measurement = None
        confidence = "high"
        reasoning = "Clock Time ERD (Hours/Minutes/Seconds at offsets 0,1,2) -> single dotted-time sensor"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Multi-field ERD
    if not single_field:
        domain = None
        device_class = None
        unit_of_measurement = None

        # Determine domain from first non-reserved, non-raw field
        for f in fields:
            f_lower = f["name"].lower()
            if "reserved" in f_lower or "padding" in f_lower:
                continue
            if f["type"] == "raw":
                continue
            if f["type"] == "bool":
                domain = "binary_sensor"
                break
            elif f["type"] == "enum":
                vals = f.get("values", {})
                if vals and len(vals) > 2:
                    domain = "select"
                elif vals and len(vals) == 2 and is_descriptive_enum(f):
                    domain = "select"
                elif vals and len(vals) == 2 and is_on_off_enum(f):
                    domain = "binary_sensor"
                else:
                    domain = "sensor"
                break
            elif f["type"] == "string":
                domain = "sensor"
                break
            elif f["type"] in ("u8", "u16", "u32", "i8", "i16", "i32"):
                domain = "sensor"
                break
            else:
                domain = "sensor"
                break

        if domain:
            # Check if any sub-field has temperature
            for f in fields:
                f_lower = f["name"].lower()
                if "reserved" in f_lower or "padding" in f_lower:
                    continue
                if "temperature" in f_lower and f["type"] in ("u8", "u16", "u32", "i8", "i16", "i32"):
                    device_class = "temperature"
                    unit_of_measurement = "°F"
                    break
                if "temperature" in f_lower and f["type"] == "enum":
                    device_class = "temperature"
                    break

        confidence = "medium"
        reasoning = f"Multi-field ERD ({len(fields)} fields). Domain from first non-reserved field: {domain or 'none'}"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Single-field ERD
    if not field:
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": None,
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "low",
            "filtered": False,
            "filter_reason": None,
            "reasoning": "No data fields"
        }

    field_type = field["type"]
    field_name = field["name"]
    field_name_lower = field_name.lower()

    # Bool type
    if field_type == "bool":
        has_write = "write" in operations
        has_read = "read" in operations

        if has_write and not has_read:
            domain = "button"
            device_class = "restart" if any(kw in field_name_lower for kw in ["reset", "restart", "reboot"]) else None
            confidence = "high"
            reasoning = "Bool write-only -> button (one-shot command)"
        elif has_write and has_read:
            domain = "switch"
            device_class = None
            confidence = "high"
            reasoning = "Bool writable -> switch"
        elif is_paired:
            if is_controlling:
                domain = "switch"
                device_class = None
                confidence = "high"
                reasoning = "Bool paired (controlling) -> switch"
            elif is_status:
                domain = "binary_sensor"
                device_class = None
                confidence = "high"
                reasoning = "Bool paired (status) -> binary_sensor"
        else:
            domain = "binary_sensor"
            device_class = None
            confidence = "high"
            reasoning = "Bool read-only -> binary_sensor"

        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Enum type
    if field_type == "enum":
        vals = field.get("values", {})
        num_vals = len(vals)

        has_write = "write" in operations
        has_read = "read" in operations

        if num_vals == 0:
            domain = "sensor"
            device_class = None
            confidence = "medium"
            reasoning = "Enum without values -> sensor"
            return {
                "id": erd_id,
                "name": erd_name,
                "ha_domain": domain,
                "device_class": device_class,
                "unit_of_measurement": unit_of_measurement,
                "confidence": confidence,
                "filtered": False,
                "filter_reason": None,
                "reasoning": reasoning
            }

        if has_write:
            if num_vals == 2 and is_on_off_enum(field):
                domain = "switch"
                device_class = None
                confidence = "high"
                reasoning = "2-value On/Off enum writable -> switch"
            elif num_vals == 2 and is_descriptive_enum(field):
                domain = "select"
                device_class = "enum"
                confidence = "high"
                reasoning = "2-value descriptive enum writable -> select"
            elif num_vals > 2:
                domain = "select"
                device_class = "enum"
                confidence = "high"
                reasoning = "Multi-value enum writable -> select"
            else:
                domain = "select"
                device_class = "enum"
                confidence = "medium"
                reasoning = "Enum writable -> select"
        else:
            if num_vals == 2 and is_on_off_enum(field):
                domain = "binary_sensor"
                device_class = None
                confidence = "high"
                reasoning = "2-value On/Off enum read-only -> binary_sensor"
            elif num_vals == 2 and is_descriptive_enum(field):
                domain = "sensor"
                device_class = "enum"
                confidence = "high"
                reasoning = "2-value descriptive enum read-only -> sensor+enum"
            elif num_vals > 2:
                domain = "sensor"
                device_class = "enum"
                confidence = "high"
                reasoning = "Multi-value enum read-only -> sensor+enum"
            else:
                domain = "sensor"
                device_class = "enum"
                confidence = "medium"
                reasoning = "Enum read-only -> sensor+enum"

        unit_of_measurement = detect_unit_from_name(field_name_lower)
        if domain == "sensor" and device_class is None:
            device_class = detect_device_class_from_name(field_name_lower, domain, field_type)

        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # String type
    if field_type == "string":
        domain = "sensor"
        device_class = None
        confidence = "high"
        reasoning = "String type -> sensor"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Numeric types
    if field_type in ("u8", "u16", "u32", "i8", "i16", "i32"):
        has_write = "write" in operations
        has_read = "read" in operations

        if has_write:
            domain = "number"
            device_class = detect_device_class_from_name(field_name_lower, domain, field_type)
            unit_of_measurement = detect_unit_from_name(field_name_lower)
            confidence = "high"
            reasoning = "Numeric writable -> number"
        else:
            domain = "sensor"
            device_class = detect_device_class_from_name(field_name_lower, domain, field_type)
            unit_of_measurement = detect_unit_from_name(field_name_lower)
            confidence = "high"
            reasoning = "Numeric read-only -> sensor"

        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": False,
            "filter_reason": None,
            "reasoning": reasoning
        }

    # Raw type
    if field_type == "raw":
        domain = None
        device_class = None
        confidence = "low"
        reasoning = "Raw type (no semantic meaning)"
        return {
            "id": erd_id,
            "name": erd_name,
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit_of_measurement,
            "confidence": confidence,
            "filtered": True,
            "filter_reason": "Raw type field",
            "reasoning": reasoning
        }

    # Fallback
    domain = "sensor"
    confidence = "low"
    reasoning = f"Unknown field type: {field_type}"
    return {
        "id": erd_id,
        "name": erd_name,
        "ha_domain": domain,
        "device_class": device_class,
        "unit_of_measurement": unit_of_measurement,
        "confidence": confidence,
        "filtered": False,
        "filter_reason": None,
        "reasoning": reasoning
    }


def main():
    all_reviews = []
    batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "batch_*.json")))

    # Load all ERDs to build lookup for paired_erd resolution
    all_erds = {}
    for bf in batch_files:
        with open(bf) as f:
            data = json.load(f)
        for erd in data:
            all_erds[erd["id"]] = erd

    for bf in batch_files:
        with open(bf) as f:
            data = json.load(f)
        for erd in data:
            review = review_erd(erd, all_erds)
            all_reviews.append(review)

    # Sort by ID for consistency
    all_reviews.sort(key=lambda x: x["id"])

    with open(OUTPUT, "w") as f:
        json.dump(all_reviews, f, indent=2, ensure_ascii=False)

    print(f"Reviewed {len(all_reviews)} ERDs -> {OUTPUT}")

    # Summary stats
    domains = {}
    filtered_count = 0
    for r in all_reviews:
        d = r["ha_domain"] or "none"
        domains[d] = domains.get(d, 0) + 1
        if r["filtered"]:
            filtered_count += 1

    print(f"\nDomain distribution:")
    for d in sorted(domains):
        print(f"  {d}: {domains[d]}")
    print(f"\nFiltered: {filtered_count}")
    print(f"Not filtered: {len(all_reviews) - filtered_count}")


if __name__ == "__main__":
    main()