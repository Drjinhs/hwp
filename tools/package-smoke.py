"""Edit one actual HWPX template text node; do not claim native rendering."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
import io
import copy

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite existing output')
    spec = importlib.util.spec_from_file_location('validator', ROOT / 'hwp/scripts/validate_hwpx.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    errors = validator.validate(args.template)
    if errors:
        raise SystemExit('\n'.join(errors))
    marker = 'hwp 스킬 실제 HWPX 편집 테스트'
    with zipfile.ZipFile(args.template) as source:
        body_name = next(n for n in source.namelist() if n.startswith('Contents/section') and n.endswith('.xml'))
        original = source.read(body_name)
        for _, (prefix, uri) in ET.iterparse(io.BytesIO(original), events=['start-ns']):
            if not prefix.startswith('ns'):
                ET.register_namespace(prefix, uri)
        body = ET.fromstring(original)
        target = next(e for e in body.iter() if e.tag.endswith('}t') and e.text and not list(e))
        target.text = marker
        parent_map = {child: parent for parent in body.iter() for child in parent}
        paragraph = parent_map.get(target)
        while paragraph is not None and not paragraph.tag.endswith('}p'):
            paragraph = parent_map.get(paragraph)
        if paragraph is not None:
            for cache in list(paragraph):
                if cache.tag.endswith('}linesegarray'):
                    paragraph.remove(cache)
        changed = ET.tostring(body, encoding='utf-8', xml_declaration=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(args.output, 'w') as output:
            infos = sorted(source.infolist(), key=lambda i: i.filename != 'mimetype')
            for source_info in infos:
                info = copy.copy(source_info)
                if info.filename == 'mimetype':
                    info.compress_type = zipfile.ZIP_STORED
                output.writestr(info, changed if info.filename == body_name else source.read(info.filename))
        with zipfile.ZipFile(args.output) as output:
            unchanged = [n for n in source.namelist() if n != body_name]
            assert all(source.read(n) == output.read(n) for n in unchanged)
            assert marker in ''.join(ET.fromstring(output.read(body_name)).itertext())
            report = {'source': args.template.name, 'changed_part': body_name,
                      'unchanged_entry_bytes_verified': len(unchanged),
                      'structure_errors': validator.validate(args.output),
                      'output_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'native_open_verified': False, 'visual_review_verified': False,
                      'note': 'Local template-derived edit test; output is not a distributable report or typography template.'}
    assert not report['structure_errors'], report
    args.output.with_suffix('.report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
