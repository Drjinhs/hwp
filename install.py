"""Install the independent hwp skill using Python's standard library."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
FILES = ['SKILL.md', 'agents/openai.yaml', 'references/hwpx-format.md',
         'references/hwp-conversion.md', 'scripts/validate_hwpx.py']

def digest(path):
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, help='Override the destination hwp directory')
    parser.add_argument('--check', action='store_true', help='Verify release integrity without installation')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'checksums.json').read_text(encoding='utf-8'))
    for name in FILES:
        if digest(ROOT / 'hwp' / name) != manifest[name]:
            raise SystemExit('Integrity mismatch: ' + name)
    if args.check:
        print('OK: all five release files passed SHA-256 verification')
        return
    codex_dir = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    target = (args.target or codex_dir / 'skills' / 'hwp').resolve()
    if target.name != 'hwp':
        raise SystemExit('Destination directory must be named hwp')
    if target.exists():
        backup_root = codex_dir / 'skill-backups'
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
