#!/usr/bin/env python3
"""Valida arquitetura editorial, manifesto e links locais ativos."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML é necessário: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "publicacao" / "manifest.yml"
INVENTORY = ROOT / "recuperacao" / "inventario.json"
MIGRATIONS = ROOT / "recuperacao" / "migracoes-caminhos.yml"
FORBIDDEN_ROOTS = ("desenvolvimento/", "historico/", "recuperacao/", "publicacao/stubs/")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter não terminado")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter não é objeto")
    return data


def active_markdown_files() -> list[Path]:
    files: set[Path] = set()
    for name in ("AGENTS.md", "README.md", "RECUPERACAO.md", "SUMMARY.md", "ORGANIZACAO.md"):
        path = ROOT / name
        if path.is_file():
            files.add(path)
    for root_name in ("cenario", "campanha", "regras", "apendices"):
        files.update((ROOT / root_name).rglob("*.md"))
    files.update((ROOT / "publicacao" / "fontes").rglob("*.md"))
    publication_readme = ROOT / "publicacao" / "README.md"
    if publication_readme.is_file():
        files.add(publication_readme)
    return sorted(files)


def link_target(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1:value.index(">")]
    # Títulos opcionais aparecem depois de espaço; caminhos desta árvore não usam espaços.
    return value.split(maxsplit=1)[0]


def validate_links(errors: list[str]) -> int:
    checked = 0
    for source in active_markdown_files():
        text = source.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            target = unquote(link_target(match.group(1)))
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            clean = target.split("#", 1)[0].split("?", 1)[0]
            if not clean:
                continue
            resolved = (source.parent / clean).resolve()
            checked += 1
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"Link sai do projeto: {rel(source)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"Link local quebrado: {rel(source)} -> {target}")
    return checked


def validate_manifest(errors: list[str]) -> tuple[int, set[str]]:
    if not MANIFEST.is_file():
        errors.append("Manifesto operacional ausente: publicacao/manifest.yml")
        return 0, set()
    legacy_manifest = ROOT / "publicacao" / ("manifesto" + ".yml")
    if legacy_manifest.exists():
        errors.append(f"Manifesto histórico permanece na área operacional: {rel(legacy_manifest)}")
    if not (ROOT / "historico" / "publicacao" / "manifesto-publicacao-recuperado.yml").is_file():
        errors.append("Manifesto histórico recuperado não foi preservado")
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    indexed = {item["caminho_atual"]: item for item in inventory.get("documentos_editoriais", [])}
    destinations: set[str] = set()
    sources: set[str] = set()
    count = 0
    for section in manifest.get("secoes", []):
        for document in section.get("documentos", []):
            if not document.get("publicar", True):
                continue
            count += 1
            source = document.get("origem")
            destination = document.get("destino")
            if not source or not destination:
                errors.append(f"Entrada ativa sem origem ou destino na seção {section.get('id')}")
                continue
            if source in sources:
                errors.append(f"Fonte ativa duplicada: {source}")
            sources.add(source)
            if destination in destinations:
                errors.append(f"Destino ativo duplicado: {destination}")
            destinations.add(destination)
            if source.startswith(FORBIDDEN_ROOTS):
                errors.append(f"Fonte em raiz proibida: {source}")
            source_path = (ROOT / source).resolve()
            try:
                source_path.relative_to(ROOT)
            except ValueError:
                errors.append(f"Fonte fora do projeto: {source}")
                continue
            if not source_path.is_file():
                errors.append(f"Fonte ativa ausente: {source}")
                continue
            if Path(destination).is_absolute() or ".." in Path(destination).parts:
                errors.append(f"Destino inseguro: {destination}")
            try:
                fm = parse_front_matter(source_path)
            except ValueError as exc:
                errors.append(f"Front matter inválido: {source}: {exc}")
                continue
            if fm.get("status") in {"recuperacao-pendente", "stub-gerado"} or fm.get("publicar") is False:
                errors.append(f"Fonte ativa não publicável: {source}")
            record = indexed.get(source)
            if record is None:
                errors.append(f"Fonte ativa não inventariada: {source}")
            else:
                expected_status = record.get("status_esperado")
                if expected_status is not None and fm.get("status") != expected_status:
                    errors.append(f"Status do manifesto diverge do inventário: {source}")
                if record.get("publicar_esperado") is not True:
                    errors.append(f"Inventário não aprova fonte ativa: {source}")
    return count, sources


def validate_old_paths(errors: list[str]) -> int:
    migrations = yaml.safe_load(MIGRATIONS.read_text(encoding="utf-8")) or {}
    old_paths = [item["anterior"] for item in migrations.get("migracoes_regras", [])]
    short_paths = [Path(path).name for path in old_paths]
    scan: set[Path] = set(active_markdown_files())
    scan.update((ROOT / "tools").glob("*.py"))
    scan.add(MANIFEST)
    occurrences = 0
    for path in sorted(scan):
        text = path.read_text(encoding="utf-8", errors="replace")
        for old, short in zip(old_paths, short_paths):
            if old in text or short in text:
                occurrences += 1
                errors.append(f"Referência editorial antiga: {rel(path)} -> {old}")
    return occurrences


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        links = validate_links(errors)
        docs, _ = validate_manifest(errors)
        old_refs = validate_old_paths(errors)
    except Exception as exc:
        errors.append(f"Falha inesperada na validação: {exc}")
        links = docs = old_refs = 0

    if docs != 3:
        warnings.append(f"Manifesto atual contém {docs} documentos ativos; esperado nesta recuperação: 3")

    if errors:
        for item in errors:
            print(f"ERRO: {item}", file=sys.stderr)
        for item in warnings:
            print(f"AVISO: {item}", file=sys.stderr)
        return 1

    print("Arquitetura editorial válida.")
    print(f"Documentos ativos no manifesto: {docs}")
    print(f"Links locais verificados: {links}")
    print(f"Referências editoriais antigas: {old_refs}")
    for item in warnings:
        print(f"AVISO: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
