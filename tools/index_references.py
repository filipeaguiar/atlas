#!/usr/bin/env python3
"""Fragmenta referências externas locais e reconstrói um índice SQLite FTS5."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from chonkie import RecursiveChunker, RecursiveLevel, RecursiveRules

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "references.yml"
SCHEMA_VERSION = 1
AUTHORITY = "referencia-externa"


@dataclass(frozen=True)
class ReferenceSource:
    """Livro externo explicitamente catalogado."""

    id: str
    title: str
    edition: str
    relative_path: str
    path: Path
    sha256: str
    text: str


@dataclass(frozen=True)
class ReferenceChunk:
    """Fragmento rastreável de uma referência externa."""

    id: str
    source_id: str
    source_sha256: str
    start_index: int
    end_index: int
    approximate_page: int | None
    word_count: int
    text: str


def is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def safe_path(root: Path, value: str, *, label: str) -> Path:
    candidate = (root / value).resolve()
    if not is_inside(candidate, root):
        raise ValueError(f"{label} sai da raiz permitida: {value}")
    return candidate


def load_config(config_path: Path, root: Path) -> dict[str, Any]:
    config_path = config_path.resolve()
    root = root.resolve()
    if not is_inside(config_path, root):
        raise ValueError("configuração deve permanecer dentro da raiz do projeto")
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"catálogo deve usar schema_version: {SCHEMA_VERSION}")
    if not data.get("sources"):
        raise ValueError("catálogo não contém referências")
    if set(data.get("search", {})) != {
        "default_results",
        "max_results",
        "default_snippet_characters",
        "max_snippet_characters",
    }:
        raise ValueError("configuração de busca incompleta")
    return data


def load_sources(config: dict[str, Any], root: Path) -> list[ReferenceSource]:
    """Valida catálogo e carrega somente livros locais explicitamente listados."""

    root = root.resolve()
    reference_root = safe_path(root, config["reference_root"], label="reference_root")
    if reference_root.name != "referencias":
        raise ValueError("reference_root deve apontar para referencias/")
    if reference_root.is_symlink() or not is_inside(reference_root, root):
        raise ValueError("reference_root inválida ou externa")

    ids: set[str] = set()
    paths: set[str] = set()
    sources: list[ReferenceSource] = []
    for entry in config["sources"]:
        missing = {"id", "path", "titulo", "edicao"} - set(entry)
        if missing:
            raise ValueError(f"entrada de catálogo incompleta: {sorted(missing)}")
        source_id = str(entry["id"]).strip()
        relative_path = Path(str(entry["path"]))
        if not source_id or source_id in ids:
            raise ValueError(f"id de referência vazio ou duplicado: {source_id!r}")
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise ValueError(f"caminho de referência inválido: {relative_path}")
        source_path = (reference_root / relative_path).resolve()
        if not is_inside(source_path, reference_root):
            raise ValueError(f"referência sai de referencias/: {relative_path}")
        normalized = source_path.relative_to(reference_root).as_posix()
        if normalized in paths:
            raise ValueError(f"caminho de referência duplicado: {normalized}")
        if source_path.suffix.lower() != ".md":
            raise ValueError(f"referência deve ser Markdown: {normalized}")
        if not source_path.is_file():
            raise FileNotFoundError(f"referência catalogada ausente: {normalized}")
        if source_path.is_symlink():
            raise ValueError(f"links simbólicos não são aceitos: {normalized}")
        raw = source_path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError(f"referência não está em UTF-8: {normalized}") from exc
        ids.add(source_id)
        paths.add(normalized)
        sources.append(
            ReferenceSource(
                id=source_id,
                title=str(entry["titulo"]),
                edition=str(entry["edicao"]),
                relative_path=f"referencias/{normalized}",
                path=source_path,
                sha256=hashlib.sha256(raw).hexdigest(),
                text=text,
            )
        )
    return sorted(sources, key=lambda item: item.id)


def make_chunker(config: dict[str, Any]) -> RecursiveChunker:
    settings = config["chunker"]
    rules = RecursiveRules(
        levels=[
            RecursiveLevel(delimiters="\f", include_delim="prev"),
            RecursiveLevel(delimiters=["\n\n", "\r\n", "\n", "\r"], include_delim="prev"),
            RecursiveLevel(delimiters=[". ", "! ", "? ", ": ", "; "], include_delim="prev"),
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


def approximate_page(text: str, start_index: int) -> int | None:
    """Estima página pela quantidade de quebras de formulário anteriores."""

    if "\f" not in text:
        return None
    return text.count("\f", 0, start_index) + 1


def chunk_sources(sources: list[ReferenceSource], config: dict[str, Any]) -> list[ReferenceChunk]:
    """Fragmenta livros e gera identificadores determinísticos."""

    chunker = make_chunker(config)
    result: list[ReferenceChunk] = []
    for source in sources:
        for chunk in chunker(source.text):
            if chunk.text != source.text[chunk.start_index : chunk.end_index]:
                raise RuntimeError(f"índices inconsistentes produzidos para {source.relative_path}")
            identity = "\0".join(
                [source.id, source.sha256, str(chunk.start_index), str(chunk.end_index)]
            )
            result.append(
                ReferenceChunk(
                    id=hashlib.sha256(identity.encode("utf-8")).hexdigest(),
                    source_id=source.id,
                    source_sha256=source.sha256,
                    start_index=chunk.start_index,
                    end_index=chunk.end_index,
                    approximate_page=approximate_page(source.text, chunk.start_index),
                    word_count=chunk.token_count,
                    text=chunk.text,
                )
            )
    return result


def output_path(config: dict[str, Any], root: Path) -> Path:
    root = root.resolve()
    output = safe_path(root, config["output"], label="output")
    allowed = (root / "build" / "retrieval").resolve()
    if not is_inside(output, allowed) or output.suffix != ".sqlite":
        raise ValueError("output deve ser um SQLite sob build/retrieval/")
    return output


def create_database(path: Path, sources: list[ReferenceSource], chunks: list[ReferenceChunk]) -> None:
    """Cria banco completo em arquivo temporário e substitui a versão anterior."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.unlink(missing_ok=True)
    try:
        connection = sqlite3.connect(temporary)
        with connection:
            connection.executescript(
                """
                PRAGMA journal_mode=DELETE;
                PRAGMA synchronous=FULL;
                CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
                CREATE TABLE sources (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    edition TEXT NOT NULL,
                    path TEXT NOT NULL,
                    sha256 TEXT NOT NULL,
                    chunk_count INTEGER NOT NULL
                );
                CREATE TABLE chunks (
                    rowid INTEGER PRIMARY KEY,
                    id TEXT UNIQUE NOT NULL,
                    source_id TEXT NOT NULL REFERENCES sources(id),
                    source_sha256 TEXT NOT NULL,
                    start_index INTEGER NOT NULL,
                    end_index INTEGER NOT NULL,
                    approximate_page INTEGER,
                    word_count INTEGER NOT NULL,
                    text TEXT NOT NULL
                );
                CREATE VIRTUAL TABLE chunks_fts USING fts5(
                    text,
                    content='chunks',
                    content_rowid='rowid',
                    tokenize='unicode61 remove_diacritics 2'
                );
                """
            )
            metadata = {
                "schema_version": str(SCHEMA_VERSION),
                "authority": AUTHORITY,
                "chunker": "chonkie-1.7.0/recursive-ocr-local",
            }
            connection.executemany("INSERT INTO metadata(key, value) VALUES (?, ?)", metadata.items())
            counts = {source.id: 0 for source in sources}
            for chunk in chunks:
                counts[chunk.source_id] += 1
            connection.executemany(
                "INSERT INTO sources(id, title, edition, path, sha256, chunk_count) VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (source.id, source.title, source.edition, source.relative_path, source.sha256, counts[source.id])
                    for source in sources
                ],
            )
            connection.executemany(
                """
                INSERT INTO chunks(
                    id, source_id, source_sha256, start_index, end_index,
                    approximate_page, word_count, text
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk.id,
                        chunk.source_id,
                        chunk.source_sha256,
                        chunk.start_index,
                        chunk.end_index,
                        chunk.approximate_page,
                        chunk.word_count,
                        chunk.text,
                    )
                    for chunk in chunks
                ],
            )
            connection.execute("INSERT INTO chunks_fts(chunks_fts) VALUES ('rebuild')")
            connection.execute("PRAGMA optimize")
        connection.close()
        os.replace(temporary, path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def build_reference_index(config_path: Path, root: Path) -> tuple[Path, list[ReferenceSource], list[ReferenceChunk]]:
    config = load_config(config_path, root)
    sources = load_sources(config, root)
    chunks = chunk_sources(sources, config)
    destination = output_path(config, root)
    create_database(destination, sources, chunks)
    return destination, sources, chunks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        path, sources, chunks = build_reference_index(args.config, args.root)
    except (OSError, ValueError, RuntimeError, sqlite3.Error, yaml.YAMLError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    print(f"Autoridade: {AUTHORITY}")
    for source in sources:
        count = sum(chunk.source_id == source.id for chunk in chunks)
        print(f"{source.title}: {count} fragmentos")
    print(f"Total: {len(chunks)} fragmentos")
    print(f"Índice local: {path.relative_to(args.root.resolve()).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
