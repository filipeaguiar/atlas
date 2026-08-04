from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest
import yaml

from tools.build_retrieval_index import build_index
from tools.index_references import (
    build_reference_index,
    chunk_sources,
    load_config,
    load_sources,
)
from tools.search_references import search_database


def write_catalog(root: Path, sources: list[dict] | None = None, **overrides) -> Path:
    data = {
        "schema_version": 1,
        "reference_root": "referencias",
        "output": "build/retrieval/referencias.sqlite",
        "chunker": {"tokenizer": "word", "chunk_size": 30, "min_characters_per_chunk": 10},
        "search": {
            "default_results": 5,
            "max_results": 10,
            "default_snippet_characters": 160,
            "max_snippet_characters": 300,
        },
        "sources": sources
        or [
            {
                "id": "manual",
                "path": "manual.md",
                "titulo": "Manual de Teste",
                "edicao": "1ª edição",
            }
        ],
    }
    data.update(overrides)
    path = root / "config" / "references.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def write_book(root: Path, name: str = "manual.md") -> Path:
    path = root / "referencias" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Ataque Especial permite concentrar poder em uma ação heroica. " * 12
        + "\f"
        + "Ganho e Perda modificam circunstâncias de testes e desafios. " * 12,
        encoding="utf-8",
    )
    return path


def test_fragmentos_deterministicos_com_pagina_e_offsets(tmp_path: Path) -> None:
    catalog = write_catalog(tmp_path)
    write_book(tmp_path)
    config = load_config(catalog, tmp_path)
    sources = load_sources(config, tmp_path)

    first = chunk_sources(sources, config)
    second = chunk_sources(sources, config)

    assert first == second
    assert len(first) > 1
    assert {chunk.approximate_page for chunk in first} == {1, 2}
    for chunk in first:
        assert len(chunk.id) == 64
        assert sources[0].text[chunk.start_index : chunk.end_index] == chunk.text
        assert chunk.source_sha256 == sources[0].sha256


def test_constroi_banco_e_pesquisa_com_citacao_limitada(tmp_path: Path) -> None:
    catalog = write_catalog(tmp_path)
    write_book(tmp_path)
    database, sources, chunks = build_reference_index(catalog, tmp_path)

    assert database.is_file()
    assert len(sources) == 1
    assert chunks
    connection = sqlite3.connect(database)
    assert dict(connection.execute("SELECT key, value FROM metadata"))["authority"] == "referencia-externa"
    connection.close()

    results = search_database(
        database,
        "Ataque Especial",
        limit=1,
        snippet_characters=100,
    )
    assert len(results) == 1
    assert results[0]["authority"] == "referencia-externa"
    assert results[0]["title"] == "Manual de Teste"
    assert results[0]["edition"] == "1ª edição"
    assert results[0]["approximate_page"] == 1
    assert len(results[0]["snippet"]) <= 100
    assert "⟦Ataque⟧" in results[0]["snippet"]
    assert search_database(database, "termo inexistente", limit=3, snippet_characters=100) == []


def test_recusa_livro_ausente_caminho_externo_e_link_simbolico(tmp_path: Path) -> None:
    catalog = write_catalog(tmp_path)
    config = load_config(catalog, tmp_path)
    with pytest.raises(FileNotFoundError, match="ausente"):
        load_sources(config, tmp_path)

    outside_catalog = write_catalog(
        tmp_path,
        sources=[
            {"id": "fora", "path": "../fora.md", "titulo": "Fora", "edicao": "1"}
        ],
    )
    config = load_config(outside_catalog, tmp_path)
    with pytest.raises(ValueError, match="inválido"):
        load_sources(config, tmp_path)

    external = tmp_path.parent / "livro-externo.md"
    external.write_text("conteúdo", encoding="utf-8")
    references = tmp_path / "referencias"
    references.mkdir(exist_ok=True)
    (references / "manual.md").symlink_to(external)
    catalog = write_catalog(tmp_path)
    config = load_config(catalog, tmp_path)
    with pytest.raises(ValueError, match="sai de referencias"):
        load_sources(config, tmp_path)


def test_indice_editorial_nao_descobre_referencias(tmp_path: Path) -> None:
    reference_catalog = write_catalog(tmp_path)
    write_book(tmp_path)
    editorial = {
        "schema_version": 1,
        "source_roots": ["cenario", "campanha", "regras", "apendices"],
        "forbidden_roots": ["referencias", "build"],
        "allowed_statuses": ["canon"],
        "chunker": {"tokenizer": "word", "chunk_size": 30, "min_characters_per_chunk": 10},
        "outputs": {
            "publico": "build/retrieval/chunks-publico.json",
            "mestre": "build/retrieval/chunks-mestre.json",
        },
    }
    editorial_path = tmp_path / "config" / "retrieval.yml"
    editorial_path.write_text(yaml.safe_dump(editorial, sort_keys=False), encoding="utf-8")

    index = build_index(editorial_path, tmp_path, "mestre")

    assert index["sources"] == []
    assert index["chunks"] == []
    assert reference_catalog.is_file()
