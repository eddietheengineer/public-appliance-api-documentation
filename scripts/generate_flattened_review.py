#!/usr/bin/env python3
"""Generate a flattened ERD review file from source JSON.

Reads appliance_api_erd_definitions.json and appliance_api.json,
produces erd_flattened.json with one entry per sub-field, each
containing a 'review' section for the agent to fill in.

Usage:
    python3 scripts/generate_flattened_review.py [--input ERD_FILE] [--api API_FILE] [--output OUTPUT]
"""

import argparse
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_erd_to_features(api_defs):
    """Build mapping from ERD ID to list of {api, feature, mask}."""
    erd_to_features = {}
    for api_id, api in api_defs.get('featureApis', {}).items():
        api_name = api['name']
        for version_id, version in api.get('versions', {}).items():
            for feature in version.get('features', []):
                feature_name = feature['name']
                feature_mask = feature.get('mask', '')
                for req in feature.get('required', []):
                    erd_id = req['erd']
                    if erd_id not in erd_to_features:
                        erd_to_features[erd_id] = []
                    erd_to_features[erd_id].append({
                        'api': api_name,
                        'feature': feature_name,
                        'mask': feature_mask,
                    })
    return erd_to_features


def make_entry(erd, erd_features):
    """Create a flattened entry for one sub-field of one ERD."""
    erd_id = erd['id']
    erd_name = erd['name']
    erd_desc = erd.get('description', '')
    erd_ops = erd.get('operations', [])
    erd_paired = erd.get('paired_erd')
    erd_role = erd.get('pair_role')

    return {
        'erd_id': erd_id,
        'erd_name': erd_name,
        'erd_description': erd_desc,
        'erd_operations': erd_ops,
        'erd_paired_erd': erd_paired,
        'erd_pair_role': erd_role,
        'erd_features': erd_features,
        'field_name': erd.get('field_name') or erd['name'],
        'field_type': erd.get('field_type') or 'unknown',
        'field_offset': erd.get('field_offset'),
        'field_size': erd.get('field_size'),
        'field_values': erd.get('field_values'),
        'field_bits': erd.get('field_bits'),
        'field_device_class': erd.get('field_device_class'),
        'field_unit_of_measurement': erd.get('field_unit_of_measurement'),
        'field_state_class': erd.get('field_state_class'),
        'field_ha_domain': erd.get('field_ha_domain'),
        'field_confidence': erd.get('field_confidence'),
        'field_last_reviewed': erd.get('field_last_reviewed'),
        'erd_ha_domain': erd.get('ha_domain'),
        'erd_device_class': erd.get('device_class'),
        'erd_unit_of_measurement': erd.get('unit_of_measurement'),
        'erd_scaling_factor': erd.get('scaling_factor'),
        'erd_state_class': erd.get('state_class'),
        'erd_options': erd.get('options'),
        'erd_confidence': erd.get('confidence'),
        'erd_comment': erd.get('comment'),
        'erd_updateClass': erd.get('updateClass'),
        'review': {
            'ha_domain': None,
            'device_class': None,
            'unit_of_measurement': None,
            'state_class': None,
            'filtered': False,
            'filter_reason': None,
            'reasoning': '',
        },
    }


def flatten(erd_defs, erd_to_features):
    """Flatten ERD definitions into one entry per sub-field."""
    flattened = []
    for erd in erd_defs.get('erds', []):
        erd_id = erd['id']
        erd_features = erd_to_features.get(erd_id, [])
        fields = erd.get('data', [])

        if len(fields) == 1:
            # Single field: merge field data into ERD context
            f = fields[0]
            merged = dict(erd)
            merged.update({
                'field_name': f['name'],
                'field_type': f['type'],
                'field_offset': f['offset'],
                'field_size': f['size'],
                'field_values': f.get('values'),
                'field_bits': f.get('bits'),
                'field_device_class': f.get('device_class'),
                'field_unit_of_measurement': f.get('unit_of_measurement'),
                'field_state_class': f.get('state_class'),
                'field_ha_domain': f.get('ha_domain'),
                'field_confidence': f.get('confidence'),
                'field_last_reviewed': f.get('last_reviewed'),
            })
            flattened.append(make_entry(merged, erd_features))
        else:
            # Multi-field: one entry per sub-field
            for f in fields:
                merged = dict(erd)
                merged.update({
                    'field_name': f['name'],
                    'field_type': f['type'],
                    'field_offset': f['offset'],
                    'field_size': f['size'],
                    'field_values': f.get('values'),
                    'field_bits': f.get('bits'),
                    'field_device_class': f.get('device_class'),
                    'field_unit_of_measurement': f.get('unit_of_measurement'),
                    'field_state_class': f.get('state_class'),
                    'field_ha_domain': f.get('ha_domain'),
                    'field_confidence': f.get('confidence'),
                    'field_last_reviewed': f.get('last_reviewed'),
                })
                flattened.append(make_entry(merged, erd_features))

    return flattened


def main():
    parser = argparse.ArgumentParser(
        description='Generate flattened ERD review file from source JSON.'
    )
    parser.add_argument(
        '--input',
        default=os.path.join(REPO_ROOT, 'appliance_api_erd_definitions.json'),
        help='Path to ERD definitions JSON (default: appliance_api_erd_definitions.json)',
    )
    parser.add_argument(
        '--api',
        default=os.path.join(REPO_ROOT, 'appliance_api.json'),
        help='Path to appliance API JSON (default: appliance_api.json)',
    )
    parser.add_argument(
        '--output',
        default=os.path.join(REPO_ROOT, 'erd_flattened.json'),
        help='Output path (default: erd_flattened.json)',
    )
    args = parser.parse_args()

    erd_defs = load_json(args.input)
    api_defs = load_json(args.api)

    erd_to_features = build_erd_to_features(api_defs)
    flattened = flatten(erd_defs, erd_to_features)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(flattened, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(flattened)} entries from {len(erd_defs.get('erds', []))} ERDs")
    print(f"Output: {args.output}")


if __name__ == '__main__':
    main()