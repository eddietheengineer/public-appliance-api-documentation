#!/usr/bin/env python3
"""
Generate a coverage report summarizing HA metadata completeness across all ERDs.
Writes coverage_report.md to the repo root and to GitHub Step Summary if running in CI.
"""

import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ha_constants import ERD_DEFINITIONS_FILE
from validator_utils import IN_GITHUB_ACTIONS


def pct(n, total):
    if total == 0:
        return '0.0'
    return f'{n / total * 100:.1f}'


def generate_report():
    try:
        with open(ERD_DEFINITIONS_FILE) as f:
            data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, OSError) as exc:
        print(f'  ERROR: Failed to load {ERD_DEFINITIONS_FILE}: {exc}')
        raise SystemExit(1) from exc

    erds = data.get('erds', [])
    total = len(erds)
    ha_erds = [e for e in erds if isinstance(e, dict) and e.get('ha_domain')]
    ha_total = len(ha_erds)

    domain_counts = defaultdict(int)
    for e in ha_erds:
        if isinstance(e, dict):
            domain_counts[e['ha_domain']] += 1

    metadata_fields = [
        'device_class', 'unit_of_measurement', 'scaling_factor',
        'state_class', 'confidence', 'comment',
    ]
    metadata_counts = {}
    for field in metadata_fields:
        with_field = sum(1 for e in ha_erds if isinstance(e, dict) and e.get(field))
        without_field = ha_total - with_field
        metadata_counts[field] = (with_field, without_field)

    confidence_counts = defaultdict(int)
    for e in ha_erds:
        if isinstance(e, dict):
            c = e.get('confidence', '')
            if c:
                confidence_counts[c] += 1

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    lines = [
        '# HA Metadata Coverage Report',
        '',
        f'Generated: {timestamp}',
        '',
        '## ERD Summary',
        '',
        '| Metric | Count |',
        '|--------|-------|',
        f'| Total ERDs | {total} |',
        f'| ERDs with ha_domain | {ha_total} |',
        '',
        '## Coverage by HA Domain',
        '',
        '| ha_domain | Count |',
        '|-----------|-------|',
    ]

    for domain in sorted(domain_counts.keys()):
        lines.append(f'| {domain} | {domain_counts[domain]} |')

    lines += [
        '',
        '## Metadata Coverage (of ERDs with ha_domain)',
        '',
        '| Field | With | Without | Coverage % |',
        '|-------|------|---------|------------|',
    ]

    for field in metadata_fields:
        with_f, without_f = metadata_counts[field]
        lines.append(f'| {field} | {with_f} | {without_f} | {pct(with_f, ha_total)}% |')

    lines += [
        '',
        '## Confidence Distribution',
        '',
        '| Confidence | Count |',
        '|------------|-------|',
    ]

    for level in ('high', 'medium', 'low'):
        count = confidence_counts.get(level, 0)
        lines.append(f'| {level} | {count} |')

    lines.append('')

    return '\n'.join(lines), total, ha_total


def main():
    report_content, total, ha_total = generate_report()
    print(report_content)
    print(f'  Total ERDs: {total}')
    print(f'  ERDs with ha_domain: {ha_total}')

    if IN_GITHUB_ACTIONS:
        github_step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
        if github_step_summary:
            with open(github_step_summary, 'a', encoding='utf-8') as f:
                f.write(report_content)
            print(f'Written coverage report to GitHub Step Summary')


if __name__ == '__main__':
    main()