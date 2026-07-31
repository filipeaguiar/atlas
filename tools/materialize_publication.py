#!/usr/bin/env python3
"""Materializa somente fontes explicitamente aprovadas no manifesto atual.

Também sincroniza os 23 stubs de aventura a partir de
`desenvolvimento/planejamento/funcoes-aventuras.yml`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML é necessário: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "publicacao" / "manifest.yml"
FUNCTIONS = ROOT / "desenvolvimento" / "planejamento" / "funcoes-aventuras.yml"
STUBS = ROOT / "publicacao" / "stubs" / "campanha" / "aventuras"
FORBIDDEN_ROOTS = {"desenvolvimento", "historico", "recuperacao"}


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML raiz inválida: {path}")
    return data


def safe_project_path(raw: str) -> Path:
    path = (ROOT / raw).resolve()
    try:
        rel = path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"Caminho fora do projeto: {raw}") from exc
    if rel.parts and rel.parts[0] in FORBIDDEN_ROOTS:
        raise ValueError(f"Fonte interna proibida: {raw}")
    if rel.parts[:2] == ("publicacao", "stubs"):
        raise ValueError(f"Stub não pode ser fonte publicável: {raw}")
    return path


def parse_front_matter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("Front matter não terminado")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("Front matter inválido")
    return data


def slug(text: str) -> str:
    import unicodedata
    value = unicodedata.normalize("NFKD", text)
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()


def sync_stubs(check: bool = False) -> list[str]:
    data = load_yaml(FUNCTIONS)
    adventures = data.get("aventuras")
    if not isinstance(adventures, dict) or len(adventures) != 23:
        raise ValueError("funcoes-aventuras.yml deve conter exatamente 23 aventuras")
    changes: list[str] = []
    for raw_number in sorted(adventures, key=lambda v: int(v)):
        number = int(raw_number)
        item = adventures[raw_number]
        arc = int(item["arco"])
        title = item.get("titulo") or f"Aventura {number:02d} — título em desenvolvimento"
        filename = f"{number:02d}-{slug(title)}.md"
        path = STUBS / filename
        extra = ""
        if number == 14:
            extra = """
## Agência e resultados possíveis

O marco obrigatório é reconhecer a seleção deliberada da Vanguarda. A captura física não é obrigatória. A aventura deve aceitar:

1. captura impedida, com evidência suficiente do padrão;
2. captura concluída com custos impostos ao antagonista;
3. captura concluída com vantagem ampla da oposição.
"""
        content = f"""---
id: aventura-{number:02d}
titulo: "{title}"
tipo: aventura
status: stub-gerado
publicar: false
arco: {arc}
funcao: "{str(item['funcao']).replace('"', '\\"')}"
"""
        if item.get("marco_obrigatorio"):
            content += f'marco_obrigatorio: "{item["marco_obrigatorio"]}"\n'
        if item.get("resultado_fisico"):
            content += f'resultado_fisico: "{item["resultado_fisico"]}"\n'
        content += f"""---

# {title}

> Documento interno de preparação. Não entra na publicação enquanto `publicar` permanecer falso.

**Arco:** {arc}  
**Função estrutural:** {item['funcao']}.

## Resumo para o Mestre

_A preencher quando a aventura for desenvolvida._

## Estado inicial relevante

_A preencher a partir do briefing de continuidade._

## Elenco, locais e pressões

_A preencher._

## Situações e cenas

_A preencher sem impor uma sequência única de decisões._

## Pistas e contrajogo

_A preencher com mais de um caminho para cada revelação indispensável._

## Consequências e debriefing

_A preencher e registrar depois na transição interna._
{extra}
"""
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != content:
            changes.append(str(path.relative_to(ROOT)))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    return changes


def iter_documents(manifest: dict):
    for section in manifest.get("secoes", []):
        section_id = section.get("id")
        section_title = section.get("titulo", section_id)
        for doc in section.get("documentos", []):
            yield section_id, section_title, doc


def validate(manifest_path: Path) -> tuple[dict, list[dict], list[str]]:
    manifest = load_yaml(manifest_path)
    docs: list[dict] = []
    errors: list[str] = []
    destinations: set[str] = set()
    forbidden_terms = manifest.get("termos_proibidos", [])

    for section_id, section_title, doc in iter_documents(manifest):
        if not doc.get("publicar", True):
            continue
        source_raw = doc.get("origem")
        dest_raw = doc.get("destino")
        if not source_raw or not dest_raw:
            errors.append(f"Documento sem origem/destino na seção {section_id}")
            continue
        try:
            source = safe_project_path(source_raw)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not source.exists():
            errors.append(f"Fonte ausente: {source_raw}")
            continue
        if dest_raw in destinations:
            errors.append(f"Destino duplicado: {dest_raw}")
            continue
        destinations.add(dest_raw)
        text = source.read_text(encoding="utf-8")
        try:
            fm = parse_front_matter(text)
        except ValueError as exc:
            errors.append(f"{source_raw}: {exc}")
            continue
        if fm.get("publicar") is False or fm.get("status") == "recuperacao-pendente":
            errors.append(f"Fonte não publicável declarada como ativa: {source_raw}")
            continue
        for term in forbidden_terms:
            if term in text:
                errors.append(f"Termo proibido em {source_raw}: {term}")
        docs.append({
            "secao": section_id,
            "secao_titulo": section_title,
            "origem": source_raw,
            "destino": dest_raw,
            "titulo": fm.get("titulo") or Path(dest_raw).stem.replace("-", " ").title(),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })
    return manifest, docs, errors


def materialize(manifest_path: Path, check: bool = False) -> int:
    manifest, docs, errors = validate(manifest_path)
    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1

    cfg = manifest["publicacao"]
    out = safe_project_path(cfg.get("conteudo", "publicacao/conteudo"))
    report = safe_project_path(cfg.get("relatorio", "build/relatorio-materializacao.md"))

    if check:
        print(f"Manifesto válido: {manifest_path.relative_to(ROOT)}")
        print(f"Documentos publicáveis recuperados: {len(docs)}")
        return 0

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    summary = ["# Sumário da publicação recuperada", ""]
    current_section = None
    publication = {"publicacao": cfg, "documentos": docs}
    for doc in docs:
        source = ROOT / doc["origem"]
        dest = out / doc["destino"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
        if doc["secao"] != current_section:
            current_section = doc["secao"]
            summary += [f'- **{doc["secao_titulo"]}**']
        summary += [f'  - [{doc["titulo"]}]({doc["destino"]})']

    (out / "SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    (out / "publication.yml").write_text(yaml.safe_dump(publication, allow_unicode=True, sort_keys=False), encoding="utf-8")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# Relatório de materialização\n\n"
        f"- Manifesto: `{manifest_path.relative_to(ROOT)}`\n"
        f"- Saída: `{out.relative_to(ROOT)}`\n"
        f"- Documentos incluídos: **{len(docs)}**\n"
        "- Fontes internas copiadas: **0**\n\n"
        "## Documentos\n\n" + "\n".join(f'- `{d["destino"]}` ← `{d["origem"]}`' for d in docs) + "\n",
        encoding="utf-8",
    )
    print(f"Materialização concluída: {len(docs)} documentos")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--sync-stubs", action="store_true")
    args = parser.parse_args()

    manifest = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    if args.sync_stubs:
        changes = sync_stubs(check=args.check)
        print(f"Stubs {'a alterar' if args.check else 'sincronizados'}: {len(changes)}")
        if args.check and changes:
            for path in changes:
                print(f"- {path}")
            return 2
        if not args.check and not manifest.exists():
            return 0
    return materialize(manifest, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
