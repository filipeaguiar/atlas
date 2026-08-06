#!/usr/bin/env python3
"""Curadoria interativa de imagens usando o Kitty graphics protocol."""

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import shutil
import sys
import termios
import tty
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = PROJECT_ROOT / "desenvolvimento" / "curadoria" / "imagens-3det-victory"


def fit_terminal(width: int, height: int, max_columns: int, max_rows: int) -> tuple[int, int]:
    """Calcula uma caixa que preserva proporção, assumindo células 1:2."""
    if width <= 0 or height <= 0:
        return max(1, max_columns), max(1, max_rows)
    max_columns = max(1, max_columns)
    max_rows = max(1, max_rows)
    aspect = width / height
    columns = round(2 * max_rows * aspect)
    if columns <= max_columns:
        return max(1, columns), max_rows
    rows = round(max_columns / (2 * aspect))
    return max_columns, max(1, min(rows, max_rows))


def kitty_delete_all() -> None:
    sys.stdout.write("\x1b_Ga=d,d=A,q=2\x1b\\")
    sys.stdout.flush()


def kitty_display(path: Path, columns: int, rows: int) -> None:
    """Transmite um PNG ao terminal em blocos do Kitty graphics protocol."""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    chunks = [encoded[index : index + 4096] for index in range(0, len(encoded), 4096)]
    for index, chunk in enumerate(chunks):
        more = 1 if index < len(chunks) - 1 else 0
        if index == 0:
            controls = f"a=T,f=100,q=2,c={columns},r={rows},m={more}"
        else:
            controls = f"q=2,m={more}"
        sys.stdout.write(f"\x1b_G{controls};{chunk}\x1b\\")
    sys.stdout.flush()


def herdr_graphics_enabled(config_path: Path | None = None) -> bool:
    if not os.environ.get("HERDR_ENV"):
        return True
    path = config_path or Path(
        os.environ.get("HERDR_CONFIG_PATH", Path.home() / ".config" / "herdr" / "config.toml")
    )
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return False
    return data.get("experimental", {}).get("kitty_graphics") is True


def read_key() -> str:
    if not sys.stdin.isatty():
        raise RuntimeError("a entrada padrão precisa ser um terminal interativo")
    descriptor = sys.stdin.fileno()
    previous = termios.tcgetattr(descriptor)
    try:
        tty.setraw(descriptor)
        key = os.read(descriptor, 1).decode("utf-8", errors="ignore")
    finally:
        termios.tcsetattr(descriptor, termios.TCSADRAIN, previous)
    if key == "\x03":
        raise KeyboardInterrupt
    return key


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError("curadoria.csv não possui cabeçalho")
        return list(reader.fieldnames), list(reader)


def atomic_write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def save_decision(
    image_id: str,
    decision: str,
    *,
    csv_path: Path,
    inventory_path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
    inventory: dict[str, Any],
) -> None:
    csv_matches = [row for row in rows if row.get("id") == image_id]
    json_matches = [item for item in inventory.get("images", []) if item.get("id") == image_id]
    if len(csv_matches) != 1 or len(json_matches) != 1:
        raise ValueError(f"ID inconsistente nos inventários: {image_id}")
    csv_matches[0]["decision"] = decision
    json_matches[0]["decision"] = decision
    inventory["curation_updated_at"] = datetime.now(UTC).isoformat()
    atomic_write_csv(csv_path, fields, rows)
    atomic_write_json(inventory_path, inventory)


def resolve_image(
    row: dict[str, str], inventory: dict[str, Any], project_root: Path = PROJECT_ROOT
) -> tuple[Path, int, int]:
    matches = [item for item in inventory.get("images", []) if item.get("id") == row.get("id")]
    if len(matches) != 1:
        raise ValueError(f"ID ausente ou duplicado no inventário: {row.get('id')}")
    record = matches[0]
    relative_path = row.get("path") or record.get("path")
    if not relative_path:
        raise ValueError(f"imagem sem caminho registrado: {row.get('id')}")
    path = (project_root / relative_path).resolve()
    if not path.is_file() or not path.is_relative_to(project_root.resolve()):
        raise ValueError(f"imagem ausente ou fora do projeto: {relative_path}")
    try:
        width = int(row.get("width") or record["width"])
        height = int(row.get("height") or record["height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"dimensões inválidas: {row.get('id')}") from exc
    return path, width, height


def select_rows(
    rows: list[dict[str, str]], *, batch: str | None, show_all: bool, start: str | None
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if row.get("decision", "pendente") != "lixo"
        and (show_all or row.get("decision", "pendente") == "pendente")
    ]
    if batch:
        normalized = batch if batch.startswith("parte-") else f"parte-{batch}"
        selected = [row for row in selected if row.get("batch") == normalized]
    if start:
        positions = [index for index, row in enumerate(selected) if row.get("id") == start]
        if not positions:
            raise ValueError(f"ID inicial não encontrado na seleção: {start}")
        selected = selected[positions[0] :]
    return selected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="raiz da curadoria")
    parser.add_argument("--batch", help="restringe a um lote, por exemplo 02 ou parte-02")
    parser.add_argument("--start", help="começa em um ID específico")
    parser.add_argument(
        "--all", action="store_true", help="também mostra itens já decididos, exceto lixo"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    csv_path = root / "curadoria.csv"
    inventory_path = root / "inventario.json"
    try:
        fields, rows = load_rows(csv_path)
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        selected = select_rows(rows, batch=args.batch, show_all=args.all, start=args.start)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    if not selected:
        print("Nenhuma imagem corresponde à seleção.")
        return 0
    if not sys.stdout.isatty() or not sys.stdin.isatty():
        print("ERRO: execute em um terminal interativo com suporte ao Kitty graphics protocol.", file=sys.stderr)
        return 1
    if os.environ.get("HERDR_ENV") and not herdr_graphics_enabled():
        print(
            "ERRO: gráficos estão desativados no Herdr. Adicione ao ~/.config/herdr/config.toml:\n\n"
            "[experimental]\nkitty_graphics = true\n\n"
            "Depois execute: herdr server reload-config",
            file=sys.stderr,
        )
        return 1
    if "kitty" not in os.environ.get("TERM", "").lower() and not os.environ.get("KITTY_WINDOW_ID"):
        print("AVISO: o terminal não se identifica como Kitty; a imagem pode não ser exibida.")

    approved = 0
    discarded = 0
    skipped = 0
    sys.stdout.write("\x1b[?1049h\x1b[?25l")
    sys.stdout.flush()
    try:
        for index, row in enumerate(selected, 1):
            path, width, height = resolve_image(row, inventory)
            terminal = shutil.get_terminal_size((100, 32))
            image_columns, image_rows = fit_terminal(
                width, height, max(20, terminal.columns - 2), max(5, terminal.lines - 8)
            )
            kitty_delete_all()
            sys.stdout.write("\x1b[2J\x1b[H")
            sys.stdout.write(
                f"[{index}/{len(selected)}] {row['id']}  •  {row['batch']}\n"
                f"Arquivo: {row['filename']}\n"
                f"Original: {row['original_name']}\n"
                f"Dimensões: {row['width']}×{row['height']}  •  decisão atual: {row['decision']}\n\n"
            )
            sys.stdout.flush()
            kitty_display(path, image_columns, image_rows)
            # A imagem começa na linha 6. O protocolo pode mover o cursor por
            # conta própria; posicioná-lo de forma absoluta evita deslocamento
            # duplicado, linhas vazias e rolagem da tela.
            controls_row = min(terminal.lines, 6 + image_rows)
            sys.stdout.write(f"\x1b[{controls_row};1H")
            sys.stdout.write("[s] aprovar   [l] lixo   [espaço] pular   [q] sair")
            sys.stdout.flush()
            while True:
                key = read_key()
                if key.lower() == "s":
                    save_decision(
                        row["id"],
                        "aprovar",
                        csv_path=csv_path,
                        inventory_path=inventory_path,
                        fields=fields,
                        rows=rows,
                        inventory=inventory,
                    )
                    approved += 1
                    break
                if key.lower() == "l":
                    save_decision(
                        row["id"],
                        "lixo",
                        csv_path=csv_path,
                        inventory_path=inventory_path,
                        fields=fields,
                        rows=rows,
                        inventory=inventory,
                    )
                    discarded += 1
                    break
                if key == " ":
                    skipped += 1
                    break
                if key.lower() == "q":
                    return 0
    except KeyboardInterrupt:
        return 130
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"\nERRO: {exc}", file=sys.stderr)
        return 1
    finally:
        kitty_delete_all()
        sys.stdout.write("\x1b[?25h\x1b[?1049l")
        sys.stdout.flush()
    print(
        f"Curadoria encerrada: {approved} aprovada(s), "
        f"{discarded} marcada(s) como lixo, {skipped} pulada(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
