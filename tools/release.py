"""Refresh release checksums after an intentional skill edit."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
files = ['SKILL.md', 'agents/openai.yaml', 'references/hwpx-format.md',
         'references/hwp-conversion.md', 'scripts/validate_hwpx.py']
manifest = {}
for name in files:
    text = (root / 'hwp' / name).read_text(encoding='utf-8').replace('\r\n', '\n').replace('\r', '\n')
    manifest[name] = hashlib.sha256(text.encode()).hexdigest()
(root / 'checksums.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print('Updated release checksums.')
