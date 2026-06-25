#!/usr/bin/env python3
"""
Validate that all ha_domain/device_class combinations in the ERD definitions
are valid for Home Assistant. Exits with code 1 and prints errors if any
invalid combinations are found.
"""

import json
import sys
from pathlib import Path

VALID_DEVICE_CLASSES = {
    'button': {'restart'},
    'switch': {'outlet', 'switch'},
    'binary_sensor': {
        'battery', 'battery_charging', 'carbon_monoxide', 'cold',
        'connectivity', 'door', 'garage_door', 'gas', 'heat',
        'light', 'lock', 'moisture', 'motion', 'moving',
        'occupancy', 'opening', 'plug', 'power', 'presence',
        'problem', 'running', 'safety', 'smoke', 'sound',
        'tamper', 'update', 'vibration', 'window',
    },
    'sensor': {
        'date', 'enum', 'timestamp', 'uptime',
        'absolute_humidity', 'apparent_power', 'aqi', 'area',
        'atmospheric_pressure', 'battery', 'blood_glucose_concentration',
        'carbon_monoxide', 'carbon_dioxide', 'conductivity', 'current',
        'data_rate', 'data_size', 'distance', 'duration', 'energy',
        'energy_distance', 'energy_storage', 'frequency', 'gas',
        'humidity', 'illuminance', 'irradiance', 'moisture', 'monetary',
        'nitrogen_dioxide', 'nitrogen_monoxide', 'nitrous_oxide', 'ozone',
        'ph', 'pm1', 'pm10', 'pm25', 'pm4', 'power_factor', 'power',
        'precipitation', 'precipitation_intensity', 'pressure',
        'reactive_energy', 'reactive_power', 'signal_strength',
        'sound_pressure', 'speed', 'sulphur_dioxide', 'temperature',
        'temperature_delta', 'volatile_organic_compounds',
        'volatile_organic_compounds_parts', 'voltage', 'volume',
        'volume_storage', 'volume_flow_rate', 'water', 'weight',
        'wind_direction', 'wind_speed',
    },
}


def main():
    defs_path = Path(__file__).parent / 'appliance_api_erd_definitions.json'
    with open(defs_path) as f:
        data = json.load(f)

    errors = []
    for erd in data.get('erds', []):
        erd_id = erd.get('id', '<unknown>')
        name = erd.get('name', '<unknown>')
        ha_domain = erd.get('ha_domain')
        device_class = erd.get('device_class')

        if not ha_domain:
            continue

        if not device_class:
            continue

        valid = VALID_DEVICE_CLASSES.get(ha_domain)
        if valid is None:
            # No restrictions for this domain
            continue

        if device_class not in valid:
            errors.append(
                f"ERD {erd_id} ({name}): ha_domain='{ha_domain}' with "
                f"device_class='{device_class}' is invalid. "
                f"Valid values for '{ha_domain}': {sorted(valid)}"
            )

    if errors:
        print(f"Found {len(errors)} invalid device_class combinations:")
        for err in errors:
            print(f"  ERROR: {err}")
        sys.exit(1)
    else:
        print("All ha_domain/device_class combinations are valid.")
        sys.exit(0)


if __name__ == '__main__':
    main()
