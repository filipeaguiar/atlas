from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.identify_images import (
    append_name,
    autocomplete_names,
    load_names,
    normalize_text,
    save_identity,
    select_approved,
)


def test_autocomplete_ignora_acentos_caixa_e_busca_por_palavras() -> None:
    names = ["Véspera", "Caio Ventura — Impacto", "Lívia Monteiro — Métrica"]
    assert normalize_text("VÉSPERA") == "vespera"
    assert autocomplete_names(names, "ves") == ["Véspera"]
    assert autocomplete_names(names, "impact caio") == ["Caio Ventura — Impacto"]


def test_load_names_ignora_comentarios_e_duplicatas(tmp_path: Path) -> None:
    path = tmp_path / "personagens.txt"
    path.write_text("# grupo\nVéspera\n\nvespera\nCustódio\n", encoding="utf-8")
    assert load_names(path) == ["Véspera", "Custódio"]


def test_append_name_persiste_novo_nome_sem_duplicar(tmp_path: Path) -> None:
    path = tmp_path / "personagens.txt"
    path.write_text("# Lista\nVéspera\n", encoding="utf-8")
    assert append_name(path, "  Novo   Herói  ") == "Novo Herói"
    assert append_name(path, "novo heroi") == "Novo Herói"
    assert load_names(path) == ["Véspera", "Novo Herói"]
    assert path.read_text(encoding="utf-8").count("Novo Herói") == 1


def test_select_approved_remove_pendentes_identificados_e_hashes_repetidos() -> None:
    rows = [
        {"id": "a", "decision": "aprovar", "identity": "", "sha256": "1"},
        {"id": "b", "decision": "aprovar", "identity": "", "sha256": "1"},
        {"id": "c", "decision": "aprovar", "identity": "Zero", "sha256": "2"},
        {"id": "d", "decision": "pendente", "identity": "", "sha256": "3"},
    ]
    assert [row["id"] for row in select_approved(rows)] == ["a"]
    assert [row["id"] for row in select_approved(rows, show_all=True)] == ["a", "c"]


def test_save_identity_propaga_para_duplicata_exata(tmp_path: Path) -> None:
    fields = ["id", "sha256", "decision", "identity"]
    rows = [
        {"id": "a", "sha256": "hash", "decision": "aprovar", "identity": ""},
        {"id": "b", "sha256": "hash", "decision": "aprovar", "identity": ""},
    ]
    inventory = {
        "images": [
            {"id": "a", "sha256": "hash", "identity": ""},
            {"id": "b", "sha256": "hash", "identity": ""},
        ]
    }
    csv_path = tmp_path / "curadoria.csv"
    inventory_path = tmp_path / "inventario.json"

    assert save_identity(
        "a",
        "Zero",
        csv_path=csv_path,
        inventory_path=inventory_path,
        fields=fields,
        rows=rows,
        inventory=inventory,
    ) == 2

    with csv_path.open(newline="") as stream:
        saved = list(csv.DictReader(stream))
    saved_inventory = json.loads(inventory_path.read_text())
    assert [row["identity"] for row in saved] == ["Zero", "Zero"]
    assert [item["identity"] for item in saved_inventory["images"]] == ["Zero", "Zero"]
