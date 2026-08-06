#!/usr/bin/env python3
"""Associa personagens às imagens aprovadas com autocomplete no terminal."""

from __future__ import annotations

import argparse
import json
import os
import select
import shutil
import sys
import termios
import tty
import unicodedata
from pathlib import Path
from typing import Any

# Ao executar `python tools/identify_images.py`, Python inclui apenas `tools/`
# no caminho de módulos. Incluímos a raiz para manter os mesmos imports usados
# pelos testes e pela execução com `python -m`.
ANSI_CYAN_BOLD = "\x1b[1;36m"
ANSI_RESET = "\x1b[0m"

SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_PROJECT_ROOT))

from tools.curate_images import (
    DEFAULT_ROOT,
    PROJECT_ROOT,
    atomic_write_csv,
    atomic_write_json,
    fit_terminal,
    herdr_graphics_enabled,
    kitty_delete_all,
    kitty_display,
    load_rows,
    resolve_image,
)


def normalize_text(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


def autocomplete_names(names: list[str], query: str) -> list[str]:
    """Filtra por todas as palavras digitadas, ignorando acentos e caixa."""
    terms = normalize_text(query).split()
    matches = [name for name in names if all(term in normalize_text(name) for term in terms)]
    normalized_query = normalize_text(query).strip()
    return sorted(
        matches,
        key=lambda name: (
            not normalize_text(name).startswith(normalized_query),
            normalize_text(name),
        ),
    )


def load_names(path: Path) -> list[str]:
    names = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not names:
        raise ValueError(f"lista de personagens vazia: {path}")
    unique: dict[str, str] = {}
    for name in names:
        unique.setdefault(normalize_text(name), name)
    return list(unique.values())


def append_name(path: Path, name: str) -> str:
    clean_name = " ".join(name.strip().split())
    if not clean_name or "\n" in name or "\r" in name:
        raise ValueError("nome de personagem inválido")
    existing = load_names(path)
    match = next(
        (candidate for candidate in existing if normalize_text(candidate) == normalize_text(clean_name)),
        None,
    )
    if match:
        return match
    content = path.read_text(encoding="utf-8")
    marker = "# Adicionados durante a identificação"
    if marker not in content:
        content = content.rstrip() + f"\n\n{marker}\n"
    content += clean_name + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.replace(path)
    return clean_name


def select_approved(
    rows: list[dict[str, str]], *, show_all: bool = False, start: str | None = None
) -> list[dict[str, str]]:
    selected = [
        row
        for row in rows
        if row.get("decision") == "aprovar" and (show_all or not row.get("identity", "").strip())
    ]
    if start:
        positions = [index for index, row in enumerate(selected) if row.get("id") == start]
        if not positions:
            raise ValueError(f"ID inicial não encontrado na seleção: {start}")
        selected = selected[positions[0] :]
    unique: list[dict[str, str]] = []
    hashes: set[str] = set()
    for row in selected:
        fingerprint = row.get("sha256") or row.get("id", "")
        if fingerprint not in hashes:
            hashes.add(fingerprint)
            unique.append(row)
    return unique


def save_identity(
    image_id: str,
    identity: str,
    *,
    csv_path: Path,
    inventory_path: Path,
    fields: list[str],
    rows: list[dict[str, str]],
    inventory: dict[str, Any],
) -> int:
    csv_matches = [row for row in rows if row.get("id") == image_id]
    json_matches = [item for item in inventory.get("images", []) if item.get("id") == image_id]
    if len(csv_matches) != 1 or len(json_matches) != 1:
        raise ValueError(f"ID inconsistente nos inventários: {image_id}")
    fingerprint = csv_matches[0].get("sha256")
    affected_csv = [
        row
        for row in rows
        if row.get("id") == image_id or (fingerprint and row.get("sha256") == fingerprint)
    ]
    affected_json = [
        item
        for item in inventory.get("images", [])
        if item.get("id") == image_id or (fingerprint and item.get("sha256") == fingerprint)
    ]
    for row in affected_csv:
        row["identity"] = identity
    for item in affected_json:
        item["identity"] = identity
    atomic_write_csv(csv_path, fields, rows)
    atomic_write_json(inventory_path, inventory)
    return len(affected_csv)


def read_input_key() -> str:
    descriptor = sys.stdin.fileno()
    first = os.read(descriptor, 1)
    if first == b"\x03":
        raise KeyboardInterrupt
    if first == b"\x1b":
        sequence = first
        while select.select([descriptor], [], [], 0.025)[0] and len(sequence) < 3:
            sequence += os.read(descriptor, 1)
        return sequence.decode("ascii", errors="ignore")

    leading = first[0]
    expected = 1
    if leading & 0b11110000 == 0b11110000:
        expected = 4
    elif leading & 0b11100000 == 0b11100000:
        expected = 3
    elif leading & 0b11000000 == 0b11000000:
        expected = 2
    encoded = first
    while len(encoded) < expected:
        encoded += os.read(descriptor, 1)
    return encoded.decode("utf-8", errors="ignore")


def clear_line(row: int) -> None:
    sys.stdout.write(f"\x1b[{row};1H\x1b[2K")


def prompt_identity(names: list[str], prompt_row: int, terminal_lines: int) -> str | None:
    query = ""
    selected = 0
    selection_active = False
    message = ""
    suggestion_limit = max(1, min(6, terminal_lines - prompt_row - 2))
    descriptor = sys.stdin.fileno()
    previous = termios.tcgetattr(descriptor)
    try:
        tty.setraw(descriptor)
        while True:
            matches = autocomplete_names(names, query)
            if matches:
                selected %= min(len(matches), suggestion_limit)
            else:
                selected = 0
            for row in range(prompt_row, terminal_lines + 1):
                clear_line(row)
            clear_line(prompt_row)
            sys.stdout.write(f"Personagem: {query}")
            for offset, name in enumerate(matches[:suggestion_limit], 1):
                clear_line(prompt_row + offset)
                marker = "›" if selection_active and offset - 1 == selected else " "
                sys.stdout.write(f"{marker} {name}")
            help_row = min(terminal_lines, prompt_row + suggestion_limit + 1)
            clear_line(help_row)
            sys.stdout.write(
                message
                or "↑↓/Tab seleciona • Enter confirma • Enter vazio pula • Esc sai"
            )
            sys.stdout.write(f"\x1b[{prompt_row};{len('Personagem: ') + len(query) + 1}H")
            sys.stdout.flush()

            key = read_input_key()
            message = ""
            if key in ("\r", "\n"):
                if not query.strip() and not selection_active:
                    return ""
                exact = next(
                    (name for name in names if normalize_text(name) == normalize_text(query).strip()),
                    None,
                )
                if exact:
                    return exact
                if selection_active and matches:
                    return matches[selected]
                if query.strip():
                    return " ".join(query.strip().split())
                message = "Digite um novo nome ou selecione uma sugestão."
            elif key in ("\x1b",):
                return None
            elif key in ("\t", "\x1b[B"):
                if matches:
                    if selection_active:
                        selected = (selected + 1) % min(len(matches), suggestion_limit)
                    else:
                        selected = 0
                        selection_active = True
            elif key == "\x1b[A":
                if matches:
                    if selection_active:
                        selected = (selected - 1) % min(len(matches), suggestion_limit)
                    else:
                        selected = min(len(matches), suggestion_limit) - 1
                        selection_active = True
            elif key in ("\x7f", "\b"):
                query = query[:-1]
                selected = 0
                selection_active = False
            elif key.isprintable():
                query += key
                selected = 0
                selection_active = False
    finally:
        termios.tcsetattr(descriptor, termios.TCSADRAIN, previous)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="raiz da curadoria")
    parser.add_argument("--names", type=Path, help="lista alternativa de personagens")
    parser.add_argument("--start", help="começa em um ID específico")
    parser.add_argument("--all", action="store_true", help="também permite reidentificar imagens")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    csv_path = root / "curadoria.csv"
    inventory_path = root / "inventario.json"
    names_path = (args.names or root / "personagens.txt").resolve()
    try:
        fields, rows = load_rows(csv_path)
        inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
        names = load_names(names_path)
        selected = select_approved(rows, show_all=args.all, start=args.start)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    if not selected:
        print("Nenhuma imagem aprovada aguarda identificação.")
        return 0
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("ERRO: execute em um terminal interativo.", file=sys.stderr)
        return 1
    if os.environ.get("HERDR_ENV") and not herdr_graphics_enabled():
        print("ERRO: ative [experimental] kitty_graphics = true no Herdr.", file=sys.stderr)
        return 1

    identified = 0
    skipped = 0
    sys.stdout.write("\x1b[?1049h\x1b[?25l")
    sys.stdout.flush()
    try:
        for index, row in enumerate(selected, 1):
            if row.get("identity", "").strip() and not args.all:
                continue
            path, width, height = resolve_image(row, inventory, PROJECT_ROOT)
            terminal = shutil.get_terminal_size((100, 32))
            image_columns, image_rows = fit_terminal(
                width, height, max(20, terminal.columns - 2), max(5, terminal.lines - 15)
            )
            kitty_delete_all()
            sys.stdout.write("\x1b[2J\x1b[H")
            current_identity = row.get("identity") or "não identificada"
            sys.stdout.write(
                f"[{index}/{len(selected)}] {row['id']} • {row['batch']}\n"
                f"Arquivo: {row['filename']}\n"
                f"Original: {row['original_name']}\n"
                f"Identidade atual: {ANSI_CYAN_BOLD}{current_identity}{ANSI_RESET}\n\n"
            )
            sys.stdout.flush()
            kitty_display(path, image_columns, image_rows)
            identity = prompt_identity(names, min(terminal.lines, 6 + image_rows), terminal.lines)
            if identity is None:
                break
            if not identity:
                skipped += 1
                continue
            known_identity = next(
                (name for name in names if normalize_text(name) == normalize_text(identity)), None
            )
            if known_identity:
                identity = known_identity
            else:
                identity = append_name(names_path, identity)
                names.append(identity)
            save_identity(
                row["id"],
                identity,
                csv_path=csv_path,
                inventory_path=inventory_path,
                fields=fields,
                rows=rows,
                inventory=inventory,
            )
            identified += 1
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
        f"Identificação encerrada: {identified} imagem(ns) identificada(s), "
        f"{skipped} pulada(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
