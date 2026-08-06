from __future__ import annotations

import csv
import json
from pathlib import Path

from tools.curate_images import (
    fit_terminal,
    herdr_graphics_enabled,
    resolve_image,
    save_decision,
    select_rows,
)


def test_fit_terminal_preserva_limites_e_proporcao() -> None:
    columns, rows = fit_terminal(1600, 1000, 100, 30)
    assert columns <= 100
    assert rows <= 30
    assert columns > rows

    columns, rows = fit_terminal(800, 1600, 100, 30)
    assert columns <= 100
    assert rows == 30
    assert columns <= rows


def test_select_rows_filtra_pendentes_lote_e_inicio() -> None:
    rows = [
        {"id": "parte-02-001", "batch": "parte-02", "decision": "pendente"},
        {"id": "parte-02-002", "batch": "parte-02", "decision": "aprovar"},
        {"id": "parte-03-001", "batch": "parte-03", "decision": "pendente"},
        {"id": "parte-03-002", "batch": "parte-03", "decision": "pendente"},
        {"id": "parte-03-003", "batch": "parte-03", "decision": "lixo"},
    ]
    assert [row["id"] for row in select_rows(rows, batch=None, show_all=False, start=None)] == [
        "parte-02-001",
        "parte-03-001",
        "parte-03-002",
    ]
    assert [row["id"] for row in select_rows(rows, batch="03", show_all=False, start="parte-03-002")] == [
        "parte-03-002"
    ]
    assert "parte-03-003" not in [
        row["id"] for row in select_rows(rows, batch=None, show_all=True, start=None)
    ]


def test_detecta_configuracao_grafica_do_herdr(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("HERDR_ENV", "1")
    config = tmp_path / "config.toml"
    config.write_text("[experimental]\nkitty_graphics = false\n")
    assert herdr_graphics_enabled(config) is False
    config.write_text("[experimental]\nkitty_graphics = true\n")
    assert herdr_graphics_enabled(config) is True


def test_resolve_image_usa_caminho_do_inventario_quando_csv_nao_possui_path(tmp_path: Path) -> None:
    image = tmp_path / "lotes" / "parte-02" / "001.png"
    image.parent.mkdir(parents=True)
    image.write_bytes(b"png")
    row = {"id": "parte-02-001", "width": "1024", "height": "1536"}
    inventory = {
        "images": [
            {
                "id": "parte-02-001",
                "path": "lotes/parte-02/001.png",
                "width": 1024,
                "height": 1536,
            }
        ]
    }

    path, width, height = resolve_image(row, inventory, tmp_path)

    assert path == image.resolve()
    assert (width, height) == (1024, 1536)


def test_save_decision_atualiza_csv_e_json_atomicamente(tmp_path: Path) -> None:
    fields = ["id", "decision", "identity", "notes"]
    rows = [{"id": "parte-02-001", "decision": "pendente", "identity": "", "notes": ""}]
    inventory = {"images": [{"id": "parte-02-001", "decision": "pendente"}]}
    csv_path = tmp_path / "curadoria.csv"
    inventory_path = tmp_path / "inventario.json"

    save_decision(
        "parte-02-001",
        "aprovar",
        csv_path=csv_path,
        inventory_path=inventory_path,
        fields=fields,
        rows=rows,
        inventory=inventory,
    )

    with csv_path.open(newline="") as stream:
        saved_rows = list(csv.DictReader(stream))
    saved_inventory = json.loads(inventory_path.read_text())
    assert saved_rows[0]["decision"] == "aprovar"
    assert saved_inventory["images"][0]["decision"] == "aprovar"
    assert saved_inventory["curation_updated_at"]
