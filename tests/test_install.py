import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.codex = Path(self.temp.name) / 'codex'
        self.target = self.codex / 'skills' / 'hwp'
        self.env = dict(os.environ, CODEX_HOME=str(self.codex))

    def run_install(self, *args):
        return subprocess.run([sys.executable, str(ROOT / 'install.py'), *args], env=self.env,
                              capture_output=True, text=True)

    def test_check_does_not_install(self):
        result = self.run_install('--check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())

    def test_install_status_backup_preserve_other_files(self):
        self.assertEqual(self.run_install().returncode, 0)
        self.assertEqual(self.run_install('--status').returncode, 0)
        extra = self.target / 'custom.txt'
        extra.write_text('keep me')
        (self.target / 'SKILL.md').write_text('old skill')
        self.assertNotEqual(self.run_install('--status').returncode, 0)
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.codex / 'skill-backups').glob('hwp-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'SKILL.md').read_text(), 'old skill')
        self.assertEqual(extra.read_text(), 'keep me')
        self.assertEqual(self.run_install('--status').returncode, 0)

    def test_missing_installation_status_is_read_only(self):
        self.assertNotEqual(self.run_install('--status').returncode, 0)
        self.assertFalse(self.codex.exists())

    def test_backup_inside_skill_is_rejected(self):
        self.assertEqual(self.run_install().returncode, 0)
        result = self.run_install('--backup-dir', str(self.target / 'backup'))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.target / 'backup').exists())

    def test_doctor_does_not_create_installation(self):
        result = subprocess.run([sys.executable, str(ROOT / 'doctor.py')], env=self.env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['skill_entrypoint_exists'])
        self.assertFalse(self.codex.exists())

    @unittest.skipUnless(sys.platform == 'win32', 'Windows launcher only')
    def test_windows_double_click_launcher(self):
        result = subprocess.run(['cmd.exe', '/d', '/c', str(ROOT / 'install.cmd')],
                                env=self.env, input=b'\n\n', capture_output=True,
                                timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.run_install('--status').returncode, 0)

if __name__ == '__main__':
    unittest.main()
