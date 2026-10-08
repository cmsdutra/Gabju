"""Regressões da seleção de componentes distribuídos."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from plugin_payload import payload_files


def test_shared_components_and_resources_are_included(tmp_path):
    names = [
        "plugin.json", "scripts/indexar_pdf.py", "library/common.py",
        "agents/revisor.toml", "mcp.json", "assets/modelo.pdf",
        "assets/calculos.xlsx", "tools/consulta.py",
    ]
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("recurso", encoding="utf-8")
    assert {p.relative_to(tmp_path).as_posix() for p in payload_files(tmp_path)} == set(names)


def test_development_and_transient_files_are_excluded(tmp_path):
    names = [
        "scripts/indexar_pdf.py", "scripts/package_plugin.py",
        "scripts/__pycache__/indexar_pdf.pyc", "docs/ticket.md",
        "tests/test_indexar_pdf.py", "dist/plugin.zip", "AGENTS.md",
        "skills/example/tests/test_example.py", "temp_debug.pdf",
    ]
    for name in names:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("arquivo", encoding="utf-8")
    result = {p.relative_to(tmp_path).as_posix() for p in payload_files(tmp_path)}
    assert result == {"scripts/indexar_pdf.py"}
