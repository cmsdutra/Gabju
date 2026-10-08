#!/usr/bin/env python3
"""Validação determinística do plugin e de seu conteúdo portátil."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from plugin_payload import payload_files


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"\d+\.\d+\.\d+")
FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
RESOURCE_LITERAL_RE = re.compile(
    r"`((?:[a-z0-9-]+/)?(?:references|assets|scripts)/[^`]+)`"
)
SKILL_CALL_RE = re.compile(r"\$([a-z0-9]+(?:-[a-z0-9]+)*)")

LOCAL_DEPENDENCIES = {
    "caminho absoluto local": re.compile(r"(?:/home/|[A-Za-z]:\\\\Users\\\\)"),
    "pipeline Workbench": re.compile(r"(?:\.workbench|Workbench)(?:/|\\\\|\b)"),
    "árvore local do vault": re.compile(r"(?:300_Trabalho|400_Biblioteca|\.claude/skills)"),
    "repositório local de minutas": re.compile(r"Minutas/(?:04_)?Repositório", re.IGNORECASE),
    "comando de busca local": re.compile(r"\brg\s+(?:-[^\s]+\s+)*.*(?:Minutas|Repositório)"),
}
TRANSIENT_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db", ".pytest_cache", ".mypy_cache"}
TRANSIENT_SUFFIXES = {".pyc", ".pyo", ".swp", ".tmp", ".bak"}
SECRET_FILENAMES = re.compile(
    r"^(?:\.env(?:\..+)?|credentials?(?:\..+)?|secrets?(?:\..+)?|id_rsa|id_ed25519)$|\.(?:pem|key|p12|pfx)$",
    re.IGNORECASE,
)
SECRET_CONTENT = {
    "chave privada": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "chave OpenAI": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "chave AWS": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".txt", ".csv"}


def read_text(path: Path, errors: list[str]) -> str | None:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{path.relative_to(ROOT)}: BOM UTF-8 não permitido")
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: UTF-8 inválido ({exc})")
        return None


def parse_yaml(text: str, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        errors.append(f"{label}: YAML inválido ({exc})")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label}: YAML deve ser um objeto")
        return None
    return value


def resolve_resource(skill_dir: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    if any(char in target for char in "<>*{}"):
        return None
    target = target.removeprefix("./")
    own_candidate = skill_dir / target
    sibling_candidate = SKILLS / target
    if own_candidate.exists():
        return own_candidate
    if sibling_candidate.exists():
        return sibling_candidate
    root_candidate = ROOT / target
    if root_candidate.exists():
        return root_candidate
    return own_candidate


def validate_resources(skill_file: Path, text: str, errors: list[str]) -> None:
    included = {path.resolve() for path in payload_files(ROOT)}
    targets = [match.group(1) for match in MARKDOWN_LINK_RE.finditer(text)]
    targets.extend(match.group(1) for match in RESOURCE_LITERAL_RE.finditer(text))
    for raw_target in targets:
        resolved = resolve_resource(skill_file.parent, raw_target)
        if resolved is not None:
            resource = resolved.resolve()
            available = resource in included or (
                resolved.is_dir() and any(resource in path.parents for path in included)
            )
            if not available:
                errors.append(f"{skill_file.relative_to(ROOT)}: recurso ausente do pacote ({raw_target})")


def validate_payload_files(errors: list[str]) -> None:
    for path in payload_files(ROOT):
        rel = path.relative_to(ROOT)
        if path.name in TRANSIENT_NAMES or path.suffix.lower() in TRANSIENT_SUFFIXES:
            errors.append(f"{rel}: artefato transitório não permitido")
        if path.is_dir() and path.name == "node_modules":
            errors.append(f"{rel}: dependência local node_modules não permitida")
        if path.is_file() and SECRET_FILENAMES.search(path.name):
            errors.append(f"{rel}: nome de arquivo potencialmente secreto")
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path, errors)
        if text is None:
            continue
        for label, pattern in LOCAL_DEPENDENCIES.items():
            if pattern.search(text):
                errors.append(f"{rel}: dependência local remanescente ({label})")
        for label, pattern in SECRET_CONTENT.items():
            if pattern.search(text):
                errors.append(f"{rel}: segredo potencial detectado ({label})")


def validate_manifest(errors: list[str]) -> dict[str, Any] | None:
    manifest_path = ROOT / "plugin.json"
    text = read_text(manifest_path, errors)
    if text is None:
        return None
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"plugin.json: JSON inválido ({exc})")
        return None
    name = manifest.get("name", "")
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append("plugin.json: name deve ser kebab-case e ter até 64 caracteres")
    version = manifest.get("version", "")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        errors.append("plugin.json: version deve seguir SemVer estrito")
    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        errors.append("plugin.json: schema Agent Plugins 1.0 ausente ou incorreto")
    interface = manifest.get("extensions", {}).get("com.openai", {}).get("interface", {})
    if not isinstance(interface, dict):
        errors.append("plugin.json: extensions.com.openai.interface deve ser objeto")
        return manifest
    short_description = interface.get("shortDescription", "")
    if not isinstance(short_description, str) or len(short_description) > 30:
        errors.append("plugin.json: shortDescription deve ser texto de até 30 caracteres")
    prompts = interface.get("defaultPrompt", [])
    if not isinstance(prompts, (str, list)):
        errors.append("plugin.json: defaultPrompt deve ser string ou lista")
    if isinstance(prompts, list) and (
        not prompts or len(prompts) > 3 or not all(isinstance(prompt, str) for prompt in prompts)
    ):
        errors.append("plugin.json: defaultPrompt deve ter de um a três textos")
    return manifest


def validate_skills(errors: list[str]) -> int:
    skill_files = sorted(SKILLS.glob("*/SKILL.md"))
    names: set[str] = set()
    parsed: list[tuple[Path, str]] = []
    for skill_file in skill_files:
        text = read_text(skill_file, errors)
        if text is None:
            continue
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"{skill_file.relative_to(ROOT)}: frontmatter ausente ou inválido")
            continue
        frontmatter = parse_yaml(match.group(1), str(skill_file.relative_to(ROOT)), errors)
        if frontmatter is None:
            continue
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        if name != skill_file.parent.name:
            errors.append(f"{skill_file.relative_to(ROOT)}: name não coincide com a pasta")
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            errors.append(f"{skill_file.relative_to(ROOT)}: name inválido")
        elif name in names:
            errors.append(f"{skill_file.relative_to(ROOT)}: name duplicado")
        else:
            names.add(name)
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{skill_file.relative_to(ROOT)}: description ausente")
        validate_resources(skill_file, text, errors)
        parsed.append((skill_file, text))

        openai_yaml = skill_file.parent / "agents" / "openai.yaml"
        if not openai_yaml.is_file():
            errors.append(f"{openai_yaml.relative_to(ROOT)}: arquivo obrigatório ausente")
            continue
        yaml_text = read_text(openai_yaml, errors)
        if yaml_text is None:
            continue
        config = parse_yaml(yaml_text, str(openai_yaml.relative_to(ROOT)), errors)
        if config is None:
            continue
        interface = config.get("interface")
        policy = config.get("policy")
        if not isinstance(interface, dict):
            errors.append(f"{openai_yaml.relative_to(ROOT)}: interface ausente")
            continue
        for field in ("display_name", "short_description", "default_prompt"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                errors.append(f"{openai_yaml.relative_to(ROOT)}: campo {field} ausente")
        if isinstance(name, str) and f"${name}" not in interface.get("default_prompt", ""):
            errors.append(f"{openai_yaml.relative_to(ROOT)}: default_prompt deve mencionar ${name}")
        allow_implicit = policy.get("allow_implicit_invocation") if isinstance(policy, dict) else None
        if not isinstance(allow_implicit, bool):
            errors.append(f"{openai_yaml.relative_to(ROOT)}: allow_implicit_invocation deve ser booleano")
        disabled = frontmatter.get("disable-model-invocation", False)
        if disabled is not False and not isinstance(disabled, bool):
            errors.append(f"{skill_file.relative_to(ROOT)}: disable-model-invocation deve ser booleano")
        if isinstance(allow_implicit, bool) and bool(disabled) == allow_implicit:
            errors.append(f"{skill_file.parent.relative_to(ROOT)}: políticas de invocação sem paridade")

    for skill_file, text in parsed:
        for called_name in SKILL_CALL_RE.findall(text):
            if called_name not in names:
                errors.append(f"{skill_file.relative_to(ROOT)}: skill chamada não empacotada (${called_name})")
    return len(skill_files)


def main() -> int:
    errors: list[str] = []
    manifest = validate_manifest(errors)
    skill_count = validate_skills(errors)
    validate_payload_files(errors)
    if errors:
        print("Validação falhou:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print(f"Plugin válido: {manifest['name']} {manifest['version']} ({skill_count} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
