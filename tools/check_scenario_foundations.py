#!/usr/bin/env python3
"""Valida proveniência e limites dos fundamentos públicos do cenário."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML é necessário: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "desenvolvimento" / "planejamento" / "matriz-factual-cenario.yml"
INVENTORY = ROOT / "recuperacao" / "inventario.json"
MANIFEST = ROOT / "publicacao" / "manifest.yml"
ALLOWED_SOURCE_ROOTS = {
    "publicacao/fontes/introducao/01-introducao.md",
    "regras/README.md",
    "regras/05-operacoes-do-atlas.md",
    "AGENTS.md",
    "apendices/questoes-em-aberto.md",
}
SECRET_PATTERNS = {
    "identidade de Tomás": re.compile(r"\bTomás(?:\s+Valença)?\b", re.I),
    "Vestígios": re.compile(r"\bVestígio(?:s)?\b", re.I),
    "Clarão artificial": re.compile(r"Clarão\s+artificial", re.I),
    "Retorno da campanha": re.compile(r"\bO\s+Retorno\b"),
    "sequestros": re.compile(r"\bsequestro(?:s|ado|ada)?\b", re.I),
    "Tenente Principal": re.compile(r"Tenente\s+Principal", re.I),
    "sobrevivência secreta": re.compile(r"antagonista.{0,50}sobreviv", re.I | re.S),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def split_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("front matter ausente")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter não terminado")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter não é objeto")
    return data, text[end + 5 :]


def active_sources() -> set[str]:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    return {
        doc["origem"]
        for section in manifest.get("secoes", [])
        for doc in section.get("documentos", [])
        if doc.get("publicar", True)
    }


def main() -> int:
    errors: list[str] = []
    matrix = yaml.safe_load(MATRIX.read_text(encoding="utf-8")) or {}
    targets = set(matrix.get("capitulos_em_escopo", []))
    if len(targets) != 9:
        errors.append(f"Matriz deve conter nove capítulos; encontrou {len(targets)}")
    if matrix.get("metadata", {}).get("publicar") is not False:
        errors.append("Matriz factual deve permanecer não publicável")

    declared_sources = {item.get("caminho") for item in matrix.get("fontes_permitidas", [])}
    if declared_sources != ALLOWED_SOURCE_ROOTS:
        errors.append("Lista de fontes permitidas diverge do contrato desta reescrita")
    for fact in matrix.get("fatos_autorizados", []):
        source_id = fact.get("fonte")
        source = next((item.get("caminho") for item in matrix.get("fontes_permitidas", []) if item.get("id") == source_id), None)
        if source not in ALLOWED_SOURCE_ROOTS:
            errors.append(f"Fato usa fonte não autorizada: {fact.get('id')} -> {source!r}")
        for chapter in fact.get("capitulos", []):
            if chapter not in targets:
                errors.append(f"Fato autoriza capítulo fora do escopo: {fact.get('id')} -> {chapter}")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    indexed = {item["caminho_atual"]: item for item in inventory.get("documentos_editoriais", [])}
    manifest_sources = active_sources()
    forbidden_terms = (yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}).get("termos_proibidos", [])

    for target in sorted(targets):
        path = ROOT / target
        if not path.is_file():
            errors.append(f"Capítulo ausente: {target}")
            continue
        try:
            fm, body = split_front_matter(path)
        except ValueError as exc:
            errors.append(f"{target}: {exc}")
            continue
        expected = {
            "status": "canon",
            "origem": "reescrita-aprovada",
            "publicar": True,
            "aprovado": True,
            "reescrita_de_marcador": True,
        }
        for key, value in expected.items():
            if fm.get(key) != value:
                errors.append(f"{target}: {key} deve ser {value!r}")
        sources = set(fm.get("fontes_fatuais", []))
        if not sources or not sources <= ALLOWED_SOURCE_ROOTS:
            errors.append(f"{target}: fontes_fatuais ausentes ou não autorizadas: {sorted(sources)}")
        if len(body.strip()) < 1500:
            errors.append(f"{target}: conteúdo insuficiente para capítulo completo")
        if "Recuperação pendente" in body or "_A preencher" in body:
            errors.append(f"{target}: marcador ou placeholder remanescente")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(body):
                errors.append(f"{target}: segredo público proibido ({label})")
        for term in forbidden_terms:
            if term in body:
                errors.append(f"{target}: termo editorial proibido: {term}")
        record = indexed.get(target)
        if record is None or record.get("estado_recuperacao") != "reescrito-aprovado":
            errors.append(f"{target}: inventário não registra reescrita aprovada")
        else:
            history = record.get("historico_recuperacao", {})
            if history.get("conteudo_original_recuperado") is not False or not history.get("sha256_marcador_substituido"):
                errors.append(f"{target}: histórico do marcador incompleto")
        if target not in manifest_sources:
            errors.append(f"{target}: capítulo aprovado ausente do manifesto")

    if inventory.get("contagens_esperadas", {}).get("marcadores_recuperacao_pendente") != 85:
        errors.append("Inventário não espera 85 marcadores pendentes")
    if inventory.get("contagens_esperadas", {}).get("reescritos_aprovados") != 9:
        errors.append("Inventário não espera nove reescritas aprovadas")
    if inventory.get("contagens_esperadas", {}).get("documentos_ativos_manifesto") != 12:
        errors.append("Inventário não espera 12 documentos ativos")

    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1

    print("Fundamentos públicos do cenário válidos.")
    print(f"Capítulos reescritos e aprovados: {len(targets)}")
    print(f"Fontes factuais permitidas: {len(ALLOWED_SOURCE_ROOTS)}")
    print("Segredos públicos encontrados: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
