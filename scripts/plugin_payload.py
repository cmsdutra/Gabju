"""Seleção comum dos arquivos distribuídos no plugin."""

from pathlib import Path


EXCLUDED_NAMES = {
    ".git", ".gitignore", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "__pycache__", ".DS_Store", "Thumbs.db", "node_modules", "tests",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".swp", ".tmp", ".bak"}
DEVELOPMENT_PATHS = {
    "dist", "docs", "tests", "AGENTS.md", "CLAUDE.md", "requirements-dev.txt",
    "scripts/package_plugin.py", "scripts/validate_plugin.py",
    "scripts/plugin_payload.py", "temp_debug.pdf",
}


def payload_files(root: Path) -> list[Path]:
    """Inclui componentes de qualquer tipo, preservando seus caminhos relativos."""
    files = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_NAMES for part in relative.parts):
            continue
        if any(relative == Path(item) or Path(item) in relative.parents
               for item in DEVELOPMENT_PATHS):
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"Link simbólico fora do contrato de distribuição: {relative}")
        if path.is_file():
            files.append(path)
    return files
