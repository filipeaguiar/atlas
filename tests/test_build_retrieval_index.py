from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from tools.build_retrieval_index import build_index, write_index


def write_config(root: Path, **overrides) -> Path:
    data = {
        "schema_version": 1,
        "source_roots": ["cenario", "campanha", "regras", "apendices"],
        "forbidden_roots": [
            "desenvolvimento",
            "historico",
            "recuperacao",
            "publicacao/stubs",
            "publicacao/conteudo",
            "build",
        ],
        "allowed_statuses": ["canon"],
        "chunker": {"tokenizer": "word", "chunk_size": 40, "min_characters_per_chunk": 10},
        "outputs": {
            "publico": "build/retrieval/chunks-publico.json",
            "mestre": "build/retrieval/chunks-mestre.json",
        },
    }
    data.update(overrides)
    path = root / "config" / "retrieval.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def write_document(path: Path, *, title: str, status: str = "canon", **metadata) -> None:
    front = {"id": title.lower().replace(" ", "-"), "titulo": title, "status": status, **metadata}
    body = (
        f"# {title}\n\n"
        + "Este é um parágrafo editorial aprovado com contexto suficiente para indexação. " * 8
        + "\n\n## Segunda seção\n\n"
        + "Outro trecho preserva a estrutura do documento e sua proveniência. " * 6
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False) + "---\n" + body,
        encoding="utf-8",
    )


def test_isola_audiencias_e_ignora_fontes_nao_aprovadas(tmp_path: Path) -> None:
    config = write_config(tmp_path)
    write_document(tmp_path / "cenario" / "publico.md", title="Documento público", publicar=True)
    write_document(
        tmp_path / "campanha" / "segredo.md",
        title="Segredo do Mestre",
        camada="mestre",
        conteudo_para_jogadores=False,
        publicar=True,
    )
    write_document(
        tmp_path / "cenario" / "pendente.md",
        title="Marcador",
        status="recuperacao-pendente",
        publicar=False,
    )
    write_document(
        tmp_path / "regras" / "nao-publicar.md",
        title="Documento interno",
        publicar=False,
    )

    public = build_index(config, tmp_path, "publico")
    master = build_index(config, tmp_path, "mestre")

    assert {item["path"] for item in public["sources"]} == {"cenario/publico.md"}
    assert {item["path"] for item in master["sources"]} == {
        "campanha/segredo.md",
        "cenario/publico.md",
    }
    assert all(chunk["metadata"]["status"] == "canon" for chunk in master["chunks"])
    assert all(chunk["source_path"] != "campanha/segredo.md" for chunk in public["chunks"])
    ignored = {item["path"]: item["reason"] for item in public["ignored"]}
    assert "conteúdo restrito ao Mestre" in ignored["campanha/segredo.md"]
    assert "status não autorizado" in ignored["cenario/pendente.md"]
    assert ignored["regras/nao-publicar.md"] == "publicar: false"


def test_fragmentos_sao_deterministicos_e_preservam_proveniencia(tmp_path: Path) -> None:
    config = write_config(tmp_path)
    source = tmp_path / "cenario" / "capitulo.md"
    write_document(source, title="Capítulo Canônico", origem="reescrita-aprovada", publicar=True)

    first = build_index(config, tmp_path, "publico")
    second = build_index(config, tmp_path, "publico")

    assert first == second
    assert len(first["chunks"]) > 1
    for chunk in first["chunks"]:
        assert len(chunk["id"]) == 64
        assert chunk["source_path"] == "cenario/capitulo.md"
        assert chunk["source_sha256"] == first["sources"][0]["sha256"]
        assert chunk["heading"] in {"Capítulo Canônico", "Segunda seção"}
        assert chunk["source_start_index"] < chunk["source_end_index"]
        assert chunk["text"]

    output = write_index(first, config, tmp_path)
    assert output == tmp_path / "build" / "retrieval" / "chunks-publico.json"
    assert json.loads(output.read_text(encoding="utf-8")) == first


def test_recusa_caminhos_fora_da_raiz_e_outputs_nao_derivados(tmp_path: Path) -> None:
    external = tmp_path.parent / "Atlas.bkp"
    external.mkdir(exist_ok=True)
    bad_source = write_config(tmp_path, source_roots=["../Atlas.bkp"])
    with pytest.raises(ValueError, match="sai da raiz"):
        build_index(bad_source, tmp_path, "publico")

    safe_config = write_config(tmp_path)
    write_document(tmp_path / "cenario" / "capitulo.md", title="Capítulo", publicar=True)
    index = build_index(safe_config, tmp_path, "publico")
    bad_output = write_config(
        tmp_path,
        outputs={"publico": "indice.json", "mestre": "build/retrieval/chunks-mestre.json"},
    )
    with pytest.raises(ValueError, match="build/retrieval"):
        write_index(index, bad_output, tmp_path)


def test_ignora_markdown_sem_front_matter(tmp_path: Path) -> None:
    config = write_config(tmp_path)
    path = tmp_path / "apendices" / "rascunho.md"
    path.parent.mkdir(parents=True)
    path.write_text("# Rascunho\n\nSem metadados.", encoding="utf-8")

    index = build_index(config, tmp_path, "mestre")

    assert index["sources"] == []
    assert index["chunks"] == []
    assert index["ignored"] == [{"path": "apendices/rascunho.md", "reason": "front matter ausente"}]
