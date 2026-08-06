#!/usr/bin/env python3
"""Valida estrutura e gate editorial de aventuras incrementais."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "publicacao" / "manifest.yml"
REQUIRED_FINAL_HEADINGS = ("A história até aqui", "Fichas dos desafios", "Experiência", "Encerrando a aventura")
FORBIDDEN_BODY_HEADINGS = (
    "Resumo para o Mestre",
    "Função na campanha",
    "Elenco do exame",
    "Informações essenciais",
    "Desafios e regras",
    "Objetivos",
    "Sequência de cenas",
    "Alternativas entre cenas",
    "Estados de encerramento",
    "Consequências",
    "Debriefing, XP e progressão",
)


class AdventureError(ValueError):
    pass


def split_front_matter(text: str, path: Path) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise AdventureError(f"front matter ausente: {path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AdventureError(f"front matter não terminado: {path}")
    metadata = yaml.safe_load(text[4:end]) or {}
    if not isinstance(metadata, dict):
        raise AdventureError(f"front matter inválido: {path}")
    return metadata, text[end + 5 :]


def section_block(body: str, heading: re.Match[str], following: list[re.Match[str]]) -> str:
    later = [item.start() for item in following if item.start() > heading.start()]
    end = min(later) if later else len(body)
    return body[heading.end() : end]


def validate_adventure(path: Path, manifest_path: Path) -> None:
    metadata, body = split_front_matter(path.read_text(encoding="utf-8"), path)
    required_metadata = ("id", "titulo", "tipo", "status", "origem", "arco", "numero", "funcao", "publicar", "proveniencia")
    missing_metadata = [key for key in required_metadata if key not in metadata]
    if missing_metadata:
        raise AdventureError(f"metadados ausentes: {missing_metadata}")
    if metadata["tipo"] != "aventura":
        raise AdventureError("tipo deve ser aventura")
    if not isinstance(metadata["numero"], int) or not 1 <= metadata["numero"] <= 23:
        raise AdventureError("numero deve estar entre 1 e 23")

    title = re.search(r"^# (.+?)\s*$", body, re.MULTILINE)
    if not title:
        raise AdventureError("título H1 ausente")
    h2s = list(re.finditer(r"^## (.+?)\s*$", body, re.MULTILINE))
    headings = [item.group(1) for item in h2s]
    missing_headings = [heading for heading in REQUIRED_FINAL_HEADINGS if heading not in headings]
    if missing_headings:
        raise AdventureError(f"partes obrigatórias ausentes: {missing_headings}")
    forbidden = [heading for heading in FORBIDDEN_BODY_HEADINGS if heading in headings]
    if forbidden:
        raise AdventureError(f"seções de planejamento não permitidas no capítulo: {forbidden}")

    history = next(item for item in h2s if item.group(1) == "A história até aqui")
    intro = body[title.end() : history.start()]
    if len(re.sub(r"\s+", " ", intro).strip()) < 120:
        raise AdventureError("resumo inicial ausente ou curto demais")
    if "> **Leia em voz alta:**" not in intro:
        raise AdventureError("resumo deve conter leitura em voz alta")

    scenes = [item for item in h2s if re.fullmatch(r"Cena \d+ — .+", item.group(1))]
    if not scenes:
        raise AdventureError("nenhuma cena principal declarada")
    for scene in scenes:
        block = section_block(body, scene, h2s)
        if "> **Leia em voz alta:**" not in block:
            raise AdventureError(f"cena sem leitura em voz alta: {scene.group(1)}")
        if len(re.sub(r"\s+", " ", block).strip()) < 250:
            raise AdventureError(f"cena sem conteúdo suficiente: {scene.group(1)}")

    order = ["A história até aqui", scenes[0].group(1), "Fichas dos desafios", "Experiência", "Encerrando a aventura"]
    positions = [headings.index(item) for item in order]
    if positions != sorted(positions):
        raise AdventureError("ordem estrutural inválida")
    history_index = headings.index("A história até aqui")
    sheets_index = headings.index("Fichas dos desafios")
    scene_headings = [scene.group(1) for scene in scenes]
    if headings[history_index + 1 : sheets_index] != scene_headings:
        raise AdventureError("entre A história até aqui e as fichas devem existir somente cenas nomeadas")

    objective_major = len(re.findall(r"^### Objetivo Maior", body, re.MULTILINE))
    if objective_major != 1:
        raise AdventureError("aventura deve ter exatamente um Objetivo Maior")
    for phrase in ("Ganho", "Perda", "Ajuda", "Pontos de Ação", "XP"):
        if phrase not in body:
            raise AdventureError(f"orientação mecânica ausente: {phrase}")

    final_start = next(item.end() for item in h2s if item.group(1) == "Fichas dos desafios")
    final_material = body[final_start:]
    forbidden_negative = re.search(r"\b(não concede|não inclui|não possui|não há)\b", final_material, re.IGNORECASE)
    if forbidden_negative:
        raise AdventureError(f"material final descreve ausência: {forbidden_negative.group(0)}")

    manifest = manifest_path.read_text(encoding="utf-8")
    try:
        relative = path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        relative = path.as_posix()
    selected = relative in manifest
    approved = metadata.get("status") == "canon" and metadata.get("publicar") is True and metadata.get("aprovado") is True
    if selected and not approved:
        raise AdventureError("aventura em revisão não pode constar no manifesto")
    if approved and not selected:
        raise AdventureError("aventura aprovada e publicável deve constar no manifesto")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failed = False
    for path in args.paths:
        try:
            validate_adventure(path, args.manifest)
        except (OSError, AdventureError) as exc:
            failed = True
            print(f"ERRO: {exc}", file=sys.stderr)
        else:
            print(f"Aventura válida: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
