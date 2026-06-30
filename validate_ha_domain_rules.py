#!/usr/bin/env python3
"""
Validate that ERD metadata follows Home Assistant domain-specific rules.
Based on Home Assistant core source code validation logic.

Exits with code 1 and prints errors if any violations are found.
"""

import json
import os
import sys
from pathlib import Path

IN_GITHUB_ACTIONS = os.environ.get('GITHUB_ACTIONS') == 'true'


def emit_error(message: str, file: str = "", line: int = 0) -> None:
    """Emit an error message, using GitHub Actions annotation format if in CI."""
    if IN_GITHUB_ACTIONS:
        if file and line:
            print(f"::error file={file},line={line}::{message}")
        else:
            print(f"::error::{message}")
    else:
        print(f"  ERROR: {message}")


# Valid device classes for binary_sensor
BINARY_SENSOR_DEVICE_CLASSES = {
    'battery', 'battery_charging', 'carbon_monoxide', 'cold',
    'connectivity', 'door', 'garage_door', 'gas', 'heat',
    'light', 'lock', 'moisture', 'motion', 'moving',
    'occupancy', 'opening', 'plug', 'power', 'presence',
    'problem', 'running', 'safety', 'smoke', 'sound',
    'tamper', 'update', 'vibration', 'window',
}

# Sensor device classes that are non-numeric (cannot have unit_of_measurement or state_class)
SENSOR_NON_NUMERIC_DEVICE_CLASSES = {'date', 'enum', 'timestamp', 'uptime'}

# Valid units for each sensor device_class (from HA DEVICE_CLASS_UNITS)
SENSOR_DEVICE_CLASS_UNITS = {
    'absolute_humidity': {'g/m³', 'mg/m³'},
    'apparent_power': {'mVA', 'VA', 'kVA'},
    'aqi': {None},
    'area': {'mm²', 'cm²', 'm²', 'km²', 'in²', 'ft²', 'yd²', 'mi²'},
    'atmospheric_pressure': {'Pa', 'hPa', 'kPa', 'bar', 'cbar', 'mbar', 'mmHg', 'inHg', 'psi'},
    'battery': {'%'},
    'blood_glucose_concentration': {'mg/dL', 'mmol/L'},
    'carbon_monoxide': {'ppb', 'ppm', 'mg/m³', 'μg/m³'},
    'carbon_dioxide': {'ppm'},
    'conductivity': {'S/cm', 'mS/cm', 'μS/cm'},
    'current': {'A', 'mA', 'μA'},
    'data_rate': {'bit/s', 'kB/s', 'KB/s', 'MB/s', 'GB/s', 'TB/s', 'Mbit/s', 'Gbit/s', 'Tbit/s', 'kbit/s'},
    'data_size': {'bit', 'kbit', 'Mbit', 'Gbit', 'Tbit', 'B', 'kB', 'KB', 'MB', 'GB', 'TB', 'KiB', 'MiB', 'GiB', 'TiB'},
    'distance': {'mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi'},
    'duration': {'d', 'h', 'min', 's', 'ms', 'μs'},
    'energy': {'J', 'kJ', 'MJ', 'GJ', 'mWh', 'Wh', 'kWh', 'MWh', 'GWh', 'TWh', 'cal', 'kcal', 'Mcal', 'Gcal'},
    'energy_distance': {'kWh/100km', 'Wh/km', 'mi/kWh', 'km/kWh'},
    'energy_storage': {'J', 'kJ', 'MJ', 'GJ', 'mWh', 'Wh', 'kWh', 'MWh', 'GWh', 'TWh', 'cal', 'kcal', 'Mcal', 'Gcal'},
    'frequency': {'mHz', 'Hz', 'kHz', 'MHz', 'GHz'},
    'gas': {'CCF', 'ft³', 'm³', 'L', 'MCF'},
    'humidity': {'%'},
    'illuminance': {'lx'},
    'irradiance': {'W/m²', 'BTU/(h⋅ft²)'},
    'moisture': {'%'},
    'monetary': {'EUR', 'USD', 'GBP', 'JPY', 'CNY', 'INR', 'RUB', 'BRL', 'MXN', 'KRW', 'AUD', 'CAD', 'CHF', 'HKD', 'SGD', 'SEK', 'NOK', 'DKK', 'PLN', 'CZK', 'HUF', 'ILS', 'CLP', 'ARS', 'COP', 'PEN', 'UYU', 'VEF', 'VES', 'BOB', 'PYG', 'DOP', 'CRC', 'NIO', 'GTQ', 'PAB', 'CUP', 'HTG', 'HNL', 'JMD', 'TTD', 'BBD', 'XCD', 'AWG', 'ANG', 'GYD', 'SRD', 'BMD', 'KYD', 'BZD', 'BSD', 'BBD', 'XCD', 'DOP', 'HTG', 'JMD', 'TTD', 'BBD', 'XCD', 'AWG', 'ANG', 'GYD', 'SRD', 'BMD', 'KYD', 'BZD', 'BSD'},
    'nitrogen_dioxide': {'ppb', 'ppm', 'μg/m³'},
    'nitrogen_monoxide': {'ppb', 'μg/m³'},
    'nitrous_oxide': {'μg/m³'},
    'ozone': {'ppb', 'ppm', 'μg/m³'},
    'ph': {None},
    'pm1': {'μg/m³'},
    'pm10': {'μg/m³'},
    'pm25': {'μg/m³'},
    'pm4': {'μg/m³'},
    'power': {'mW', 'W', 'kW', 'MW', 'GW', 'TW', 'BTU/h'},
    'power_factor': {'%', None},
    'precipitation': {'mm', 'cm', 'in'},
    'precipitation_intensity': {'mm/d', 'mm/h', 'in/d', 'in/h'},
    'pressure': {'Pa', 'hPa', 'kPa', 'bar', 'cbar', 'mbar', 'mmHg', 'inHg', 'psi', 'inH₂O'},
    'reactive_energy': {'varh', 'kvarh'},
    'reactive_power': {'mvar', 'var', 'kvar'},
    'signal_strength': {'dB', 'dBm'},
    'sound_pressure': {'dB', 'dBA'},
    'speed': {'mm/d', 'mm/h', 'm/s', 'km/h', 'mm/s', 'in/d', 'in/h', 'in/s', 'ft/s', 'mph', 'kn', 'Beaufort'},
    'sulphur_dioxide': {'ppb', 'ppm', 'μg/m³'},
    'temperature': {'°C', '°F', 'K'},
    'temperature_delta': {'°C', '°F', 'K'},
    'volatile_organic_compounds': {'μg/m³', 'mg/m³'},
    'volatile_organic_compounds_parts': {'ppb', 'ppm'},
    'voltage': {'V', 'mV', 'μV', 'kV', 'MV'},
    'volume': {'mL', 'L', 'm³', 'ft³', 'CCF', 'MCF', 'fl. oz.', 'gal'},
    'volume_storage': {'mL', 'L', 'm³', 'ft³', 'CCF', 'MCF', 'fl. oz.', 'gal'},
    'volume_flow_rate': {'m³/h', 'm³/min', 'm³/s', 'L/h', 'L/min', 'L/s', 'mL/s', 'ft³/min', 'gal/min', 'gal/d'},
    'water': {'CCF', 'ft³', 'm³', 'L', 'MCF', 'gal'},
    'weight': {'μg', 'mg', 'g', 'kg', 'oz', 'lb'},
    'wind_direction': {'°'},
    'wind_speed': {'m/s', 'km/h', 'ft/s', 'mph', 'kn', 'Beaufort'},
}

# Valid state_classes for each sensor device_class (from HA DEVICE_CLASS_STATE_CLASSES)
SENSOR_DEVICE_CLASS_STATE_CLASSES = {
    'absolute_humidity': {'measurement'},
    'apparent_power': {'measurement'},
    'aqi': {'measurement'},
    'area': {'measurement', 'total', 'total_increasing'},
    'atmospheric_pressure': {'measurement'},
    'battery': {'measurement'},
    'blood_glucose_concentration': {'measurement'},
    'carbon_monoxide': {'measurement'},
    'carbon_dioxide': {'measurement'},
    'conductivity': {'measurement'},
    'current': {'measurement'},
    'data_rate': {'measurement'},
    'data_size': {'measurement', 'total', 'total_increasing'},
    'date': set(),
    'distance': {'measurement', 'total', 'total_increasing'},
    'duration': {'measurement', 'total', 'total_increasing'},
    'energy': {'total', 'total_increasing'},
    'energy_distance': {'measurement'},
    'energy_storage': {'measurement'},
    'enum': set(),
    'frequency': {'measurement'},
    'gas': {'total', 'total_increasing'},
    'humidity': {'measurement'},
    'illuminance': {'measurement'},
    'irradiance': {'measurement'},
    'moisture': {'measurement'},
    'monetary': {'total'},
    'nitrogen_dioxide': {'measurement'},
    'nitrogen_monoxide': {'measurement'},
    'nitrous_oxide': {'measurement'},
    'ozone': {'measurement'},
    'ph': {'measurement'},
    'pm1': {'measurement'},
    'pm10': {'measurement'},
    'pm25': {'measurement'},
    'pm4': {'measurement'},
    'power': {'measurement'},
    'power_factor': {'measurement'},
    'precipitation': {'measurement', 'total', 'total_increasing'},
    'precipitation_intensity': {'measurement'},
    'pressure': {'measurement'},
    'reactive_energy': {'total', 'total_increasing'},
    'reactive_power': {'measurement'},
    'signal_strength': {'measurement'},
    'sound_pressure': {'measurement'},
    'speed': {'measurement'},
    'sulphur_dioxide': {'measurement'},
    'temperature': {'measurement'},
    'temperature_delta': {'measurement'},
    'timestamp': set(),
    'uptime': set(),
    'volatile_organic_compounds': {'measurement'},
    'volatile_organic_compounds_parts': {'measurement'},
    'voltage': {'measurement'},
    'volume': {'total', 'total_increasing'},
    'volume_storage': {'measurement'},
    'volume_flow_rate': {'measurement'},
    'water': {'total', 'total_increasing'},
    'weight': {'measurement', 'total', 'total_increasing'},
    'wind_direction': {'measurement_angle'},
    'wind_speed': {'measurement'},
}

# Valid units for each state_class (from HA STATE_CLASS_UNITS)
STATE_CLASS_UNITS = {
    'measurement_angle': {'°'},
}

# Number device classes (same as sensor, but excludes date/enum/timestamp/uptime)
NUMBER_DEVICE_CLASSES = {
    'absolute_humidity', 'apparent_power', 'aqi', 'area', 'atmospheric_pressure',
    'battery', 'blood_glucose_concentration', 'carbon_monoxide', 'carbon_dioxide',
    'conductivity', 'current', 'data_rate', 'data_size', 'distance', 'duration',
    'energy', 'energy_distance', 'energy_storage', 'frequency', 'gas', 'humidity',
    'illuminance', 'irradiance', 'moisture', 'monetary', 'nitrogen_dioxide',
    'nitrogen_monoxide', 'nitrous_oxide', 'ozone', 'ph', 'pm1', 'pm10', 'pm25',
    'pm4', 'power', 'power_factor', 'precipitation', 'precipitation_intensity',
    'pressure', 'reactive_energy', 'reactive_power', 'signal_strength',
    'sound_pressure', 'speed', 'sulphur_dioxide', 'temperature', 'temperature_delta',
    'volatile_organic_compounds', 'volatile_organic_compounds_parts', 'voltage',
    'volume', 'volume_storage', 'volume_flow_rate', 'water', 'weight',
    'wind_direction', 'wind_speed',
}

# Number device class units (same as sensor)
NUMBER_DEVICE_CLASS_UNITS = SENSOR_DEVICE_CLASS_UNITS


def validate_sensor(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate sensor domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement') or None
    state_class = erd.get('state_class') or ''

    # Non-numeric device classes cannot have unit_of_measurement or state_class
    if device_class in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
        if unit_of_measurement:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"cannot have unit_of_measurement='{unit_of_measurement}'",
                file=defs_file
            )
        if state_class:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"cannot have state_class='{state_class}'",
                file=defs_file
            )

    # Validate unit_of_measurement for device_class
    if device_class and unit_of_measurement:
        valid_units = SENSOR_DEVICE_CLASS_UNITS.get(device_class)
        if valid_units is not None and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    # Validate state_class for device_class
    if device_class and state_class:
        valid_state_classes = SENSOR_DEVICE_CLASS_STATE_CLASSES.get(device_class)
        if valid_state_classes is not None and state_class not in valid_state_classes:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with device_class='{device_class}' "
                f"has invalid state_class='{state_class}'. "
                f"Valid state_classes: {sorted([str(sc) for sc in valid_state_classes]) or 'none'}",
                file=defs_file
            )

    # Validate unit_of_measurement for state_class
    if state_class and unit_of_measurement:
        valid_units = STATE_CLASS_UNITS.get(state_class)
        if valid_units is not None and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): sensor with state_class='{state_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    return error_count


def validate_binary_sensor(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate binary_sensor domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')

    # binary_sensor cannot have unit_of_measurement
    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    # binary_sensor cannot have state_class
    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor cannot have state_class='{state_class}'",
            file=defs_file
        )

    # Validate device_class
    if device_class and device_class not in BINARY_SENSOR_DEVICE_CLASSES:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): binary_sensor has invalid device_class='{device_class}'. "
            f"Valid device_classes: {sorted(BINARY_SENSOR_DEVICE_CLASSES)}",
            file=defs_file
        )

    return error_count


def validate_number(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate number domain rules. Returns error count."""
    error_count = 0
    device_class = erd.get('device_class') or ''
    unit_of_measurement = erd.get('unit_of_measurement') or None
    state_class = erd.get('state_class')

    # number cannot have state_class
    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): number cannot have state_class='{state_class}'",
            file=defs_file
        )

    # Validate device_class (cannot be date/enum/timestamp/uptime)
    if device_class and device_class in SENSOR_NON_NUMERIC_DEVICE_CLASSES:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): number cannot have device_class='{device_class}'",
            file=defs_file
        )

    # Validate unit_of_measurement for device_class
    if device_class and unit_of_measurement:
        valid_units = NUMBER_DEVICE_CLASS_UNITS.get(device_class)
        if valid_units is not None and unit_of_measurement not in valid_units:
            error_count += 1
            emit_error(
                f"ERD {erd_id} ({name}): number with device_class='{device_class}' "
                f"has invalid unit_of_measurement='{unit_of_measurement}'. "
                f"Valid units: {sorted([str(u) for u in valid_units if u])}",
                file=defs_file
            )

    return error_count


def validate_select(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate select domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): select cannot have device_class='{device_class}'",
            file=defs_file
        )

    return error_count


def validate_switch(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate switch domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): switch cannot have device_class='{device_class}'",
            file=defs_file
        )

    return error_count


def validate_button(erd: dict, erd_id: str, name: str, defs_file: str) -> int:
    """Validate button domain rules. Returns error count."""
    error_count = 0
    unit_of_measurement = erd.get('unit_of_measurement')
    state_class = erd.get('state_class')
    scaling_factor = erd.get('scaling_factor')
    device_class = erd.get('device_class')

    if unit_of_measurement:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have unit_of_measurement='{unit_of_measurement}'",
            file=defs_file
        )

    if state_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have state_class='{state_class}'",
            file=defs_file
        )

    if scaling_factor:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have scaling_factor={scaling_factor}",
            file=defs_file
        )

    if device_class:
        error_count += 1
        emit_error(
            f"ERD {erd_id} ({name}): button cannot have device_class='{device_class}'",
            file=defs_file
        )

    return error_count


def main():
    defs_path = Path(__file__).parent / 'appliance_api_erd_definitions.json'
    with open(defs_path) as f:
        data = json.load(f)

    error_count = 0
    defs_file = str(defs_path)

    for erd in data.get('erds', []):
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')

        if not ha_domain:
            continue

        if ha_domain == 'sensor':
            error_count += validate_sensor(erd, erd_id, name, defs_file)
        elif ha_domain == 'binary_sensor':
            error_count += validate_binary_sensor(erd, erd_id, name, defs_file)
        elif ha_domain == 'number':
            error_count += validate_number(erd, erd_id, name, defs_file)
        elif ha_domain == 'select':
            error_count += validate_select(erd, erd_id, name, defs_file)
        elif ha_domain == 'switch':
            error_count += validate_switch(erd, erd_id, name, defs_file)
        elif ha_domain == 'button':
            error_count += validate_button(erd, erd_id, name, defs_file)

    if error_count > 0:
        print(f"Found {error_count} HA domain rule violation(s).")
        sys.exit(1)
    else:
        print("All HA domain rule checks passed.")
        sys.exit(0)


if __name__ == '__main__':
    main()
