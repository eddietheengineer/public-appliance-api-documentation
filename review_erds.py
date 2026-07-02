#!/usr/bin/env python3
"""Review all ERDs from batch files and produce subagent_review_b.json."""

import json
import re
import os
from datetime import datetime, timezone

BATCH_DIR = "/home/joshua/public-appliance-api-documentation"
OUTPUT = os.path.join(BATCH_DIR, "subagent_review_b.json")

# --- Filter patterns (from AGENTS.md + erd_rules.md) ---
# These are applied to ERD names to determine if they should be filtered.
# Order matters: more specific patterns first.

def should_filter(name):
    """Check if ERD name matches a filter pattern. Returns (reason, pattern) or None."""
    n = name.lower()

    # Diagnostics
    if re.search(r'diagnostic', n):
        return ("diagnostic", "diagnostic")
    if re.search(r'fault', n):
        return ("fault", "fault")
    if re.search(r'reset\s+reason', n):
        return ("reset reason", "reset\\s+reason")
    if re.search(r'program\s+counter', n):
        return ("program counter", "program\\s+counter")
    if re.search(r'fault\s+code', n):
        return ("fault code", "fault\\s+code")
    if re.search(r'linux\s+diagnostics', n):
        return ("linux diagnostics", "linux\\s+diagnostics")

    # Firmware
    if re.search(r'configuration\s+hash', n):
        return ("configuration hash", "configuration\\s+hash")
    if re.search(r'schedule\s+hash', n):
        return ("schedule hash", "schedule\\s+hash")
    if re.search(r'sha[-\s]?256', n):
        return ("SHA-256", "sha[-\\s]?256")
    if re.search(r'boot\s+loader', n):
        return ("boot loader version", "boot\\s+loader\\s+version")
    if re.search(r'supported\s+image\s+types', n):
        return ("supported image types", "supported\\s+image\\s+types")
    if re.search(r'engineering\s+revision', n):
        return ("engineering revision", "engineering\\s+revision")
    if re.search(r'engineering\s+snapshot', n):
        return ("engineering snapshot", "engineering\\s+snapshot")
    if re.search(r'application\s+version', n):
        return ("application version", "application\\s+version")
    if re.search(r'parametric\s+version', n):
        return ("parametric version", "parametric\\s+version")
    if re.search(r'auxiliary\s+version', n):
        return ("auxiliary version", "auxiliary\\s+version")
    if re.search(r'mainboard\s+application\s+version', n):
        return ("mainboard application version", "mainboard\\s+application\\s+version")
    if re.search(r'temperature\s+board\s+application\s+version', n):
        return ("temperature board application version", "temperature\\s+board\\s+application\\s+version")
    if re.search(r'dispenser\s+board\s+application\s+version', n):
        return ("dispenser board application version", "dispenser\\s+board\\s+application\\s+version")
    if re.search(r'door\s+board\s+application\s+version', n):
        return ("door board application version", "door\\s+board\\s+application\\s+version")
    if re.search(r'deli-?pan\s+board\s+application\s+version', n):
        return ("deli-pan board application version", "deli-?pan\\s+board\\s+application\\s+version")
    if re.search(r'wifi\s+zigbee\s+board\s+application\s+version', n):
        return ("wifi zigbee board application version", "wifi\\s+zigbee\\s+board\\s+application\\s+version")
    if re.search(r'auto-fill\s+board\s+application\s+version', n):
        return ("auto-fill board application version", "auto-fill\\s+board\\s+application\\s+version")
    if re.search(r'feature\s+board\s+application\s+version', n):
        return ("feature board application version", "feature\\s+board\\s+application\\s+version")
    if re.search(r'rfid\s+board\s+application\s+version', n):
        return ("rfid board application version", "rfid\\s+board\\s+application\\s+version")
    if re.search(r'feature\s+pan\s+board\s+application\s+version', n):
        return ("feature pan board application version", "feature\\s+pan\\s+board\\s+application\\s+version")
    if re.search(r'autofill\s+pitcher\s+board\s+application\s+version', n):
        return ("autofill pitcher board application version", "autofill\\s+pitcher\\s+board\\s+application\\s+version")
    if re.search(r'convertible\s+drawer\s+ui\s+board\s+application\s+version', n):
        return ("convertible drawer ui board application version", "convertible\\s+drawer\\s+ui\\s+board\\s+application\\s+version")
    if re.search(r'ready\s+to\s+enter\s+boot', n):
        return ("ready to enter boot loader", "ready\\s+to\\s+enter\\s+boot")
    if re.search(r'reset\s+board', n):
        return ("reset board", "reset\\s+board")
    if re.search(r'personality', n):
        return ("personality", "personality")
    if re.search(r'notifications', n) and 'supported' not in n:
        return ("notifications", "notifications")
    if re.search(r'water\s+heater\s+reset\s+information', n):
        return ("water heater reset information", "water\\s+heater\\s+reset\\s+information")
    if re.search(r'recipe\s+status', n):
        return ("recipe status", "recipe\\s+status")
    if re.search(r'menu\s+tree\s+parametric\s+hash', n):
        return ("menu tree parametric hash", "menu\\s+tree\\s+parametric\\s+hash")
    if re.search(r'camera\s+configuration\s+personality', n):
        return ("camera configuration personality", "camera\\s+configuration\\s+personality")

    # Commissioning
    if re.search(r'matter', n):
        return ("matter", "matter")
    if re.search(r'alexa', n):
        return ("alexa", "alexa")
    if re.search(r'voice\s+module', n):
        return ("voice module", "voice\\s+module")
    if re.search(r'onboarding', n):
        return ("onboarding", "onboarding")
    if re.search(r'pairing\s+code', n):
        return ("pairing code", "pairing\\s+code")
    if re.search(r'commissioning', n):
        return ("commissioning", "commissioning")

    # Service mode
    if re.search(r'service\s+mode', n):
        return ("service mode", "service\\s+mode")
    if re.search(r'service\s+mode\s+electric\s+room\s+heater', n):
        return ("service mode electric room heater", "service\\s+mode\\s+electric\\s+room\\s+heater")

    # Sabbath mode (redundant)
    if re.search(r'enhanced\s+sabbath', n):
        return ("enhanced sabbath mode", "enhanced\\s+sabbath")

    # Push notifications
    if re.search(r'push\s+notification', n):
        return ("push notification", "push\\s+notification")

    # Availability/allowability
    if re.search(r'available\s+connect\s+cycles', n):
        return ("available connect cycles", "available")
    if re.search(r'available\s+sound\s+levels', n):
        return ("available sound levels", "available")
    if re.search(r'available\s+modes', n):
        return ("available modes", "available")
    if re.search(r'available\s+ac\s+modes', n):
        return ("available AC modes", "available")
    if re.search(r'available\s+fan\s+speeds', n):
        return ("available fan speeds", "available")
    if re.search(r'available\s+color\s+schemes', n):
        return ("available color schemes", "available")
    if re.search(r'available\s+demand\s+response', n):
        return ("available demand response", "available")
    if re.search(r'available\s+select', n):
        return ("available select", "available")
    if re.search(r'available\s+connect', n):
        return ("available connect", "available")
    if re.search(r'available\s+options', n):
        return ("available options", "available")
    if re.search(r'available\s+cycle', n):
        return ("available cycle", "available")
    if re.search(r'available\s+light', n):
        return ("available light", "available")
    if re.search(r'available\s+fan', n):
        return ("available fan", "available")
    if re.search(r'available\s+modes', n):
        return ("available modes", "available")
    if re.search(r'available\s+ac', n):
        return ("available AC", "available")
    if re.search(r'available\s+color', n):
        return ("available color", "available")
    if re.search(r'available\s+demand', n):
        return ("available demand", "available")
    if re.search(r'available\s+fan', n):
        return ("available fan", "available")
    if re.search(r'available\s+select', n):
        return ("available select", "available")
    if re.search(r'available\s+connect', n):
        return ("available connect", "available")
    if re.search(r'available\s+cycle', n):
        return ("available cycle", "available")
    if re.search(r'available\s+light', n):
        return ("available light", "available")
    if re.search(r'modification\s+available', n):
        return ("modification available", "modification\\s+available")
    if re.search(r'action\s+available', n):
        return ("action available", "action\\s+available")
    if re.search(r'allowable', n):
        return ("allowable", "allowable")
    if re.search(r'allowed', n):
        return ("allowed", "allowed")
    if re.search(r'available', n):
        return ("available", "available")

    # Supported features
    if re.search(r'supported\s+feature', n):
        return ("supported feature", "supported\\s+feature")
    if re.search(r'supported\s+state', n):
        return ("supported state", "supported\\s+state")
    if re.search(r'supported\s+equipment', n):
        return ("supported equipment", "supported\\s+equipment")
    if re.search(r'supported\s+sound', n):
        return ("supported sound themes", "supported\\s+sound")
    if re.search(r'supported\s+brew', n):
        return ("supported brew", "supported\\s+brew")
    if re.search(r'supported\s+cook', n):
        return ("supported cook", "supported\\s+cook")
    if re.search(r'supported\s+notification', n):
        return ("supported notification", "supported\\s+notification")
    if re.search(r'supported\s+device', n):
        return ("supported device", "supported\\s+device")
    if re.search(r'supported\s+states', n):
        return ("supported states", "supported\\s+states")

    # Clock/time
    if re.search(r'clock\s+time', n):
        return ("clock time", "clock\\s+time")
    if re.search(r'clock\s+format', n):
        return ("clock format", "clock\\s+format")
    if re.search(r'clock\s+display', n):
        return ("clock display", "clock\\s+display")
    if re.search(r'ntp', n):
        return ("ntp", "ntp")
    if re.search(r'time\s+zone', n):
        return ("time zone", "time\\s+zone")
    if re.search(r'daylight\s+saving', n):
        return ("daylight saving", "daylight\\s+saving")

    # Network
    if re.search(r'wifi\s+status', n):
        return ("wifi status", "wifi\\s+status")
    if re.search(r'signal\s+strength', n):
        return ("signal strength", "signal\\s+strength")
    if re.search(r'ble\s+master', n):
        return ("ble master", "ble\\s+master")
    if re.search(r'wireless\s+connection', n):
        return ("wireless connection", "wireless\\s+connection")

    # Energy pricing
    if re.search(r'electrical\s+pricing', n):
        return ("electrical pricing", "electrical\\s+pricing")
    if re.search(r'demand\s+response', n):
        return ("demand response", "demand\\s+response")
    if re.search(r'time\s+of\s+use', n):
        return ("time of use", "time\\s+of\\s+use")

    # Camera
    if re.search(r'still\s+frame', n):
        return ("still frame", "still\\s+frame")
    if re.search(r'image\s+upload', n):
        return ("image upload", "image\\s+upload")
    if re.search(r'image\s+capture', n):
        return ("image capture", "image\\s+capture")
    if re.search(r'camera\s+stream', n):
        return ("camera stream", "camera\\s+stream")
    if re.search(r'camera\s+configuration', n):
        return ("camera configuration", "camera\\s+configuration")

    # Sound
    if re.search(r'sound\s+level', n):
        return ("sound level", "sound\\s+level")
    if re.search(r'sound\s+theme', n):
        return ("sound theme", "sound\\s+theme")

    # Usage profile
    if re.search(r'usage\s+profile', n):
        return ("usage profile", "usage\\s+profile")

    # Current report
    if re.search(r'current\s+report', n):
        return ("current report", "current\\s+report")

    # Feature configuration
    if re.search(r'feature\s+configuration', n):
        return ("feature configuration", "feature\\s+configuration")

    # Cycle definitions
    if re.search(r'cycle\s+definition', n):
        return ("cycle definition", "cycle\\s+definition")

    # Latched key
    if re.search(r'latched\s+key', n):
        return ("latched key", "latched\\s+key")

    # DIP switch
    if re.search(r'dip\s+switch', n):
        return ("dip switch", "dip\\s+switch")

    # Most recent cycle
    if re.search(r'most\s+recent\s+cycle', n):
        return ("most recent cycle", "most\\s+recent\\s+cycle")

    # Unused/reserved
    if re.search(r'unused', n):
        return ("unused", "unused")
    if re.search(r'reserved', n):
        return ("reserved", "reserved")

    # Operational errors
    if re.search(r'issue', n):
        return ("issue", "issue")
    if re.search(r'failure', n):
        return ("failure", "failure")

    # Temperature display units (redundant)
    if re.search(r'temperature\s+display\s+units', n):
        return ("temperature display units", "temperature\\s+display\\s+units")

    # User interface locked (redundant)
    if re.search(r'user\s+interface\s+locked', n):
        return ("user interface locked", "user\\s+interface\\s+locked")

    return None


def is_clock_time(data_fields):
    """Detect clock time ERDs: Hours/Minutes/Seconds at offsets 0,1,2."""
    if len(data_fields) != 3:
        return False
    offsets = [f.get("offset", -1) for f in data_fields]
    types = [f.get("type", "") for f in data_fields]
    if offsets != [0, 1, 2]:
        return False
    if types != ["u8", "u8", "u8"]:
        return False
    names_lower = [f.get("name", "").lower() for f in data_fields]
    has_hour = any("hour" in n for n in names_lower)
    has_minute = any("minute" in n for n in names_lower)
    has_second = any("second" in n for n in names_lower)
    return has_hour and has_minute and has_second


def is_version_erd(data_fields):
    """Detect version ERDs: Critical Major/Minor + Non-Critical Major/Minor at offsets 0-3."""
    if len(data_fields) != 4:
        return False
    offsets = [f.get("offset", -1) for f in data_fields]
    types = [f.get("type", "") for f in data_fields]
    if offsets != [0, 1, 2, 3]:
        return False
    if types != ["u8", "u8", "u8", "u8"]:
        return False
    names_lower = [f.get("name", "").lower() for f in data_fields]
    has_major = any("major" in n for n in names_lower)
    has_minor = any("minor" in n for n in names_lower)
    return has_major and has_minor


def is_multi_field(data_fields):
    return len(data_fields) > 1


def is_paired(erd):
    return "paired_erd" in erd


def get_enum_values(data_fields):
    all_values = []
    for f in data_fields:
        if f.get("type") == "enum" and "values" in f:
            all_values.extend(f["values"].values())
    return all_values


def get_unit_from_name(name):
    """Extract unit of measurement from field name."""
    n = name.lower()
    if "°f" in name or "fahrenheit" in n:
        return "°F"
    if "°c" in name or "celsius" in n:
        return "°C"
    if "voltage" in n:
        return "V"
    if "current" in n:
        return "A"
    if "watt" in n:
        return "W"
    if "kwh" in n:
        return "kWh"
    if "min" in n:
        return "min"
    if " h " in name or " hour" in n:
        return "h"
    if " s " in name or " second" in n:
        return "s"
    if "rpm" in n:
        return "rpm"
    if "cfm" in n:
        return "CFM"
    if "gal" in n:
        return "gal"
    if "lx" in n:
        return "lx"
    if "hpa" in n:
        return "hPa"
    if "%" in name:
        return "%"
    return None


def get_device_class_from_name(name):
    """Extract device_class from field name."""
    n = name.lower()
    if "temperature" in n:
        return "temperature"
    if "voltage" in n:
        return "voltage"
    if "current" in n:
        return "current"
    if "power" in n:
        return "power"
    if "energy" in n:
        return "energy"
    if "humidity" in n:
        return "humidity"
    if "pressure" in n:
        return "pressure"
    if "illuminance" in n:
        return "illuminance"
    if "distance" in n:
        return "distance"
    if "battery" in n:
        if "charging" in n:
            return "battery_charging"
        return "battery"
    if "door" in n:
        return "door"
    if "moisture" in n:
        return "moisture"
    if "plug" in n:
        return "plug"
    return None


def determine_domain_and_metadata(erd):
    """Determine HA domain, device_class, unit_of_measurement for an ERD."""
    name = erd.get("name", "")
    data_fields = erd.get("data", [])
    operations = erd.get("operations", [])
    field_type = data_fields[0].get("type") if data_fields else None
    has_write = "write" in operations
    has_read = "read" in operations
    paired_flag = "paired_erd" in erd

    # Check filter patterns first
    filter_result = should_filter(name)
    if filter_result:
        reason, pattern = filter_result
        return {
            "ha_domain": None,
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "low",
            "filtered": True,
            "filter_reason": reason,
            "reasoning": f"Filtered: {reason}"
        }

    # Clock time ERD
    if is_clock_time(data_fields):
        return {
            "ha_domain": "sensor",
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "high",
            "filtered": False,
            "filter_reason": None,
            "reasoning": "Clock Time (Hours/Minutes/Seconds) → single dotted-time sensor"
        }

    # Version ERD
    if is_version_erd(data_fields):
        return {
            "ha_domain": "sensor",
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "high",
            "filtered": False,
            "filter_reason": None,
            "reasoning": "Version ERD (4 u8 fields) → single dotted-version sensor"
        }

    # Multi-field ERD
    if is_multi_field(data_fields):
        # Determine domain from first non-reserved field
        primary_field = None
        for f in data_fields:
            fname = f.get("name", "").lower()
            if "reserved" not in fname and "padding" not in fname:
                primary_field = f
                break

        if primary_field is None:
            return {
                "ha_domain": None,
                "device_class": None,
                "unit_of_measurement": None,
                "confidence": "low",
                "filtered": True,
                "filter_reason": "reserved",
                "reasoning": "Multi-field ERD with only reserved/padding fields"
            }

        ptype = primary_field.get("type")
        pname = primary_field.get("name", "")

        # Determine domain from primary field type
        if ptype == "bool":
            domain = "switch" if (has_write or paired_flag) else "binary_sensor"
        elif ptype == "enum":
            enum_vals = get_enum_values(data_fields)
            if len(enum_vals) <= 2:
                descriptive = any(
                    v.lower() not in ("on", "off", "enable", "disable", "enabled", "disabled")
                    for v in enum_vals
                )
                if descriptive and (has_write or paired_flag):
                    domain = "select"
                elif descriptive:
                    domain = "sensor"
                elif has_write or paired_flag:
                    domain = "switch"
                else:
                    domain = "binary_sensor"
            else:
                if has_write or paired_flag:
                    domain = "select"
                else:
                    domain = "sensor"
        elif ptype in ("u8", "u16", "u32", "i8", "i16", "i32"):
            domain = "number" if (has_write or paired_flag) else "sensor"
        elif ptype == "string":
            domain = "sensor"
        else:
            domain = "sensor"

        # Multi-field: no device_class at ERD level
        return {
            "ha_domain": domain,
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "medium",
            "filtered": False,
            "filter_reason": None,
            "reasoning": f"Multi-field ERD, primary type={ptype}, domain={domain}"
        }

    # Single-field ERDs
    if field_type == "bool":
        if has_write or paired_flag:
            return {
                "ha_domain": "switch",
                "device_class": None,
                "unit_of_measurement": None,
                "confidence": "high",
                "filtered": False,
                "filter_reason": None,
                "reasoning": "Bool writable → switch"
            }
        return {
            "ha_domain": "binary_sensor",
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "high",
            "filtered": False,
            "filter_reason": None,
            "reasoning": "Bool read-only → binary_sensor"
        }

    elif field_type == "enum":
        enum_vals = get_enum_values(data_fields)
        num_vals = len(enum_vals)

        if num_vals == 0:
            return {
                "ha_domain": "sensor",
                "device_class": None,
                "unit_of_measurement": None,
                "confidence": "medium",
                "filtered": False,
                "filter_reason": None,
                "reasoning": "Enum with no values → sensor"
            }

        if num_vals == 1:
            return {
                "ha_domain": "sensor",
                "device_class": "enum",
                "unit_of_measurement": None,
                "confidence": "high",
                "filtered": False,
                "filter_reason": None,
                "reasoning": "Single-value enum → sensor with device_class:enum"
            }

        val_labels = [v.lower() for v in enum_vals]
        is_on_off = (
            ("on" in val_labels and "off" in val_labels) or
            ("enable" in val_labels and "disable" in val_labels) or
            ("enabled" in val_labels and "disabled" in val_labels)
        )

        if num_vals == 2:
            if is_on_off:
                if has_write or paired_flag:
                    return {
                        "ha_domain": "switch",
                        "device_class": None,
                        "unit_of_measurement": None,
                        "confidence": "high",
                        "filtered": False,
                        "filter_reason": None,
                        "reasoning": "2-value On/Off enum → switch"
                    }
                else:
                    return {
                        "ha_domain": "binary_sensor",
                        "device_class": None,
                        "unit_of_measurement": None,
                        "confidence": "high",
                        "filtered": False,
                        "filter_reason": None,
                        "reasoning": "2-value On/Off enum → binary_sensor"
                    }
            else:
                if has_write or paired_flag:
                    return {
                        "ha_domain": "select",
                        "device_class": None,
                        "unit_of_measurement": None,
                        "confidence": "high",
                        "filtered": False,
                        "filter_reason": None,
                        "reasoning": "2-value descriptive enum → select"
                    }
                else:
                    return {
                        "ha_domain": "sensor",
                        "device_class": "enum",
                        "unit_of_measurement": None,
                        "confidence": "high",
                        "filtered": False,
                        "filter_reason": None,
                        "reasoning": "2-value descriptive enum → sensor+device_class:enum"
                    }
        else:
            if has_write or paired_flag:
                return {
                    "ha_domain": "select",
                    "device_class": None,
                    "unit_of_measurement": None,
                    "confidence": "high",
                    "filtered": False,
                    "filter_reason": None,
                    "reasoning": f"{num_vals}-value enum → select"
                }
            else:
                return {
                    "ha_domain": "sensor",
                    "device_class": "enum",
                    "unit_of_measurement": None,
                    "confidence": "high",
                    "filtered": False,
                    "filter_reason": None,
                    "reasoning": f"{num_vals}-value enum → sensor+device_class:enum"
                }

    elif field_type in ("u8", "u16", "u32", "i8", "i16", "i32"):
        device_class = get_device_class_from_name(name)
        unit = get_unit_from_name(name)

        if has_write or paired_flag:
            domain = "number"
            # number domain: almost NEVER device_class (except temperature)
            if device_class and device_class != "temperature":
                device_class = None
        else:
            domain = "sensor"

        return {
            "ha_domain": domain,
            "device_class": device_class,
            "unit_of_measurement": unit,
            "confidence": "high" if device_class else "medium",
            "filtered": False,
            "filter_reason": None,
            "reasoning": f"{field_type} numeric {'writable' if has_write or paired_flag else 'read-only'} → {domain}"
        }

    elif field_type == "string":
        return {
            "ha_domain": "sensor",
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "high",
            "filtered": False,
            "filter_reason": None,
            "reasoning": "String type → sensor"
        }

    elif field_type == "raw":
        return {
            "ha_domain": None,
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "low",
            "filtered": True,
            "filter_reason": "raw type field",
            "reasoning": "Raw bytes with no semantic meaning → filtered"
        }

    else:
        return {
            "ha_domain": None,
            "device_class": None,
            "unit_of_measurement": None,
            "confidence": "low",
            "filtered": True,
            "filter_reason": f"unknown type: {field_type}",
            "reasoning": f"Unknown field type: {field_type}"
        }


def process_erd(erd):
    result = determine_domain_and_metadata(erd)
    return {
        "id": erd.get("id", ""),
        "name": erd.get("name", ""),
        "ha_domain": result["ha_domain"],
        "device_class": result["device_class"],
        "unit_of_measurement": result["unit_of_measurement"],
        "confidence": result["confidence"],
        "filtered": result["filtered"],
        "filter_reason": result["filter_reason"],
        "reasoning": result["reasoning"]
    }


def main():
    all_reviews = []
    batch_files = sorted([
        f for f in os.listdir(BATCH_DIR)
        if f.startswith("batch_") and f.endswith(".json")
    ])

    for batch_file in batch_files:
        filepath = os.path.join(BATCH_DIR, batch_file)
        with open(filepath) as f:
            erds = json.load(f)

        for erd in erds:
            review = process_erd(erd)
            all_reviews.append(review)

    print(f"Total reviews: {len(all_reviews)}")

    # Statistics
    domains = {}
    filtered_count = 0
    for r in all_reviews:
        d = r["ha_domain"] or "none"
        domains[d] = domains.get(d, 0) + 1
        if r["filtered"]:
            filtered_count += 1

    print(f"Filtered: {filtered_count}")
    print(f"Domains: {domains}")

    with open(OUTPUT, "w") as f:
        json.dump(all_reviews, f, indent=2)

    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()