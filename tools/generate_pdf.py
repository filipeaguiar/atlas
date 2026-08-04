#!/usr/bin/env python3
"""Gera a versão incremental do livro do Mestre em HTML e PDF."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import markdown

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.materialize_publication import (
    DEFAULT_MANIFEST,
    PROJECT_ROOT,
    Materialization,
    PublicationError,
    PublicationPlan,
    materialize,
    prepare_publication,
    rewrite_links,
)

DEFAULT_TEMPLATE = PROJECT_ROOT / "publicacao" / "templates" / "livro.html"
DEFAULT_CSS = PROJECT_ROOT / "publicacao" / "estilos" / "livro.css"
REPORT_PATH = PROJECT_ROOT / "build" / "relatorio-publicacao.json"
CHROME_CANDIDATES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")


def safe_template_path(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise PublicationError(f"{label} deve permanecer dentro do projeto") from exc
    if not resolved.is_file():
        raise PublicationError(f"{label} ausente: {resolved}")
    return resolved


def markdown_to_html(text: str) -> str:
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "footnotes", "attr_list", "md_in_html"],
        output_format="html5",
    )


def metadata_text(value: Any) -> str:
    if isinstance(value, list):
        return "; ".join(str(item) for item in value)
    if isinstance(value, dict):
        return "; ".join(f"{key}: {item}" for key, item in value.items())
    return str(value)


def render_html(
    materialization: Materialization,
    template_path: Path,
    css_path: Path,
) -> Path:
    """Renderiza capa, sumário, capítulos e handouts em um único HTML."""

    plan = materialization.plan
    template_path = safe_template_path(template_path, plan.root, "template")
    css_path = safe_template_path(css_path, plan.root, "CSS")
    template = template_path.read_text(encoding="utf-8")
    css = css_path.read_text(encoding="utf-8")
    required_placeholders = {"{{TITLE}}", "{{CSS}}", "{{COVER}}", "{{TOC}}", "{{CONTENT}}"}
    missing = [placeholder for placeholder in required_placeholders if placeholder not in template]
    if missing:
        raise PublicationError(f"template sem placeholders: {missing}")

    is_development = "dev" in plan.book.version.lower() or plan.book.status == "desenvolvimento"
    development_badge = (
        '<div class="dev-badge">Versão incremental — material em desenvolvimento</div>'
        if is_development
        else ""
    )
    cover = f"""
<section class="cover">
  <div class="cover-kicker">Módulo de campanha para o Mestre</div>
  <h1>{html.escape(plan.book.title)}</h1>
  <h2>{html.escape(plan.book.subtitle)}</h2>
  <div class="cover-meta">
    <div>Versão {html.escape(plan.book.version)}</div>
    {development_badge}
  </div>
</section>
""".strip()

    toc_parts = ['<nav class="toc" id="sumario"><h1>Sumário</h1>']
    for section in plan.sections:
        toc_parts.append(f'<div class="toc-section">{html.escape(section.title)}</div><ul>')
        if section.documents:
            for document in section.documents:
                toc_parts.append(
                    f'<li><a href="#{html.escape(document.anchor)}">'
                    f'{html.escape(str(document.metadata["titulo"]))}</a></li>'
                )
        else:
            toc_parts.append("<li><em>Em preparação</em></li>")
        toc_parts.append("</ul>")
    toc_parts.append("</nav>")
    toc = "\n".join(toc_parts)

    resource_names = {
        (plan.root / record["source"]).resolve(): Path(record["materialized"]).name
        for record in materialization.resource_records
    }
    content_parts: list[str] = []
    for index, section in enumerate(plan.sections, 1):
        content_parts.append(
            f'<section class="section-divider" id="secao-{html.escape(section.id)}">'
            f'<div class="section-number">Seção {index}</div>'
            f'<h1>{html.escape(section.title)}</h1>'
            + ("<p>Conteúdo em preparação para uma versão futura.</p>" if not section.documents else "")
            + "</section>"
        )
        for document in section.documents:
            body = rewrite_links(document.body, document, plan, resource_names)
            rendered = markdown_to_html(body)
            if section.role == "handouts":
                content_parts.append(
                    f'<article class="handout-instructions" id="{html.escape(document.anchor)}">'
                    '<div class="master-note">'
                    f'<h1>Orientação do Mestre — {html.escape(str(document.metadata["titulo"]))}</h1>'
                    "<dl>"
                    f'<dt>Como usar</dt><dd>{html.escape(metadata_text(document.metadata["orientacao_mestre"]))}</dd>'
                    f'<dt>Quando entregar</dt><dd>{html.escape(metadata_text(document.metadata["entregar_quando"]))}</dd>'
                    f'<dt>O que revela</dt><dd>{html.escape(metadata_text(document.metadata["revela"]))}</dd>'
                    "</dl></div></article>"
                )
                content_parts.append(
                    '<article class="handout-page">'
                    '<div class="handout-label">Material para entregar aos jogadores a critério do Mestre</div>'
                    f"{rendered}</article>"
                )
            else:
                content_parts.append(
                    f'<article class="chapter" id="{html.escape(document.anchor)}">{rendered}</article>'
                )
    content = "\n".join(content_parts)

    document = (
        template.replace("{{TITLE}}", html.escape(f"{plan.book.title} — {plan.book.version}"))
        .replace("{{CSS}}", css)
        .replace("{{COVER}}", cover)
        .replace("{{TOC}}", toc)
        .replace("{{CONTENT}}", content)
    )
    html_path = materialization.content_root / "livro.html"
    html_path.write_text(document, encoding="utf-8")
    if html_path.stat().st_size < 1000:
        raise PublicationError("HTML gerado está vazio ou incompleto")
    return html_path


def find_chrome(explicit: str | None = None) -> Path:
    candidate = explicit or os.environ.get("CHROME_BIN")
    if candidate:
        resolved = Path(candidate).expanduser().resolve()
        if not resolved.is_file() or not os.access(resolved, os.X_OK):
            raise PublicationError(f"CHROME_BIN não aponta para executável válido: {candidate}")
        return resolved
    for name in CHROME_CANDIDATES:
        found = shutil.which(name)
        if found:
            return Path(found).resolve()
    raise PublicationError(
        "Google Chrome/Chromium não encontrado; configure CHROME_BIN=/caminho/do/executavel"
    )


def chrome_version(chrome: Path) -> str:
    try:
        result = subprocess.run(
            [str(chrome), "--version"], capture_output=True, text=True, check=True, timeout=15
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PublicationError(f"não foi possível consultar a versão do Chrome: {exc}") from exc
    return (result.stdout or result.stderr).strip()


def render_pdf(chrome: Path, html_path: Path, pdf_path: Path, root: Path) -> list[str]:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_path.unlink(missing_ok=True)
    profile = root / "build" / ".chrome-publication"
    shutil.rmtree(profile, ignore_errors=True)
    command = [
        str(chrome),
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as exc:
        raise PublicationError(f"falha ao executar Chrome: {exc}") from exc
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise PublicationError(f"Chrome encerrou com código {result.returncode}: {detail}")
    if not pdf_path.is_file() or pdf_path.stat().st_size < 1000:
        raise PublicationError("Chrome não produziu um PDF válido e não vazio")
    return command


def artifact_record(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(root).as_posix(),
        "size": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def write_report(
    plan: PublicationPlan,
    materialization: Materialization,
    html_path: Path,
    pdf_path: Path,
    chrome: Path,
    chrome_description: str,
    command: list[str],
) -> Path:
    report_path = plan.root / "build" / "relatorio-publicacao.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    documents = [
        {
            "source": document.relative_path,
            "id": document.metadata["id"],
            "title": document.metadata["titulo"],
            "section": document.section_id,
            "role": document.section_role,
            "order": document.order,
            "sha256": document.sha256,
        }
        for document in plan.documents
    ]
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "book": {
            "title": plan.book.title,
            "subtitle": plan.book.subtitle,
            "version": plan.book.version,
            "language": plan.book.language,
            "status": plan.book.status,
        },
        "mode": "strict" if plan.strict else "incremental",
        "input_digest": plan.input_digest,
        "manifest": plan.manifest_path.relative_to(plan.root).as_posix(),
        "chrome": {"path": str(chrome), "version": chrome_description, "command": command},
        "documents": documents,
        "issues": [issue.__dict__ for issue in plan.issues],
        "resources": materialization.resource_records,
        "artifacts": [
            artifact_record(materialization.summary_path, plan.root),
            artifact_record(materialization.combined_path, plan.root),
            artifact_record(materialization.metadata_path, plan.root),
            artifact_record(html_path, plan.root),
            artifact_record(pdf_path, plan.root),
        ],
    }
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return report_path


def generate(
    manifest_path: Path,
    root: Path,
    *,
    strict: bool = False,
    template_path: Path | None = None,
    css_path: Path | None = None,
    chrome_path: str | None = None,
) -> tuple[Path, Path, PublicationPlan]:
    root = root.resolve()
    plan = prepare_publication(manifest_path, root, strict=strict)
    pdf_path = root / "build" / f"{plan.book.basename}-{plan.book.version}.pdf"
    report_path = root / "build" / "relatorio-publicacao.json"
    pdf_path.unlink(missing_ok=True)
    report_path.unlink(missing_ok=True)
    materialization = materialize(plan)
    html_path = render_html(
        materialization,
        template_path or root / "publicacao" / "templates" / "livro.html",
        css_path or root / "publicacao" / "estilos" / "livro.css",
    )
    chrome = find_chrome(chrome_path)
    description = chrome_version(chrome)
    command = render_pdf(chrome, html_path, pdf_path, root)
    report = write_report(
        plan, materialization, html_path, pdf_path, chrome, description, command
    )
    return pdf_path, report, plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--chrome", help="sobrescreve CHROME_BIN")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        pdf, report, plan = generate(
            args.manifest,
            args.root,
            strict=args.strict,
            chrome_path=args.chrome,
        )
    except (OSError, PublicationError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print(f"Livro do Mestre: {plan.book.title} {plan.book.version}")
    print(f"Modo: {'estrito' if plan.strict else 'incremental'}")
    print(f"Documentos: {len(plan.documents)}")
    print(f"Pendências locais: {len(plan.issues)}")
    print(f"PDF: {pdf.relative_to(plan.root)}")
    print(f"Relatório: {report.relative_to(plan.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
