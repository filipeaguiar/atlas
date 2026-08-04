#!/usr/bin/env python3
"""Pesquisa o índice local de referências externas com SQLite FTS5."""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.index_references import AUTHORITY, DEFAULT_CONFIG, PROJECT_ROOT, load_config, output_path


def normalize_query(query: str) -> str:
    """Converte texto livre em consulta FTS que exige todos os termos."""

    terms = re.findall(r"[^\W_]+", query, flags=re.UNICODE)
    if not terms:
        raise ValueError("consulta não contém termos pesquisáveis")
    return " AND ".join(f'"{term}"' for term in terms)


def trim_snippet(value: str, maximum: int) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) <= maximum:
        return value
    shortened = value[: maximum - 2].rstrip()
    return shortened + " …"


def validate_database(connection: sqlite3.Connection) -> None:
    metadata = dict(connection.execute("SELECT key, value FROM metadata"))
    if metadata.get("authority") != AUTHORITY:
        raise ValueError("banco não é um índice de referências externas")
    if metadata.get("schema_version") != "1":
        raise ValueError("versão do índice de referências não suportada")


def search_database(
    database: Path,
    query: str,
    *,
    limit: int,
    snippet_characters: int,
) -> list[dict[str, Any]]:
    """Executa busca ranqueada e retorna apenas snippets limitados."""

    if limit < 1 or snippet_characters < 80:
        raise ValueError("limites de busca inválidos")
    fts_query = normalize_query(query)
    if not database.is_file():
        raise FileNotFoundError("índice ausente; execute tools/index_references.py")

    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        validate_database(connection)
        rows = connection.execute(
            """
            SELECT
                c.id,
                c.start_index,
                c.end_index,
                c.approximate_page,
                c.word_count,
                s.id AS source_id,
                s.title,
                s.edition,
                s.path,
                bm25(chunks_fts) AS score,
                snippet(chunks_fts, 0, '⟦', '⟧', ' … ', 48) AS snippet
            FROM chunks_fts
            JOIN chunks AS c ON c.rowid = chunks_fts.rowid
            JOIN sources AS s ON s.id = c.source_id
            WHERE chunks_fts MATCH ?
            ORDER BY score, s.id, c.start_index
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()
    finally:
        connection.close()

    return [
        {
            "authority": AUTHORITY,
            "chunk_id": row["id"],
            "source_id": row["source_id"],
            "title": row["title"],
            "edition": row["edition"],
            "path": row["path"],
            "approximate_page": row["approximate_page"],
            "start_index": row["start_index"],
            "end_index": row["end_index"],
            "word_count": row["word_count"],
            "snippet": trim_snippet(row["snippet"], snippet_characters),
        }
        for row in rows
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="termos mecânicos a localizar")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--snippet-characters", type=int)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config, args.root)
        settings = config["search"]
        requested_limit = args.limit if args.limit is not None else int(settings["default_results"])
        requested_snippet = (
            args.snippet_characters
            if args.snippet_characters is not None
            else int(settings["default_snippet_characters"])
        )
        limit = min(max(1, requested_limit), int(settings["max_results"]))
        snippet_characters = min(
            max(80, requested_snippet), int(settings["max_snippet_characters"])
        )
        database = output_path(config, args.root)
        results = search_database(
            database,
            args.query,
            limit=limit,
            snippet_characters=snippet_characters,
        )
    except (OSError, ValueError, sqlite3.Error, yaml.YAMLError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    print("Autoridade: referencia-externa — confira a passagem na obra original.")
    if not results:
        print("Nenhum resultado.")
        return 0
    for number, result in enumerate(results, 1):
        page = result["approximate_page"] if result["approximate_page"] is not None else "indisponível"
        print(f"\n{number}. {result['title']} — {result['edition']}")
        print(
            f"   Página aproximada: {page}; offsets: "
            f"{result['start_index']}–{result['end_index']}"
        )
        print(f"   {result['snippet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
