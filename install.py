"""Install the independent hwp skill using Python's standard library."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent
FILES = ['SKILL.md', 'agents/openai.yaml', 'references/hwpx-format.md',
         'references/hwp-conversion.md', 'scripts/validate_hwpx.py']

def digest(path):
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    if sys.version_info < (3, 10):
        raise SystemExit('Python 3.10 or newer is required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, help='Override the destination hwp directory')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--check', action='store_true', help='Verify release integrity without installation')
    actions.add_argument('--status', action='store_true', help='Verify the existing installation without writing files')
    parser.add_argument('--backup-dir', type=Path, help='Override the backup directory')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'checksums.json').read_text(encoding='utf-8'))
    for name in FILES:
        if digest(ROOT / 'hwp' / name) != manifest[name]:
            raise SystemExit('Integrity mismatch: ' + name)
    codex_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    target = (args.target or codex_dir / 'skills' / 'hwp').resolve()
    if target.name != 'hwp':
        raise SystemExit('Destination directory must be named hwp')
    if args.check:
        print('OK: all five release files passed SHA-256 verification')
        return
    if args.status:
        problems = []
        for name in FILES:
            destination = target / name
            if not destination.is_file():
                problems.append('Missing installed file: ' + name)
            elif digest(destination) != manifest[name]:
                problems.append('Installed version differs: ' + name)
        if problems:
            raise SystemExit('\n'.join(problems))
        print('OK: installed files match this release:', target)
        return
    if target.exists():
        backup_root = (args.backup_dir or codex_dir / 'skill-backups').resolve()
        if backup_root == target or target in backup_root.parents:
            raise SystemExit('Backup directory must be outside the installed skill')
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup = backup_root / ('hwp-' + stamp)
        backup_root.mkdir(parents=True, exist_ok=True)
        shutil.copytree(target, backup)
        print('Backup:', backup)
    for name in FILES:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / 'hwp' / name, destination)
        assert digest(destination) == manifest[name]
    print('Installed and verified:', target)

if __name__ == '__main__':
    main()
