#!/usr/bin/env python3
"""Perform conservative structural checks on an HWPX ZIP package."""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path, PurePosixPath, PureWindowsPath
from xml.etree import ElementTree

EXPECTED_MIMETYPE = b"application/hwp+zip"
REQUIRED_ENTRIES = {
    "mimetype",
    "META-INF/manifest.xml",
    "Contents/content.hpf",
    "Contents/header.xml",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"file not found: {path}"]
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if not infos:
                return ["empty ZIP package"]
            if names[0] != "mimetype":
                errors.append("mimetype is not the first ZIP entry")
            else:
                if infos[0].compress_type != zipfile.ZIP_STORED:
                    errors.append("mimetype must be stored without compression")
                if archive.read("mimetype").strip() != EXPECTED_MIMETYPE:
                    errors.append("unexpected mimetype content")
            missing = sorted(REQUIRED_ENTRIES.difference(names))
            if missing:
                errors.append("missing required entries: " + ", ".join(missing))
            if not any(name.startswith("Contents/section") and name.endswith(".xml") for name in names):
                errors.append("no Contents/section*.xml body part found")
            seen: set[str] = set()
            for info in infos:
                posix = PurePosixPath(info.filename.replace('\\', '/'))
                windows = PureWindowsPath(info.filename)
                if posix.is_absolute() or windows.drive or windows.root or ".." in posix.parts:
                    errors.append(f"unsafe archive path: {info.filename}")
                if info.filename in seen:
                    errors.append(f"duplicate ZIP entry: {info.filename}")
                seen.add(info.filename)
                if info.filename.lower().endswith((".xml", ".hpf")):
                    try:
                        ElementTree.fromstring(archive.read(info.filename))
                    except ElementTree.ParseError as exc:
                        errors.append(f"invalid XML in {info.filename}: {exc}")
    except zipfile.BadZipFile as exc:
        errors.append(f"not a valid ZIP package: {exc}")
    except (RuntimeError, NotImplementedError) as exc:
        errors.append(f"unsupported or unreadable ZIP entry: {exc}")
    except OSError as exc:
        errors.append(f"unable to read file: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="HWPX file to validate")
    args = parser.parse_args()
    errors = validate(args.file)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.file} passed structural HWPX checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
