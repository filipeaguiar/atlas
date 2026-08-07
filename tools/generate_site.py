#!/usr/bin/env python3
"""Materializa o manifesto positivo e gera o site Hugo do Mestre."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.materialize_publication import (
    DEFAULT_MANIFEST,
    LINK_RE,
    PROJECT_ROOT,
    Document,
    PublicationError,
    PublicationPlan,
    local_link_target,
    prepare_publication,
)

DEFAULT_HUGO_SOURCE = PROJECT_ROOT / "publicacao" / "hugo"
DEFAULT_STAGE = PROJECT_ROOT / "build" / "hugo"
DEFAULT_DESTINATION = PROJECT_ROOT / "build" / "site"
DEFAULT_REPORT = PROJECT_ROOT / "build" / "relatorio-site.json"
STAT_LINE_RE = re.compile(
    r"^\*\*P(?P<p>\d+),[ \t]*H(?P<h>\d+),[ \t]*R(?P<r>\d+);[ \t]*(?P<resources>[^*\n]+)\*\*[ \t]*$",
    re.MULTILINE,
)
RESOURCE_RE = re.compile(r"(?P<value>\d+)\s*(?P<label>PV|PM|PA)", re.IGNORECASE)
SHEET_HEADING_RE = re.compile(r"^##[ \t]+(?P<title>[^\n]+)$", re.MULTILINE)
TOP_HEADING_RE = re.compile(r"^#[ \t]+[^\n]+\n+", re.MULTILINE)

FORBIDDEN_OUTPUT_MARKERS = (
    "desenvolvimento/",
    "historico/",
    "recuperacao/",
    "referencias/",
    "openspec/",
    "publicacao/stubs/",
    "publicacao/conteudo/",
)


def safe_output(path: Path, root: Path, expected: Path) -> Path:
    resolved = path.resolve()
    if resolved != expected.resolve() or not resolved.is_relative_to(root.resolve()):
        raise PublicationError(f"caminho de saída inseguro: {path}")
    return resolved


def route_for(document: Document) -> str:
    return f"{document.section_id}/{document.metadata['id']}/"


def resource_mapping(plan: PublicationPlan) -> dict[Path, str]:
    return {source.resolve(): name for name, source in plan.resources.items()}


def rewrite_site_links(
    body: str,
    document: Document,
    plan: PublicationPlan,
    resources: dict[Path, str],
    *,
    from_home: bool = False,
) -> str:
    declared = {item.source.resolve(): item for item in plan.documents}

    def replace(match: re.Match[str]) -> str:
        prefix, label, raw = match.groups()
        target_value = local_link_target(raw)
        if target_value is None:
            return match.group(0)
        raw_target = raw.strip().strip("<>").split(maxsplit=1)[0]
        fragment = ""
        if "#" in raw_target:
            fragment = "#" + raw_target.split("#", 1)[1]
        target = (document.source.parent / target_value).resolve()
        if target in declared:
            destination = declared[target]
            href = f"../../{destination.section_id}/{destination.metadata['id']}/{fragment}"
            return f"{prefix}[{label}]({href})"
        if prefix and target in resources:
            prefix_path = "recursos/" if from_home else "../../recursos/"
            return f"![{label}]({prefix_path}{resources[target]})"
        if not target.exists():
            raise PublicationError(
                f"referência ausente durante geração do site: {document.relative_path} -> {raw}"
            )
        return match.group(0)

    return LINK_RE.sub(replace, body)


def render_stat_panels(body: str) -> str:
    """Converte apenas a linha mecânica da cópia Hugo em HTML semântico."""

    def replace(match: re.Match[str]) -> str:
        cells = [
            ("P", match.group("p"), "Poder"),
            ("H", match.group("h"), "Habilidade"),
            ("R", match.group("r"), "Resistência"),
        ]
        cells.extend(
            (item.group("label").upper(), item.group("value"), item.group("label").upper())
            for item in RESOURCE_RE.finditer(match.group("resources"))
        )
        rendered = "".join(
            f'<span class="stat-cell" title="{title}"><b>{label}</b><strong>{value}</strong></span>'
            for label, value, title in cells
        )
        return f'<div class="stat-panel" aria-label="Atributos e recursos">{rendered}</div>'

    return STAT_LINE_RE.sub(replace, body)


def wrap_sheet_cards(body: str, fallback_title: str) -> str:
    """Agrupa cada ficha em um shortcode visual sem alterar a fonte canônica."""
    matches = list(SHEET_HEADING_RE.finditer(body))
    if not matches:
        inner = TOP_HEADING_RE.sub("", body, count=1).strip()
        anchor = re.sub(r"[^a-z0-9]+", "-", fallback_title.casefold()).strip("-")
        return (
            f'{{{{< sheet-card title="{fallback_title}" anchor="{anchor}" >}}}}\n'
            f"{inner}\n{{{{< /sheet-card >}}}}\n"
        )

    output = [body[: matches[0].start()].rstrip(), ""]
    for index, match in enumerate(matches):
        title = match.group("title").strip()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        inner = body[match.end() : end].strip()
        anchor = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")
        output.extend(
            [
                f'{{{{< sheet-card title="{title}" anchor="{anchor}" >}}}}',
                inner,
                "{{< /sheet-card >}}",
                "",
            ]
        )
    return "\n".join(output).strip() + "\n"


def front_matter(data: dict[str, Any]) -> str:
    return "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n\n"


def materialize_hugo(
    plan: PublicationPlan,
    source_root: Path = DEFAULT_HUGO_SOURCE,
    stage_root: Path = DEFAULT_STAGE,
) -> Path:
    source_root = source_root.resolve()
    if not source_root.is_dir() or not source_root.is_relative_to(plan.root):
        raise PublicationError(f"estrutura Hugo ausente ou insegura: {source_root}")
    stage_root = safe_output(stage_root, plan.root, plan.root / "build" / "hugo")
    shutil.rmtree(stage_root, ignore_errors=True)
    shutil.copytree(source_root, stage_root)
    content_root = stage_root / "content"
    static_root = stage_root / "static" / "recursos"
    data_root = stage_root / "data"
    content_root.mkdir(parents=True)
    data_root.mkdir(parents=True, exist_ok=True)

    resources = resource_mapping(plan)
    for source, name in resources.items():
        static_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, static_root / name)

    ordered = list(plan.documents)
    previous_next: dict[str, tuple[Document | None, Document | None]] = {}
    for index, document in enumerate(ordered):
        previous_next[document.relative_path] = (
            ordered[index - 1] if index else None,
            ordered[index + 1] if index + 1 < len(ordered) else None,
        )

    opening_bodies: list[str] = []
    document_records: list[dict[str, Any]] = []
    for section_index, section in enumerate(plan.sections, 1):
        section_root = content_root / section.id
        section_root.mkdir(parents=True)
        (section_root / "_index.md").write_text(
            front_matter(
                {
                    "title": section.title,
                    "weight": section_index,
                    "role": section.role,
                    "description": (
                        "Conteúdo em preparação para uma versão futura."
                        if not section.documents
                        else ""
                    ),
                }
            ),
            encoding="utf-8",
        )
        for document in section.documents:
            previous, following = previous_next[document.relative_path]
            metadata: dict[str, Any] = {
                "title": str(document.metadata["titulo"]),
                "slug": str(document.metadata["id"]),
                "weight": document.order + 1,
                "section_title": section.title,
                "editorial_id": str(document.metadata["id"]),
            }
            for presentation_key in ("tipo", "categoria"):
                if document.metadata.get(presentation_key):
                    metadata[presentation_key] = str(document.metadata[presentation_key])
            if previous:
                metadata["previous"] = {
                    "title": str(previous.metadata["titulo"]),
                    "url": route_for(previous),
                }
            if following:
                metadata["next"] = {
                    "title": str(following.metadata["titulo"]),
                    "url": route_for(following),
                }
            body = rewrite_site_links(document.body, document, plan, resources)
            if document.metadata.get("tipo") == "ficha":
                body = render_stat_panels(body)
                body = wrap_sheet_cards(body, str(document.metadata["titulo"]))
            elif document.metadata.get("tipo") == "galeria":
                body = body.rstrip() + "\n\n{{< gallery >}}\n"
            page_path = section_root / f"{document.metadata['id']}.md"
            page_path.write_text(front_matter(metadata) + body.lstrip(), encoding="utf-8")
            if section.role == "abertura":
                opening_bodies.append(
                    rewrite_site_links(document.body, document, plan, resources, from_home=True)
                )
            document_records.append(
                {
                    "id": document.metadata["id"],
                    "title": document.metadata["titulo"],
                    "section": section.id,
                    "order": document.order,
                    "route": route_for(document),
                    "sha256": document.sha256,
                }
            )

    home_metadata = {
        "title": plan.book.title,
        "description": plan.book.subtitle,
    }
    (content_root / "_index.md").write_text(
        front_matter(home_metadata) + "\n\n".join(opening_bodies).strip() + "\n",
        encoding="utf-8",
    )
    publication_data = {
        "schema_version": 1,
        "book": {
            "title": plan.book.title,
            "subtitle": plan.book.subtitle,
            "version": plan.book.version,
            "language": plan.book.language,
            "status": plan.book.status,
        },
        "manifest": plan.manifest_path.relative_to(plan.root).as_posix(),
        "input_digest": plan.input_digest,
        "documents": document_records,
        "resources": [
            {
                "published": f"recursos/{name}",
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
            for source, name in sorted(resources.items(), key=lambda item: item[1])
        ],
    }
    (data_root / "publication.json").write_text(
        json.dumps(publication_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (stage_root / "hugo.toml").open("a", encoding="utf-8") as config:
        config.write("\n[params]\n")
        config.write(f"subtitle = {json.dumps(plan.book.subtitle, ensure_ascii=False)}\n")
        config.write(f"version = {json.dumps(plan.book.version)}\n")
        config.write(f"status = {json.dumps(plan.book.status)}\n")
    return stage_root


def find_hugo(explicit: str | None = None) -> Path:
    candidate = explicit or os.environ.get("HUGO_BIN") or shutil.which("hugo")
    if not candidate:
        raise PublicationError("Hugo Extended não encontrado; instale Hugo 0.164.0 ou defina HUGO_BIN")
    path = Path(candidate).expanduser().resolve()
    if not path.is_file() or not os.access(path, os.X_OK):
        raise PublicationError(f"executável Hugo inválido: {candidate}")
    result = subprocess.run([str(path), "version"], capture_output=True, text=True, timeout=15)
    description = (result.stdout or result.stderr).strip()
    if result.returncode != 0 or "extended" not in description.lower():
        raise PublicationError(f"Hugo Extended é obrigatório: {description or candidate}")
    return path


def run_hugo(hugo: Path, stage_root: Path, destination: Path, base_url: str) -> list[str]:
    destination = safe_output(destination, PROJECT_ROOT, PROJECT_ROOT / "build" / "site")
    shutil.rmtree(destination, ignore_errors=True)
    command = [
        str(hugo),
        "--source",
        str(stage_root),
        "--destination",
        str(destination),
        "--baseURL",
        base_url.rstrip("/") + "/",
        "--cleanDestinationDir",
        "--minify",
        "--panicOnWarning",
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise PublicationError(f"Hugo falhou: {(result.stderr or result.stdout).strip()}")
    if not (destination / "index.html").is_file():
        raise PublicationError("Hugo não produziu index.html")
    return command


def audit_site(destination: Path) -> None:
    if not destination.is_dir():
        raise PublicationError("saída do site ausente")
    for path in destination.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".pdf":
            raise PublicationError(f"PDF proibido no site: {path.relative_to(destination)}")
        if path.suffix.lower() in {".html", ".xml", ".txt", ".css", ".js", ".json"}:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            for marker in FORBIDDEN_OUTPUT_MARKERS:
                if marker in text:
                    raise PublicationError(
                        f"marcador de área interna no site: {path.relative_to(destination)}: {marker}"
                    )


def generate_site(
    manifest: Path = DEFAULT_MANIFEST,
    root: Path = PROJECT_ROOT,
    *,
    base_url: str = "http://localhost:1313/",
    hugo_bin: str | None = None,
) -> tuple[Path, PublicationPlan]:
    root = root.resolve()
    if root != PROJECT_ROOT.resolve():
        raise PublicationError("o gerador do site opera somente na raiz deste projeto")
    plan = prepare_publication(manifest.resolve(), root, strict=True)
    stage = materialize_hugo(plan)
    destination = root / "build" / "site"
    hugo = find_hugo(hugo_bin)
    command = run_hugo(hugo, stage, destination, base_url)
    audit_site(destination)
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "input_digest": plan.input_digest,
        "base_url": base_url.rstrip("/") + "/",
        "hugo": str(hugo),
        "command": command,
        "documents": len(plan.documents),
        "output": "build/site",
        "pdfs_published": 0,
    }
    DEFAULT_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination, plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--base-url", default="http://localhost:1313/")
    parser.add_argument("--hugo-bin")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        destination, plan = generate_site(
            args.manifest, PROJECT_ROOT, base_url=args.base_url, hugo_bin=args.hugo_bin
        )
    except (OSError, subprocess.SubprocessError, PublicationError, yaml.YAMLError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print(f"Site: {plan.book.title} {plan.book.version}")
    print(f"Documentos: {len(plan.documents)}")
    print(f"Saída: {destination.relative_to(PROJECT_ROOT)}")
    print("PDFs publicados: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
