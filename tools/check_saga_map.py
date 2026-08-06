#!/usr/bin/env python3
"""Verifica o mapa editorial interno das 23 aventuras."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MAP = PROJECT_ROOT / "desenvolvimento" / "planejamento" / "mapa-da-saga.md"
DEFAULT_MANIFEST = PROJECT_ROOT / "publicacao" / "manifest.yml"
NODE_RE = re.compile(r"^\s*A(\d{2})\[", re.MULTILINE)


class SagaMapError(ValueError):
    pass


def subgraph_body(text: str, graph_id: str) -> str:
    match = re.search(rf'^\s*subgraph {re.escape(graph_id)}\[.*?^\s*end\s*$', text, re.MULTILINE | re.DOTALL)
    if not match:
        raise SagaMapError(f"subgrafo ausente: {graph_id}")
    return match.group(0)


def validate_map(map_path: Path, manifest_path: Path) -> None:
    text = map_path.read_text(encoding="utf-8")
    if "```mermaid" not in text:
        raise SagaMapError("bloco Mermaid ausente")
    numbers = [int(value) for value in NODE_RE.findall(text)]
    expected = list(range(1, 24))
    if sorted(numbers) != expected or len(numbers) != len(set(numbers)):
        raise SagaMapError(f"posições devem ser exatamente 1–23; encontradas: {numbers}")
    groups = {"ARC1": range(1, 7), "ARC2": range(7, 17), "ARC3": range(17, 24)}
    for graph_id, interval in groups.items():
        body = subgraph_body(text, graph_id)
        found = {int(value) for value in NODE_RE.findall(body)}
        if found != set(interval):
            raise SagaMapError(f"agrupamento incorreto em {graph_id}: {sorted(found)}")
    required = (
        "Fato fixo",
        "Consequência condicional",
        "Variável do Pacote",
        "Lacuna editorial",
        "Aventura 14",
        "captura física condicional",
        "Aventura 15",
        "Aventura 16",
        "Licença provisória",
        "Licença definitiva estudantil",
    )
    missing = [value for value in required if value not in text]
    if missing:
        raise SagaMapError(f"âncoras ou legenda ausentes: {missing}")
    manifest = manifest_path.read_text(encoding="utf-8")
    try:
        relative = map_path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        relative = map_path.as_posix()
    if relative in manifest or "desenvolvimento/" in manifest:
        raise SagaMapError("mapa interno não pode entrar no manifesto")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_map(args.map, args.manifest)
    except (OSError, SagaMapError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print("Mapa da saga válido: 23 aventuras, três arcos e planejamento isolado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
