#!/usr/bin/env python3
"""Extract the full merits reasoning block of a prior decision as Markdown quote.

The script is intentionally conservative: it extracts only when clear section
markers are present. It does not summarize, clean, or rewrite the source text.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


START_RE = re.compile(r"^\s*FUNDAMENTA(?:Ç|C)ÃO\s*$", re.IGNORECASE)
END_RE = re.compile(
    r"^\s*(?:DELIBERA(?:Ç|C)ÃO\s+JUDICIAL|DISPOSITIVO|PROVID(?:Ê|E)NCIAS\s+DE\s+IMPULSO\s+PROCESSUAL)\s*$",
    re.IGNORECASE,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def extract(lines: list[str]) -> list[str]:
    start = None
    for i, line in enumerate(lines):
        if START_RE.match(line):
            start = i + 1
            break
    if start is None:
        raise ValueError("Marcador inicial 'FUNDAMENTAÇÃO' não localizado.")

    end = None
    for i in range(start, len(lines)):
        if END_RE.match(lines[i]):
            end = i
            break
    if end is None:
        raise ValueError("Marcador final 'DELIBERAÇÃO JUDICIAL', 'DISPOSITIVO' ou 'PROVIDÊNCIAS DE IMPULSO PROCESSUAL' não localizado.")

    block = lines[start:end]
    while block and block[0] == "":
        block.pop(0)
    while block and block[-1] == "":
        block.pop()
    if not block:
        raise ValueError("Bloco de fundamentação vazio.")
    return block


def to_markdown_quote(lines: list[str]) -> str:
    return "\n".join(">" if line == "" else f"> {line}" for line in lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extrai integralmente a fundamentação de decisão concessiva e formata como citação Markdown."
    )
    parser.add_argument("arquivo", help="Arquivo .txt da decisão concessiva.")
    parser.add_argument("--plain", action="store_true", help="Emitir texto sem prefixo de citação Markdown.")
    args = parser.parse_args()

    path = Path(args.arquivo)
    try:
        text = read_text(path)
        lines = text.splitlines()
        block = extract(lines)
        output = "\n".join(block) if args.plain else to_markdown_quote(block)
    except Exception as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
