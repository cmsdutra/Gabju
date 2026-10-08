#!/usr/bin/env python3
"""Cria ZIP portátil do plugin após validação."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

from plugin_payload import payload_files


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def main() -> int:
    validation = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_plugin.py")],
        cwd=ROOT,
        check=False,
    )
    if validation.returncode:
        return validation.returncode

    manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
    name = manifest["name"]
    archive = DIST / f"{name}.zip"
    DIST.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in payload_files(ROOT):
            package.write(path, f"{name}/{path.relative_to(ROOT).as_posix()}")
    print(archive)
    return 0


if __name__ == "__main__":
    sys.exit(main())
