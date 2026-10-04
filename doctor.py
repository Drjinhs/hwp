"""Read-only environment diagnosis. Does not launch Hancom or install packages."""
import json
import os
from pathlib import Path
import platform
import shutil
import sys

def diagnose():
    codex = Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex')
    result = {
        'python': sys.version.split()[0],
        'python_executable': sys.executable,
        'python_supported': sys.version_info >= (3, 10),
        'system': platform.system(),
        'default_skill_path': str(codex / 'skills' / 'hwp'),
        'skill_entrypoint_exists': (codex / 'skills' / 'hwp' / 'SKILL.md').is_file(),
        'commands': {name: shutil.which(name) for name in ('python', 'py', 'python3', 'git', 'soffice')},
        'hancom_com_registered': False,
        'note': 'Registration is not a successful automation or conversion test. Font availability and page rendering require separate checks.'
    }
    if sys.platform == 'win32':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r'HWPFrame.HwpObject\CLSID') as key:
                result['hancom_com_registered'] = bool(winreg.QueryValueEx(key, '')[0])
        except OSError:
            pass
    return result

if __name__ == '__main__':
    print(json.dumps(diagnose(), ensure_ascii=False, indent=2))
