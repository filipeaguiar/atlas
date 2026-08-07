from __future__ import annotations

import csv
from pathlib import Path

import yaml

from tools.promote_gallery import CURATION_FILE, DATA_FILE, OUTPUT_ROOT, approved_unique_rows


def test_galeria_declara_somente_aprovadas_identificadas_e_unicas() -> None:
    rows = approved_unique_rows()
    data = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))
    records = data["images"]

    assert data["selection"] == "aprovadas-unicas"
    assert len(rows) == len(records) == 68
    assert {row["id"] for row in rows} == {record["id"] for record in records}
    assert len({record["source_sha256"] for record in records}) == len(records)
    assert all(record["identity"] for record in records)

    with CURATION_FILE.open(encoding="utf-8", newline="") as stream:
        decisions = {row["id"]: row["decision"] for row in csv.DictReader(stream)}
    assert all(decisions[record["id"]] == "aprovar" for record in records)


def test_copias_promovidas_sao_webp_declarados() -> None:
    records = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))["images"]
    declared = {record["file"] for record in records}
    published = {path.name for path in OUTPUT_ROOT.iterdir() if path.is_file()}
    assert published == declared
    for filename in declared:
        content = (OUTPUT_ROOT / filename).read_bytes()
        assert filename.endswith(".webp")
        assert content[:4] == b"RIFF" and content[8:12] == b"WEBP"
