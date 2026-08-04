#!/usr/bin/env python3
"""Valida e materializa a lista positiva do livro do Mestre."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "publicacao" / "manifest.yml"
ALLOWED_SOURCE_PREFIXES = ("cenario/", "campanha/", "regras/", "apendices/", "publicacao/fontes/")
FORBIDDEN_SOURCE_PREFIXES = (
    "referencias/",
    "desenvolvimento/",
    "historico/",
    "recuperacao/",
    "publicacao/stubs/",
    "publicacao/conteudo/",
    "build/",
    "openspec/",
)
SAFE_NAME = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


class PublicationError(ValueError):
    """Erro editorial que impede materialização."""


@dataclass(frozen=True)
class Book:
    title: str
    subtitle: str
    version: str
    language: str
    basename: str
    status: str


@dataclass
class Document:
    source: Path
    relative_path: str
    section_id: str
    section_title: str
    section_role: str
    metadata: dict[str, Any]
    body: str
    body_offset: int
    sha256: str
    anchor: str
    order: int


@dataclass
class Section:
    id: str
    title: str
    role: str
    documents: list[Document] = field(default_factory=list)


@dataclass(frozen=True)
class LinkIssue:
    source: str
    target: str
    kind: str
    message: str


@dataclass
class PublicationPlan:
    root: Path
    manifest_path: Path
    book: Book
    sections: list[Section]
    documents: list[Document]
    issues: list[LinkIssue]
    resources: dict[str, Path]
    input_digest: str
    strict: bool


@dataclass
class Materialization:
    plan: PublicationPlan
    content_root: Path
    summary_path: Path
    combined_path: Path
    metadata_path: Path
    resource_records: list[dict[str, str]]


def is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def safe_project_path(root: Path, value: str, *, label: str) -> Path:
    if not value or Path(value).is_absolute():
        raise PublicationError(f"{label} inválido: {value!r}")
    candidate = (root / value).resolve()
    if not is_inside(candidate, root):
        raise PublicationError(f"{label} sai da raiz do projeto: {value}")
    return candidate


def split_front_matter(text: str, relative_path: str) -> tuple[dict[str, Any], str, int]:
    if not text.startswith("---\n"):
        raise PublicationError(f"front matter ausente: {relative_path}")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise PublicationError(f"front matter não terminado: {relative_path}")
    try:
        metadata = yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError as exc:
        raise PublicationError(f"front matter inválido: {relative_path}: {exc}") from exc
    if not isinstance(metadata, dict):
        raise PublicationError(f"front matter deve ser objeto: {relative_path}")
    offset = end + 5
    return metadata, text[offset:], offset


def load_manifest(path: Path, root: Path) -> dict[str, Any]:
    path = path.resolve()
    root = root.resolve()
    if not is_inside(path, root):
        raise PublicationError("manifesto deve permanecer dentro do projeto")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise PublicationError(f"manifesto inválido: {exc}") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise PublicationError("manifesto deve usar schema_version: 1")
    if any(key in data for key in ("audiencia", "audiencias", "perfil", "publico")):
        raise PublicationError("manifesto não pode definir edição pública ou perfis de audiência")
    return data


def validate_book(data: dict[str, Any]) -> Book:
    book = data.get("livro")
    if not isinstance(book, dict):
        raise PublicationError("manifesto não define livro")
    required = {"titulo", "versao", "idioma", "arquivo_base"}
    missing = required - set(book)
    if missing:
        raise PublicationError(f"metadados do livro ausentes: {sorted(missing)}")
    basename = str(book["arquivo_base"])
    version = str(book["versao"])
    if not SAFE_NAME.fullmatch(basename) or "/" in basename or ".." in basename:
        raise PublicationError(f"arquivo_base inseguro: {basename!r}")
    if not SAFE_NAME.fullmatch(version.lower()) or "/" in version or ".." in version:
        raise PublicationError(f"versão insegura: {version!r}")
    return Book(
        title=str(book["titulo"]),
        subtitle=str(book.get("subtitulo", "")),
        version=version,
        language=str(book["idioma"]),
        basename=basename,
        status=str(book.get("status", "desenvolvimento")),
    )


def validate_source_path(relative_path: str, root: Path) -> Path:
    relative = Path(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise PublicationError(f"origem insegura: {relative_path}")
    normalized = relative.as_posix()
    if normalized.startswith(FORBIDDEN_SOURCE_PREFIXES):
        raise PublicationError(f"fonte em área proibida: {relative_path}")
    if not normalized.startswith(ALLOWED_SOURCE_PREFIXES):
        raise PublicationError(f"fonte fora das raízes editoriais: {relative_path}")
    source = safe_project_path(root, normalized, label="origem")
    if not source.is_file():
        raise PublicationError(f"fonte declarada ausente: {normalized}")
    if source.is_symlink():
        raise PublicationError(f"fonte não pode ser link simbólico: {normalized}")
    return source


def document_from_entry(
    entry: dict[str, Any],
    *,
    root: Path,
    section_id: str,
    section_title: str,
    section_role: str,
    order: int,
) -> Document:
    if not isinstance(entry, dict) or not entry.get("origem"):
        raise PublicationError(f"documento inválido na seção {section_id}")
    relative_path = Path(str(entry["origem"])).as_posix()
    source = validate_source_path(relative_path, root)
    raw = source.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublicationError(f"fonte não está em UTF-8: {relative_path}") from exc
    metadata, body, body_offset = split_front_matter(text, relative_path)
    if metadata.get("status") != "canon":
        raise PublicationError(f"fonte não canônica: {relative_path}")
    if metadata.get("publicar") is False:
        raise PublicationError(f"fonte declara publicar:false: {relative_path}")
    for key in ("id", "titulo"):
        if not metadata.get(key):
            raise PublicationError(f"fonte sem {key}: {relative_path}")
    document_id = str(metadata["id"])
    if not SAFE_ID.fullmatch(document_id):
        raise PublicationError(f"id editorial inseguro: {relative_path}: {document_id!r}")
    if section_role == "handouts":
        if not relative_path.startswith("apendices/handouts/"):
            raise PublicationError(f"handout fora de apendices/handouts/: {relative_path}")
        if metadata.get("tipo") != "handout":
            raise PublicationError(f"item da seção de handouts sem tipo:handout: {relative_path}")
        missing = [key for key in ("orientacao_mestre", "entregar_quando", "revela") if not metadata.get(key)]
        if missing:
            raise PublicationError(f"handout sem metadados {missing}: {relative_path}")
    elif metadata.get("tipo") == "handout":
        raise PublicationError(f"handout declarado fora da seção apropriada: {relative_path}")
    return Document(
        source=source,
        relative_path=relative_path,
        section_id=section_id,
        section_title=section_title,
        section_role=section_role,
        metadata=metadata,
        body=body,
        body_offset=body_offset,
        sha256=hashlib.sha256(raw).hexdigest(),
        anchor=f"doc-{document_id}",
        order=order,
    )


def local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    target = unquote(target)
    if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    return target.split("#", 1)[0]


def forbidden_relative(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError:
        return True
    return relative.startswith(FORBIDDEN_SOURCE_PREFIXES)


def inspect_links(
    documents: list[Document], root: Path
) -> tuple[list[LinkIssue], dict[str, Path]]:
    issues: list[LinkIssue] = []
    resources: dict[str, Path] = {}
    declared = {document.source.resolve(): document for document in documents}
    for document in documents:
        for match in LINK_RE.finditer(document.body):
            is_image = bool(match.group(1))
            target_value = local_link_target(match.group(3))
            if target_value is None:
                continue
            target = (document.source.parent / target_value).resolve()
            if not is_inside(target, root) or forbidden_relative(target, root):
                raise PublicationError(
                    f"referência local proibida em {document.relative_path}: {target_value}"
                )
            if not target.exists():
                issues.append(
                    LinkIssue(
                        source=document.relative_path,
                        target=target_value,
                        kind="recurso-ausente" if is_image else "link-ausente",
                        message="alvo local ainda indisponível",
                    )
                )
                continue
            if target.is_symlink() and not is_inside(target.resolve(), root):
                raise PublicationError(
                    f"referência local aponta para link externo em {document.relative_path}: {target_value}"
                )
            if is_image:
                if target.suffix.lower() not in IMAGE_SUFFIXES or not target.is_file():
                    raise PublicationError(
                        f"imagem local inválida em {document.relative_path}: {target_value}"
                    )
                key = hashlib.sha256(target.read_bytes()).hexdigest()[:16] + "-" + target.name
                resources[key] = target
            elif target.suffix.lower() == ".md" and target not in declared:
                issues.append(
                    LinkIssue(
                        source=document.relative_path,
                        target=target_value,
                        kind="link-nao-publicado",
                        message="alvo existe, mas não está declarado no manifesto",
                    )
                )
    return issues, resources


def prepare_publication(manifest_path: Path, root: Path, *, strict: bool = False) -> PublicationPlan:
    root = root.resolve()
    manifest_path = manifest_path.resolve()
    manifest = load_manifest(manifest_path, root)
    book = validate_book(manifest)
    section_entries = manifest.get("secoes")
    if not isinstance(section_entries, list) or not section_entries:
        raise PublicationError("manifesto não contém seções")

    sections: list[Section] = []
    documents: list[Document] = []
    section_ids: set[str] = set()
    origins: set[str] = set()
    document_ids: set[str] = set()
    order = 0
    for section_entry in section_entries:
        if not isinstance(section_entry, dict):
            raise PublicationError("seção inválida")
        section_id = str(section_entry.get("id", ""))
        title = str(section_entry.get("titulo", ""))
        role = str(section_entry.get("papel", "conteudo"))
        if not SAFE_ID.fullmatch(section_id) or section_id in section_ids:
            raise PublicationError(f"id de seção inválido ou duplicado: {section_id!r}")
        if not title or role not in {"abertura", "conteudo", "handouts"}:
            raise PublicationError(f"seção incompleta: {section_id}")
        if role == "abertura" and any(item.role == "abertura" for item in sections):
            raise PublicationError("manifesto não pode conter mais de uma seção de abertura")
        entries = section_entry.get("documentos")
        if not isinstance(entries, list):
            raise PublicationError(f"documentos deve ser lista: {section_id}")
        section = Section(id=section_id, title=title, role=role)
        section_ids.add(section_id)
        for entry in entries:
            origin = str(entry.get("origem", "")) if isinstance(entry, dict) else ""
            normalized = Path(origin).as_posix()
            if normalized in origins:
                raise PublicationError(f"origem duplicada no manifesto: {normalized}")
            document = document_from_entry(
                entry,
                root=root,
                section_id=section_id,
                section_title=title,
                section_role=role,
                order=order,
            )
            document_id = str(document.metadata["id"])
            if document_id in document_ids:
                raise PublicationError(f"id editorial duplicado: {document_id}")
            origins.add(normalized)
            document_ids.add(document_id)
            documents.append(document)
            section.documents.append(document)
            order += 1
        sections.append(section)
    if not documents:
        raise PublicationError("manifesto não seleciona documentos")

    issues, resources = inspect_links(documents, root)
    if strict and issues:
        formatted = "; ".join(f"{item.source} -> {item.target}" for item in issues)
        raise PublicationError(f"pendências locais em modo estrito: {formatted}")

    digest_payload = {
        "book": {
            "title": book.title,
            "subtitle": book.subtitle,
            "version": book.version,
            "language": book.language,
            "basename": book.basename,
            "status": book.status,
        },
        "documents": [
            {
                "path": document.relative_path,
                "sha256": document.sha256,
                "section": document.section_id,
                "order": document.order,
            }
            for document in documents
        ],
    }
    input_digest = hashlib.sha256(
        json.dumps(digest_payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return PublicationPlan(
        root=root,
        manifest_path=manifest_path,
        book=book,
        sections=sections,
        documents=documents,
        issues=issues,
        resources=resources,
        input_digest=input_digest,
        strict=strict,
    )


def rewrite_links(body: str, document: Document, plan: PublicationPlan, resource_names: dict[Path, str]) -> str:
    declared = {item.source.resolve(): item for item in plan.documents}

    def replace(match: re.Match[str]) -> str:
        prefix, label, raw = match.groups()
        target_value = local_link_target(raw)
        if target_value is None:
            return match.group(0)
        target = (document.source.parent / target_value).resolve()
        if target in declared:
            return f"{prefix}[{label}](#{declared[target].anchor})"
        if prefix and target in resource_names:
            return f"![{label}](assets/{resource_names[target]})"
        if not target.exists() or (target.suffix.lower() == ".md" and target not in declared):
            return f"[{label}](#pendencia-editorial)"
        return match.group(0)

    return LINK_RE.sub(replace, body)


def materialize(plan: PublicationPlan) -> Materialization:
    content_root = plan.root / "publicacao" / "conteudo"
    if content_root.exists():
        if content_root.resolve() != (plan.root / "publicacao" / "conteudo").resolve():
            raise PublicationError("caminho de materialização inseguro")
        shutil.rmtree(content_root)
    content_root.mkdir(parents=True)

    resource_names: dict[Path, str] = {}
    resource_records: list[dict[str, str]] = []
    assets_root = content_root / "assets"
    for name, source in sorted(plan.resources.items()):
        assets_root.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, assets_root / name)
        resource_names[source.resolve()] = name
        resource_records.append(
            {
                "source": source.relative_to(plan.root).as_posix(),
                "materialized": f"assets/{name}",
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            }
        )

    summary_lines = ["# Sumário da publicação", ""]
    combined_lines = [f"# {plan.book.title}", "", f"_Versão {plan.book.version}_", ""]
    document_records: list[dict[str, Any]] = []
    for section in plan.sections:
        summary_lines.append(f"- **{section.title}**")
        if not section.documents:
            summary_lines.append("  - _Em preparação_")
            continue
        combined_lines.extend([f"# {section.title}", ""])
        for document in section.documents:
            destination = content_root / document.relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(document.source, destination)
            summary_lines.append(
                f"  - [{document.metadata['titulo']}]({document.relative_path})"
            )
            body = rewrite_links(document.body, document, plan, resource_names)
            combined_lines.extend(
                [f'<a id="{document.anchor}"></a>', "", body.rstrip(), "", "\\newpage", ""]
            )
            document_records.append(
                {
                    "source": document.relative_path,
                    "id": document.metadata["id"],
                    "title": document.metadata["titulo"],
                    "section": document.section_id,
                    "role": document.section_role,
                    "order": document.order,
                    "sha256": document.sha256,
                }
            )
    summary_path = content_root / "SUMMARY.md"
    summary_path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    combined_path = content_root / "livro.md"
    combined_path.write_text("\n".join(combined_lines) + "\n", encoding="utf-8")
    metadata_path = content_root / "publication.json"
    metadata_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "book": {
                    "title": plan.book.title,
                    "subtitle": plan.book.subtitle,
                    "version": plan.book.version,
                    "language": plan.book.language,
                    "basename": plan.book.basename,
                    "status": plan.book.status,
                },
                "strict": plan.strict,
                "input_digest": plan.input_digest,
                "documents": document_records,
                "issues": [issue.__dict__ for issue in plan.issues],
                "resources": resource_records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return Materialization(
        plan=plan,
        content_root=content_root,
        summary_path=summary_path,
        combined_path=combined_path,
        metadata_path=metadata_path,
        resource_records=resource_records,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--check", action="store_true", help="valida sem escrever saídas")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        plan = prepare_publication(args.manifest, args.root, strict=args.strict)
        result = None if args.check else materialize(plan)
    except (OSError, PublicationError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    print(f"Livro: {plan.book.title} {plan.book.version}")
    print(f"Documentos: {len(plan.documents)}")
    print(f"Pendências locais: {len(plan.issues)}")
    print(f"Digest: {plan.input_digest}")
    if result:
        print(f"Materializado em: {result.content_root.relative_to(plan.root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
