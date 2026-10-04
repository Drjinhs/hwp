"""Synthetic ZIP fixtures test the validator; they are not Hangul documents."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'hwp/scripts/validate_hwpx.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'fixture.zip'

    def package(self, extra=None, bad_xml=False):
        with zipfile.ZipFile(self.path, 'w') as archive:
            archive.writestr('mimetype', b'application/hwp+zip')
            for name in sorted(validator.REQUIRED_ENTRIES - {'mimetype'}):
                archive.writestr(name, '<root/>')
            archive.writestr('Contents/section0.xml', '<root' if bad_xml else '<root/>')
            if extra:
                archive.writestr(extra, 'payload')

    def test_synthetic_structure_passes(self):
        self.package()
        self.assertEqual(validator.validate(self.path), [])

    def test_malformed_xml_fails(self):
        self.package(bad_xml=True)
        self.assertTrue(any('invalid XML' in e for e in validator.validate(self.path)))

    def test_traversal_and_windows_paths_fail(self):
        for name in ['../payload', '..\\payload', 'C:/payload', '/payload', '\\payload']:
            with self.subTest(name=name):
                self.package(extra=name)
                self.assertTrue(any('unsafe archive path' in e for e in validator.validate(self.path)))

    def test_plain_file_fails(self):
        self.path.write_text('not a ZIP')
        self.assertTrue(validator.validate(self.path))

if __name__ == '__main__':
    unittest.main()
