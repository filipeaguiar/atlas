#!/usr/bin/env python3
"""Gera um índice derivado de fontes editoriais aprovadas usando Chonkie."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from chonkie import RecursiveChunker, RecursiveLevel, RecursiveRules

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "retrieval.yml"
AUDIENCES = ("publico", "mestre")


@dataclass(frozen=True)
class SourceDocument:
    """Documento aprovado e pronto para fragmentação."""

    path: Path
    relative_path: str
    metadata: dict[str, Any]
    body: str
    body_offset: int
    sha256: str


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _safe_project_path(root: Path, value: str, *, label: str) -> Path:
    candidate = (root / value).resolve()
    if not _inside(candidate, root):
        raise ValueError(f"{label} sai da raiz do projeto: {value}")
    return candidate


def _relative_is_under(relative: Path, prefixes: Iterable[str]) -> bool:
    value = relative.as_posix()
    return any(value == prefix.rstrip("/") or value.startswith(prefix.rstrip("/") + "/") for prefix in prefixes)


def load_config(path: Path) -> dict[str, Any]:
    """Carrega e valida a configuração do índice."""

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if data.get("schema_version") != 1:
        raise ValueError("configuração deve usar schema_version: 1")
    if not data.get("source_roots"):
        raise ValueError("source_roots não pode ser vazio")
    if not data.get("allowed_statuses"):
        raise ValueError("allowed_statuses não pode ser vazio")
    if set(data.get("outputs", {})) != set(AUDIENCES):
        raise ValueError("outputs deve definir exatamente publico e mestre")
    return data


def split_front_matter(text: str) -> tuple[dict[str, Any], str, int]:
    """Separa front matter YAML e corpo, recusando documentos sem metadados."""

    if not text.startswith("---\n"):
        raise ValueError("front matter ausente")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter não terminado")
    metadata = yaml.safe_load(text[4:end]) or {}
    if not isinstance(metadata, dict):
        raise ValueError("front matter deve ser um objeto YAML")
    body_offset = end + 5
    return metadata, text[body_offset:], body_offset


def discover_markdown(root: Path, config: dict[str, Any]) -> list[Path]:
    """Descobre Markdown somente dentro das raízes editoriais permitidas."""

    root = root.resolve()
    forbidden = tuple(config.get("forbidden_roots", []))
    found: set[Path] = set()
    for value in config["source_roots"]:
        source_root = _safe_project_path(root, value, label="source_root")
        relative_root = source_root.relative_to(root)
        if _relative_is_under(relative_root, forbidden):
            raise ValueError(f"source_root proibida: {value}")
        if not source_root.exists():
            continue
        if not source_root.is_dir():
            raise ValueError(f"source_root não é diretório: {value}")
        for path in source_root.rglob("*.md"):
            resolved = path.resolve()
            if not _inside(resolved, root):
                raise ValueError(f"link ou caminho sai da raiz do projeto: {path}")
            relative = resolved.relative_to(root)
            if not _relative_is_under(relative, forbidden):
                found.add(resolved)
    return sorted(found, key=lambda item: item.relative_to(root).as_posix())


def load_source(
    path: Path,
    root: Path,
    config: dict[str, Any],
    audience: str,
) -> tuple[SourceDocument | None, str | None]:
    """Carrega uma fonte e explica por que fontes inelegíveis foram ignoradas."""

    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None, "arquivo não está em UTF-8"
    try:
        metadata, body, body_offset = split_front_matter(text)
    except (ValueError, yaml.YAMLError) as exc:
        return None, str(exc)

    allowed = set(config["allowed_statuses"])
    if metadata.get("status") not in allowed:
        return None, f"status não autorizado: {metadata.get('status')!r}"
    if metadata.get("publicar") is False:
        return None, "publicar: false"
    if audience == "publico" and (
        metadata.get("camada") == "mestre" or metadata.get("conteudo_para_jogadores") is False
    ):
        return None, "conteúdo restrito ao Mestre"
    if not body.strip():
        return None, "corpo vazio"

    relative = path.resolve().relative_to(root.resolve()).as_posix()
    return (
        SourceDocument(
            path=path,
            relative_path=relative,
            metadata=metadata,
            body=body,
            body_offset=body_offset,
            sha256=hashlib.sha256(raw).hexdigest(),
        ),
        None,
    )


def make_chunker(config: dict[str, Any]) -> RecursiveChunker:
    """Cria regras locais de Markdown sem baixar receitas externas."""

    settings = config["chunker"]
    rules = RecursiveRules(
        levels=[
            RecursiveLevel(
                delimiters=["\n# ", "\n## ", "\n### ", "\n#### ", "\n##### ", "\n###### "],
                include_delim="next",
            ),
            RecursiveLevel(delimiters=["\n\n", "\r\n", "\n", "\r"], include_delim="prev"),
            RecursiveLevel(delimiters=[". ", "! ", "? "], include_delim="prev"),
            RecursiveLevel(whitespace=True, include_delim="prev"),
            RecursiveLevel(),
        ]
    )
    return RecursiveChunker(
        tokenizer=settings["tokenizer"],
        chunk_size=int(settings["chunk_size"]),
        min_characters_per_chunk=int(settings["min_characters_per_chunk"]),
        rules=rules,
    )


def heading_at(text: str, offset: int) -> str | None:
    """Retorna o cabeçalho Markdown mais próximo antes do fragmento."""

    position = 0
    heading: str | None = None
    for line in text.splitlines(keepends=True):
        if position > offset:
            break
        stripped = line.strip()
        if stripped.startswith("#") and stripped.lstrip("#").startswith(" "):
            heading = stripped.lstrip("#").strip()
        position += len(line)
    return heading


def build_index(config_path: Path, root: Path, audience: str) -> dict[str, Any]:
    """Constrói em memória um índice determinístico."""

    if audience not in AUDIENCES:
        raise ValueError(f"audiência inválida: {audience}")
    root = root.resolve()
    config_path = config_path.resolve()
    if not _inside(config_path, root):
        raise ValueError("configuração deve estar dentro da raiz do projeto")
    config = load_config(config_path)
    chunker = make_chunker(config)

    chunks: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    ignored: list[dict[str, str]] = []
    for path in discover_markdown(root, config):
        relative = path.relative_to(root).as_posix()
        source, reason = load_source(path, root, config, audience)
        if source is None:
            ignored.append({"path": relative, "reason": reason or "não autorizado"})
            continue

        source_chunks = chunker(source.body)
        sources.append({"path": source.relative_path, "sha256": source.sha256, "chunks": len(source_chunks)})
        for item in source_chunks:
            if item.text != source.body[item.start_index : item.end_index]:
                raise RuntimeError(f"índices inconsistentes produzidos para {source.relative_path}")
            identity = "\0".join(
                [source.relative_path, source.sha256, audience, str(item.start_index), str(item.end_index)]
            )
            chunks.append(
                {
                    "id": hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                    "source_path": source.relative_path,
                    "source_sha256": source.sha256,
                    "source_start_index": source.body_offset + item.start_index,
                    "source_end_index": source.body_offset + item.end_index,
                    "body_start_index": item.start_index,
                    "body_end_index": item.end_index,
                    "token_count": item.token_count,
                    "heading": heading_at(source.body, item.start_index),
                    "metadata": {
                        key: source.metadata.get(key)
                        for key in ("id", "titulo", "tipo", "status", "origem", "camada")
                        if source.metadata.get(key) is not None
                    },
                    "text": item.text,
                }
            )

    settings = config["chunker"]
    return {
        "schema_version": 1,
        "audience": audience,
        "chunker": {
            "library": "chonkie",
            "version": "1.7.0",
            "strategy": "recursive-markdown-local",
            "tokenizer": settings["tokenizer"],
            "chunk_size": int(settings["chunk_size"]),
            "min_characters_per_chunk": int(settings["min_characters_per_chunk"]),
        },
        "sources": sources,
        "chunks": chunks,
        "ignored": ignored,
    }


def write_index(index: dict[str, Any], config_path: Path, root: Path) -> Path:
    """Escreve o índice somente no destino derivado configurado."""

    config = load_config(config_path)
    audience = index["audience"]
    output_value = config["outputs"][audience]
    output = _safe_project_path(root.resolve(), output_value, label="output")
    allowed_output_root = (root.resolve() / "build" / "retrieval").resolve()
    if not _inside(output, allowed_output_root):
        raise ValueError("output deve permanecer em build/retrieval/")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audience", choices=AUDIENCES, default="publico")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--check", action="store_true", help="valida e resume sem escrever a saída")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        index = build_index(args.config, args.root, args.audience)
        output = None if args.check else write_index(index, args.config, args.root)
    except (OSError, ValueError, RuntimeError, yaml.YAMLError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    print(f"Audiência: {args.audience}")
    print(f"Fontes indexadas: {len(index['sources'])}")
    print(f"Fragmentos: {len(index['chunks'])}")
    print(f"Arquivos ignorados: {len(index['ignored'])}")
    if output is not None:
        print(f"Saída: {output.relative_to(args.root.resolve()).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
