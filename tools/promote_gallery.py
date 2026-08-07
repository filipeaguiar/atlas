#!/usr/bin/env python3
"""Promove cópias otimizadas das imagens explicitamente aprovadas para a galeria."""

from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
import subprocess
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURATION_ROOT = PROJECT_ROOT / "desenvolvimento" / "curadoria" / "imagens-3det-victory"
CURATION_FILE = CURATION_ROOT / "curadoria.csv"
OUTPUT_ROOT = PROJECT_ROOT / "publicacao" / "hugo" / "static" / "images" / "galeria"
DATA_FILE = PROJECT_ROOT / "publicacao" / "hugo" / "data" / "gallery.yml"


def approved_unique_rows() -> list[dict[str, str]]:
    with CURATION_FILE.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    approved: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in rows:
        if row["decision"] != "aprovar" or row["sha256"] in seen:
            continue
        if not row["identity"]:
            raise RuntimeError(f"imagem aprovada sem identidade: {row['id']}")
        seen.add(row["sha256"])
        approved.append(row)
    return approved


def promote() -> list[dict[str, str]]:
    magick = shutil.which("magick")
    if not magick:
        raise RuntimeError("ImageMagick não encontrado")
    rows = approved_unique_rows()
    shutil.rmtree(OUTPUT_ROOT, ignore_errors=True)
    OUTPUT_ROOT.mkdir(parents=True)
    records: list[dict[str, str]] = []
    for row in rows:
        source = CURATION_ROOT / "lotes" / row["batch"] / row["filename"]
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256"]:
            raise RuntimeError(f"fonte ausente ou alterada: {row['id']}")
        filename = f"{row['id']}.webp"
        destination = OUTPUT_ROOT / filename
        subprocess.run(
            [magick, str(source), "-auto-orient", "-resize", "1200x1200>", "-strip", "-quality", "82", "-define", "webp:method=6", str(destination)],
            check=True,
        )
        records.append(
            {
                "id": row["id"],
                "identity": row["identity"],
                "file": filename,
                "source_sha256": row["sha256"],
            }
        )
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        yaml.safe_dump(
            {"schema_version": 1, "selection": "aprovadas-unicas", "images": records},
            allow_unicode=True,
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    records = promote()
    print(f"Galeria promovida: {len(records)} imagens únicas aprovadas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
