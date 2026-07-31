#!/usr/bin/env python3
"""Valida a integridade física e editorial da reconstrução."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML é necessário: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "recuperacao" / "inventario.json"
MIGRATIONS = ROOT / "recuperacao" / "migracoes-caminhos.yml"
MANIFEST = ROOT / "publicacao" / "manifest.yml"
PENDING_ROOTS = ("cenario", "campanha", "regras", "apendices")
FORBIDDEN_SOURCE_ROOTS = ("desenvolvimento/", "historico/", "recuperacao/", "publicacao/stubs/")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def parse_front_matter(path: Path) -> dict:
    if path.suffix.lower() != ".md":
        return {}
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


def physical_markers() -> set[str]:
    found: set[str] = set()
    for root_name in PENDING_ROOTS:
        for path in (ROOT / root_name).rglob("*.md"):
            try:
                if parse_front_matter(path).get("status") == "recuperacao-pendente":
                    found.add(rel(path))
            except ValueError:
                # O erro de front matter será informado na validação YAML/metadados.
                continue
    return found


def physical_stubs() -> set[str]:
    root = ROOT / "publicacao" / "stubs"
    return {rel(path) for path in root.rglob("*.md") if parse_front_matter(path).get("status") == "stub-gerado"}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # Todos os arquivos YAML devem ser sintaticamente válidos.
    for path in sorted(list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml"))):
        if ".git" in path.parts:
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"YAML inválido: {rel(path)}: {exc}")

    try:
        inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"Inventário JSON inválido: {exc}")
        inventory = {}

    if inventory.get("schema_version") != "2.0":
        errors.append("recuperacao/inventario.json deve usar schema_version 2.0")

    records = inventory.get("documentos_editoriais", [])
    if not isinstance(records, list):
        errors.append("documentos_editoriais deve ser uma lista")
        records = []

    seen: set[str] = set()
    inventory_pending: set[str] = set()
    inventory_stubs: set[str] = set()
    inventory_rewritten: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or not record.get("caminho_atual"):
            errors.append(f"Registro editorial inválido: {record!r}")
            continue
        current = record["caminho_atual"]
        if current in seen:
            errors.append(f"Caminho duplicado no inventário: {current}")
        seen.add(current)
        path = ROOT / current
        if record.get("existencia_esperada", True) and not path.exists():
            errors.append(f"Arquivo inventariado ausente: {current}")
            continue
        if not path.is_file():
            continue
        try:
            fm = parse_front_matter(path)
        except ValueError as exc:
            errors.append(f"Front matter inválido: {current}: {exc}")
            continue
        expected_status = record.get("status_esperado")
        if expected_status is not None and fm.get("status") != expected_status:
            errors.append(
                f"Status divergente: {current}: esperado {expected_status!r}, encontrado {fm.get('status')!r}"
            )
        if fm.get("publicar") is not None and fm.get("publicar") != record.get("publicar_esperado"):
            errors.append(f"Publicabilidade divergente: {current}")
        state = record.get("estado_recuperacao")
        if state == "recuperacao-pendente":
            inventory_pending.add(current)
            if fm.get("publicar") is not False:
                errors.append(f"Marcador sem publicar:false: {current}")
        if state == "stub-gerado":
            inventory_stubs.add(current)
            if fm.get("publicar") is not False:
                errors.append(f"Stub sem publicar:false: {current}")
        if state == "reescrito-aprovado":
            inventory_rewritten.add(current)
            if fm.get("status") != "canon" or fm.get("origem") != "reescrita-aprovada":
                errors.append(f"Reescrita aprovada com metadados divergentes: {current}")
            if fm.get("publicar") is not True or fm.get("aprovado") is not True:
                errors.append(f"Reescrita aprovada não publicável: {current}")
            if not fm.get("fontes_fatuais"):
                errors.append(f"Reescrita aprovada sem fontes factuais: {current}")
            history = record.get("historico_recuperacao", {})
            if history.get("conteudo_original_recuperado") is not False or not history.get("sha256_marcador_substituido"):
                errors.append(f"Reescrita sem histórico do marcador: {current}")

    expected = inventory.get("contagens_esperadas", {})
    actual_pending = physical_markers()
    if actual_pending != inventory_pending:
        for path in sorted(inventory_pending - actual_pending):
            errors.append(f"Marcador inventariado não confirmado fisicamente: {path}")
        for path in sorted(actual_pending - inventory_pending):
            errors.append(f"Marcador físico não inventariado: {path}")
    if len(actual_pending) != expected.get("marcadores_recuperacao_pendente"):
        errors.append(
            f"Contagem de marcadores divergente: {len(actual_pending)}; esperada {expected.get('marcadores_recuperacao_pendente')}"
        )

    actual_stubs = physical_stubs()
    if actual_stubs != inventory_stubs:
        for path in sorted(inventory_stubs - actual_stubs):
            errors.append(f"Stub inventariado não confirmado fisicamente: {path}")
        for path in sorted(actual_stubs - inventory_stubs):
            errors.append(f"Stub físico não inventariado: {path}")
    if len(actual_stubs) != expected.get("stubs_aventura"):
        errors.append(f"Contagem de stubs divergente: {len(actual_stubs)}; esperada {expected.get('stubs_aventura')}")
    if len(inventory_rewritten) != expected.get("reescritos_aprovados"):
        errors.append(
            f"Contagem de reescritas divergente: {len(inventory_rewritten)}; esperada {expected.get('reescritos_aprovados')}"
        )

    legacy_count = sum(1 for path in (ROOT / "publicacao" / "fontes-legado-97").rglob("*") if path.is_file())
    if legacy_count != expected.get("fontes_legado_97"):
        errors.append(f"Contagem do legado divergente: {legacy_count}; esperada {expected.get('fontes_legado_97')}")

    # Migrações preservam bytes e não deixam o caminho anterior ativo.
    try:
        migrations = yaml.safe_load(MIGRATIONS.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"Mapa de migrações inválido: {exc}")
        migrations = {}
    for item in migrations.get("migracoes_regras", []):
        old = ROOT / item["anterior"]
        current = ROOT / item["atual"]
        if old.exists():
            errors.append(f"Caminho antigo ainda existe: {item['anterior']}")
        if not current.is_file():
            errors.append(f"Caminho migrado ausente: {item['atual']}")
            continue
        digest = hashlib.sha256(current.read_bytes()).hexdigest()
        if digest != item.get("sha256_conteudo"):
            errors.append(f"Conteúdo alterado durante migração: {item['atual']}")

    # Nenhuma fonte pendente ou interna pode estar ativa no manifesto atual.
    try:
        manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        errors.append(f"Manifesto operacional inválido: {exc}")
        manifest = {}
    active_sources: list[str] = []
    for section in manifest.get("secoes", []):
        for doc in section.get("documentos", []):
            if doc.get("publicar", True):
                source = doc.get("origem")
                if source:
                    active_sources.append(source)
    if len(active_sources) != expected.get("documentos_ativos_manifesto"):
        errors.append(
            f"Documentos ativos divergentes: {len(active_sources)}; esperados {expected.get('documentos_ativos_manifesto')}"
        )
    for source in active_sources:
        path = ROOT / source
        if not path.is_file():
            errors.append(f"Fonte ativa ausente: {source}")
            continue
        fm = parse_front_matter(path)
        if fm.get("status") == "recuperacao-pendente" or fm.get("publicar") is False:
            errors.append(f"Fonte não publicável ativada: {source}")
        if source.startswith(FORBIDDEN_SOURCE_ROOTS):
            errors.append(f"Fonte interna ativada: {source}")

    # DEC-001 permanece uma invariável estrutural.
    try:
        functions = yaml.safe_load(
            (ROOT / "desenvolvimento" / "planejamento" / "funcoes-aventuras.yml").read_text(encoding="utf-8")
        )["aventuras"]
        if int(functions[14]["arco"]) != 2 or functions[14].get("resultado_fisico") != "condicional":
            errors.append("Aventura 14 não contém a segunda operação condicional")
        if "consequências da segunda operação" not in functions[15]["funcao"]:
            errors.append("Aventura 15 não contém as consequências da segunda operação")
        if "licença definitiva" not in functions[16]["funcao"]:
            errors.append("Aventura 16 não encerra o arco com licença definitiva")
    except Exception as exc:
        errors.append(f"Não foi possível validar DEC-001: {exc}")

    stale = re.compile(r"Aventura 15.{0,120}(segundo sequestro|segunda (?:operação de )?captura)", re.I | re.S)
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".yml", ".yaml", ".py"}:
            continue
        if any(part in {".git", "historico", "fontes-legado-97"} for part in path.parts) or path.name == "check_recovery.py":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if stale.search(text):
            errors.append(f"Mapeamento antigo de DEC-001 encontrado: {rel(path)}")

    warnings.append(f"Conteúdo ainda pendente de recuperação: {len(actual_pending)} documentos")

    if errors:
        for item in errors:
            print(f"ERRO: {item}", file=sys.stderr)
        for item in warnings:
            print(f"AVISO: {item}", file=sys.stderr)
        return 1

    print("Recuperação física e editorial válida.")
    print(f"Marcadores confirmados: {len(actual_pending)}")
    print(f"Stubs confirmados: {len(actual_stubs)}")
    print(f"Reescritas aprovadas: {len(inventory_rewritten)}")
    print(f"Documentos ativos no manifesto: {len(active_sources)}")
    print(f"Legado confirmado: {legacy_count}")
    for item in warnings:
        print(f"AVISO: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
