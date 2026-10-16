#!/usr/bin/env python3
"""Stamp only reviewed public HTML routes; preserve a bounded backup before changes.

Use --root for an isolated preview. Deploy calls this after publishing the catalog.
The explicit route list excludes internal files, proxy apps and generated snapshots.
"""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
from stamp_estate_bar import stamp

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/home/jeremy/demos'))
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    routes = json.loads((ROOT / 'site/assets/public-page-routes.json').read_text())['pages']
    fragment = (ROOT / 'site/assets/estate-bar/fragments/estate-bar.demos.html').read_text().strip()
    backup = None
    failures = []
    for rel in routes:
        if Path(rel).is_absolute() or any(x.startswith(('.', '_')) for x in Path(rel).parts):
            raise SystemExit(f'Unapproved path: {rel}')
        path = args.root / rel
        if not path.is_file():
            failures.append(f'Missing public page: {rel}')
            continue
        before = path.read_text()
        if args.check:
            if fragment not in before:
                failures.append(f'Navigation drift: {rel}')
            continue
        if fragment in before:
            continue
        if backup is None:
            backup = Path(tempfile.mkdtemp(prefix='intent-demos-navigation-backup-'))
        saved = backup / rel
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
        print(f'{stamp(path)}: {rel}')
    if backup:
        print(f'Backup: {backup}')
    if failures:
        raise SystemExit('\n'.join(failures))
    print(f'Public navigation verified: {len(routes)} reviewed pages')


if __name__ == '__main__':
    main()
