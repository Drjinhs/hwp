"""Check skill metadata, references, and Python syntax without dependencies."""
import ast
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skill = root / 'hwp'
text = (skill / 'SKILL.md').read_text(encoding='utf-8')
assert text.startswith('---\n')
frontmatter = text.split('---', 2)[1]
assert re.search(r'^name: hwp$', frontmatter, re.M)
assert re.search(r'^description: .+', frontmatter, re.M)
for path in re.findall(r'\]\((references/[^)]+)\)', text):
    assert (skill / path).is_file(), path
yaml = (skill / 'agents/openai.yaml').read_text(encoding='utf-8')
assert 'interface:' in yaml and '$hwp' in yaml
assert 'allow_implicit_invocation: false' not in yaml
for script in root.rglob('*.py'):
    ast.parse(script.read_text(encoding='utf-8'), filename=str(script))
print('OK: metadata, linked references, invocation settings and Python syntax')
print('Direct checks only; not a substitute for quick_validate or native document rendering.')
