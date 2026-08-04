from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml

from tools.generate_pdf import find_chrome, generate, render_html
from tools.materialize_publication import (
    PublicationError,
    materialize,
    prepare_publication,
)


def write_source(
    root: Path,
    relative: str,
    *,
    document_id: str,
    title: str,
    status: str = "canon",
    publicar: bool = True,
    tipo: str = "cenario",
    body: str | None = None,
    **metadata,
) -> Path:
    data = {
        "id": document_id,
        "titulo": title,
        "tipo": tipo,
        "status": status,
        "publicar": publicar,
        **metadata,
    }
    content = body or (f"# {title}\n\n" + "Conteúdo editorial aprovado para o livro. " * 20)
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + "---\n" + content,
        encoding="utf-8",
    )
    return path


def write_manifest(root: Path, documents: list[dict], *, version: str = "0.1.0-dev.1") -> Path:
    data = {
        "schema_version": 1,
        "livro": {
            "titulo": "Livro de Teste",
            "subtitulo": "Somente para o Mestre",
            "versao": version,
            "idioma": "pt-BR",
            "arquivo_base": "livro-de-teste",
            "status": "desenvolvimento",
        },
        "secoes": [
            {"id": "conteudo", "titulo": "Conteúdo", "papel": "conteudo", "documentos": documents},
            {"id": "handouts", "titulo": "Handouts", "papel": "handouts", "documentos": []},
        ],
    }
    path = root / "publicacao" / "manifest.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def write_layout(root: Path) -> tuple[Path, Path]:
    template = root / "publicacao" / "templates" / "livro.html"
    css = root / "publicacao" / "estilos" / "livro.css"
    template.parent.mkdir(parents=True, exist_ok=True)
    css.parent.mkdir(parents=True, exist_ok=True)
    template.write_text(
        "<html><head><title>{{TITLE}}</title><style>{{CSS}}</style></head>"
        "<body>{{COVER}}{{TOC}}{{CONTENT}}</body></html>",
        encoding="utf-8",
    )
    css.write_text("@page { size: A4; } .chapter { page-break-before: always; }", encoding="utf-8")
    return template, css


def write_fake_chrome(root: Path) -> Path:
    script = root / "fake-chrome"
    script.write_text(
        "#!/usr/bin/env python3\n"
        "import pathlib,sys\n"
        "if '--version' in sys.argv:\n"
        " print('Fake Chrome 1.0'); raise SystemExit(0)\n"
        "arg=next(x for x in sys.argv if x.startswith('--print-to-pdf='))\n"
        "path=pathlib.Path(arg.split('=',1)[1])\n"
        "path.parent.mkdir(parents=True,exist_ok=True)\n"
        "path.write_bytes(b'%PDF-1.4\\n'+b'x'*2048)\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


def test_manifesto_preserva_lista_positiva_e_ordem(tmp_path: Path) -> None:
    write_source(tmp_path, "cenario/um.md", document_id="um", title="Um")
    write_source(tmp_path, "cenario/dois.md", document_id="dois", title="Dois")
    write_source(tmp_path, "cenario/nao-declarado.md", document_id="tres", title="Três")
    manifest = write_manifest(
        tmp_path,
        [{"origem": "cenario/dois.md"}, {"origem": "cenario/um.md"}],
    )

    first = prepare_publication(manifest, tmp_path)
    second = prepare_publication(manifest, tmp_path)
    result = materialize(first)

    assert [doc.relative_path for doc in first.documents] == ["cenario/dois.md", "cenario/um.md"]
    assert first.input_digest == second.input_digest
    metadata = json.loads(result.metadata_path.read_text())
    assert [doc["source"] for doc in metadata["documents"]] == ["cenario/dois.md", "cenario/um.md"]
    assert not (result.content_root / "cenario" / "nao-declarado.md").exists()


def test_recusa_duplicatas_fontes_inseguras_e_metadados_invalidos(tmp_path: Path) -> None:
    write_source(tmp_path, "cenario/um.md", document_id="um", title="Um")
    duplicate = write_manifest(
        tmp_path,
        [{"origem": "cenario/um.md"}, {"origem": "cenario/um.md"}],
    )
    with pytest.raises(PublicationError, match="duplicada"):
        prepare_publication(duplicate, tmp_path)

    references = tmp_path / "referencias" / "livro.md"
    references.parent.mkdir(parents=True)
    references.write_text("texto protegido", encoding="utf-8")
    forbidden = write_manifest(tmp_path, [{"origem": "referencias/livro.md"}])
    with pytest.raises(PublicationError, match="proibida"):
        prepare_publication(forbidden, tmp_path)

    unsafe = write_manifest(tmp_path, [{"origem": "../fora.md"}])
    with pytest.raises(PublicationError, match="insegura"):
        prepare_publication(unsafe, tmp_path)

    write_source(
        tmp_path,
        "cenario/rascunho.md",
        document_id="rascunho",
        title="Rascunho",
        status="rascunho",
    )
    draft = write_manifest(tmp_path, [{"origem": "cenario/rascunho.md"}])
    with pytest.raises(PublicationError, match="não canônica"):
        prepare_publication(draft, tmp_path)


def test_links_sao_aviso_incremental_e_erro_estrito(tmp_path: Path) -> None:
    write_source(
        tmp_path,
        "campanha/arcos.md",
        document_id="arcos",
        title="Arcos",
        tipo="campanha",
        body="# Arcos\n\nConsulte [Arco futuro](arcos/arco-1.md).",
    )
    manifest = write_manifest(tmp_path, [{"origem": "campanha/arcos.md"}])

    incremental = prepare_publication(manifest, tmp_path, strict=False)
    assert [(issue.kind, issue.target) for issue in incremental.issues] == [
        ("link-ausente", "arcos/arco-1.md")
    ]
    with pytest.raises(PublicationError, match="modo estrito"):
        prepare_publication(manifest, tmp_path, strict=True)


def test_handout_fica_no_mesmo_html_com_orientacao_separada(tmp_path: Path) -> None:
    write_source(
        tmp_path,
        "apendices/handouts/convite.md",
        document_id="handout-convite",
        title="Convite do Atlas",
        tipo="handout",
        orientacao_mestre="Entregue somente após o contato oficial.",
        entregar_quando="Depois da cena de abertura.",
        revela=["local do exame", "horário"],
        body="# Convite do Atlas\n\nVocê foi convocado para o exame.",
    )
    manifest = write_manifest(tmp_path, [])
    data = yaml.safe_load(manifest.read_text())
    data["secoes"][1]["documentos"] = [{"origem": "apendices/handouts/convite.md"}]
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
    template, css = write_layout(tmp_path)

    plan = prepare_publication(manifest, tmp_path)
    output = render_html(materialize(plan), template, css)
    rendered = output.read_text()

    assert "Orientação do Mestre — Convite do Atlas" in rendered
    assert "Depois da cena de abertura" in rendered
    assert "handout-page" in rendered
    assert rendered.index("master-note") < rendered.index("handout-page")
    assert list((tmp_path / "build").glob("*public*")) == []


def test_build_com_chrome_simulado_gera_pdf_e_relatorio(tmp_path: Path) -> None:
    write_source(tmp_path, "cenario/capitulo.md", document_id="capitulo", title="Capítulo")
    manifest = write_manifest(tmp_path, [{"origem": "cenario/capitulo.md"}])
    template, css = write_layout(tmp_path)
    chrome = write_fake_chrome(tmp_path)
    stale = tmp_path / "publicacao" / "conteudo" / "obsoleto.md"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("antigo")

    pdf, report_path, plan = generate(
        manifest,
        tmp_path,
        template_path=template,
        css_path=css,
        chrome_path=str(chrome),
    )

    assert pdf.name == "livro-de-teste-0.1.0-dev.1.pdf"
    assert pdf.stat().st_size > 1000
    assert not stale.exists()
    report = json.loads(report_path.read_text())
    assert report["mode"] == "incremental"
    assert report["input_digest"] == plan.input_digest
    assert report["chrome"]["version"] == "Fake Chrome 1.0"
    assert len(report["documents"]) == 1
    assert all("publico" not in item["path"] for item in report["artifacts"])
    assert len(list((tmp_path / "build").glob("*.pdf"))) == 1


def test_handout_sem_orientacao_e_chrome_invalido_falham(tmp_path: Path) -> None:
    write_source(
        tmp_path,
        "apendices/handouts/incompleto.md",
        document_id="handout-incompleto",
        title="Incompleto",
        tipo="handout",
    )
    manifest = write_manifest(tmp_path, [])
    data = yaml.safe_load(manifest.read_text())
    data["secoes"][1]["documentos"] = [{"origem": "apendices/handouts/incompleto.md"}]
    manifest.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
    with pytest.raises(PublicationError, match="handout sem metadados"):
        prepare_publication(manifest, tmp_path)
    with pytest.raises(PublicationError, match="CHROME_BIN"):
        find_chrome(str(tmp_path / "chrome-ausente"))
