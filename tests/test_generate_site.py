from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.generate_site import (
    DEFAULT_DESTINATION,
    DEFAULT_STAGE,
    audit_site,
    generate_site,
    materialize_hugo,
    render_stat_panels,
    rewrite_site_links,
    wrap_sheet_cards,
)
from tools.materialize_publication import DEFAULT_MANIFEST, PROJECT_ROOT, PublicationError, prepare_publication


def test_materializacao_hugo_contem_somente_documentos_manifestados() -> None:
    plan = prepare_publication(DEFAULT_MANIFEST, PROJECT_ROOT, strict=True)
    stage = materialize_hugo(plan)
    generated_ids = {
        path.stem
        for path in (stage / "content").glob("*/*.md")
        if path.name != "_index.md"
    }
    manifest_ids = {str(document.metadata["id"]) for document in plan.documents}
    assert generated_ids == manifest_ids
    assert len(generated_ids) == 33
    assert not (stage / "content" / "desenvolvimento").exists()
    assert not list(stage.rglob("*.pdf"))
    sheet = (stage / "content" / "regras" / "fichas-equipe-atlas.md").read_text()
    assert "tipo: ficha" in sheet
    assert "categoria: npcs-atlas" in sheet


def test_links_entre_capitulos_sao_relativos_ao_site() -> None:
    plan = prepare_publication(DEFAULT_MANIFEST, PROJECT_ROOT, strict=True)
    source = next(document for document in plan.documents if document.metadata["id"] == "campanha-tres-arcos")
    rewritten = rewrite_site_links(source.body, source, plan, {})
    assert "../../campanha/campanha-arco-1/" in rewritten
    assert "README.md" not in rewritten


def test_build_hugo_funciona_em_subdiretorio_e_nao_publica_pdf() -> None:
    destination, plan = generate_site(base_url="https://exemplo.github.io/projeto/")
    assert len(plan.documents) == 33
    home = (destination / "index.html").read_text(encoding="utf-8")
    chapter = (
        destination / "campanha" / "campanha-tres-arcos" / "index.html"
    ).read_text(encoding="utf-8")
    assert 'href=/projeto/' in home
    assert "/projeto/campanha/campanha-arco-1/" in chapter
    assert "Material do Mestre" in home
    assert "material em desenvolvimento" in home
    assert "Conteúdo em preparação" in (
        destination / "handouts" / "index.html"
    ).read_text(encoding="utf-8")
    assert '<details class=mobile-menu>' in home
    assert '<details class="mobile-menu" open' not in home
    sheet = (destination / "regras" / "fichas-equipe-atlas" / "index.html").read_text()
    assert "stat-panel" in sheet
    assert "tcg-card" in sheet
    assert "tcg-card-frame" in sheet
    assert not list(destination.rglob("*.pdf"))
    report = json.loads((PROJECT_ROOT / "build" / "relatorio-site.json").read_text())
    assert report["pdfs_published"] == 0


def test_render_stat_panels_separa_atributos_e_recursos() -> None:
    rendered = render_stat_panels("**P3, H6, R4; 20 PV, 30 PM, 3 PA.**")
    assert 'class="stat-panel"' in rendered
    for label, value in (("P", "3"), ("H", "6"), ("R", "4"), ("PV", "20"), ("PM", "30"), ("PA", "3")):
        assert f"<b>{label}</b><strong>{value}</strong>" in rendered


def test_wrap_sheet_cards_cria_um_card_por_ficha() -> None:
    body = "# Compêndio\n\n## Um\n\nTexto.\n\n## Dois\n\nOutro.\n"
    wrapped = wrap_sheet_cards(body, "Compêndio")
    assert wrapped.count("{{< sheet-card") == 2
    assert 'title="Um"' in wrapped and 'title="Dois"' in wrapped


def test_auditoria_recusa_pdf_e_marcador_interno(tmp_path: Path) -> None:
    (tmp_path / "arquivo.pdf").write_bytes(b"pdf")
    with pytest.raises(PublicationError, match="PDF proibido"):
        audit_site(tmp_path)
    (tmp_path / "arquivo.pdf").unlink()
    (tmp_path / "index.html").write_text("openspec/changes/segredo")
    with pytest.raises(PublicationError, match="área interna"):
        audit_site(tmp_path)


def test_css_declara_limites_responsivos() -> None:
    css_root = PROJECT_ROOT / "publicacao" / "hugo" / "assets" / "css"
    css = "\n".join(path.read_text() for path in sorted(css_root.glob("*.css")))
    assert "@media (max-width: 48rem)" in css
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert ".mobile-menu { display: none; }" in css
    assert ".mobile-menu[open]::before" in css
    assert "position: fixed; inset: 0 auto 0 0" in css
    assert ".stat-panel" in css
    assert ".tcg-card" in css
    assert "Space Grotesk Atlas" in css and "Fraunces Atlas" in css
    assert "max-width: 100%" in css
    assert "overflow-x: auto" in css
    assert ":focus-visible" in css
    assert "http://" not in css and "https://" not in css
    for relative in (
        "fraunces/Fraunces-Variable.ttf",
        "fraunces/OFL.txt",
        "space-grotesk/SpaceGrotesk-Variable.ttf",
        "space-grotesk/OFL.txt",
    ):
        assert (PROJECT_ROOT / "publicacao" / "hugo" / "static" / "fonts" / relative).is_file()
