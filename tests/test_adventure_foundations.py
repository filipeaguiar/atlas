from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from xml.etree import ElementTree

from tools.check_adventures import AdventureError, validate_adventure
from tools.check_saga_map import SagaMapError, validate_map

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "desenvolvimento" / "planejamento" / "mapa-da-saga.md"
ADVENTURE = ROOT / "campanha" / "aventuras" / "01-exame-de-admissao.md"
MANIFEST = ROOT / "publicacao" / "manifest.yml"


def test_mapa_real_tem_23_posicoes_e_fica_fora_do_manifesto() -> None:
    validate_map(MAP, MANIFEST)
    assert "desenvolvimento/planejamento/mapa-da-saga.md" not in MANIFEST.read_text()


def test_mapa_recusa_posicao_ausente_e_selecao_editorial(tmp_path: Path) -> None:
    text = MAP.read_text()
    invalid = tmp_path / "mapa.md"
    invalid.write_text(text.replace('    A23["Aventura 23', '    FINAL["Aventura 23', 1))
    manifest = tmp_path / "manifest.yml"
    manifest.write_text("schema_version: 1\n")
    with pytest.raises(SagaMapError, match="exatamente 1–23"):
        validate_map(invalid, manifest)

    invalid.write_text(text)
    manifest.write_text(f"origem: {invalid.as_posix()}\n")
    with pytest.raises(SagaMapError, match="não pode entrar"):
        validate_map(invalid, manifest)


def test_aventura_real_tem_estrutura_e_esta_publicada() -> None:
    validate_adventure(ADVENTURE, MANIFEST)
    metadata = yaml.safe_load(ADVENTURE.read_text().split("---\n", 2)[1])
    assert metadata["status"] == "canon"
    assert metadata["publicar"] is True
    assert metadata["aprovado"] is True
    assert "campanha/aventuras/01-exame-de-admissao.md" in MANIFEST.read_text()


def test_aventura_conta_e_aprova_todos_os_oito_estudantes_recorrentes() -> None:
    body = ADVENTURE.read_text()
    students = ("Lia", "Ravi", "Cecília", "Noah", "Malu", "Ícaro", "Sofia", "Dante")
    for student in students:
        assert student in body
    assert "8 + o número de personagens jogadores" in body
    assert "somente dez continuam ativos" in body
    assert "somente onze continuam ativos" in body
    assert "Todos os oito NPCs estudantes recorrentes também são aprovados" in body


def test_aventura_recusa_secao_ausente_e_aprovacao_sem_manifesto(tmp_path: Path) -> None:
    original = ADVENTURE.read_text()
    candidate = tmp_path / "aventura.md"
    manifest = tmp_path / "manifest.yml"
    manifest.write_text("schema_version: 1\n")

    candidate.write_text(original.replace("## A história até aqui", "## Contexto", 1))
    with pytest.raises(AdventureError, match="partes obrigatórias"):
        validate_adventure(candidate, manifest)

    candidate.write_text(original)
    with pytest.raises(AdventureError, match="deve constar no manifesto"):
        validate_adventure(candidate, manifest)


def test_aventura_recusa_rascunho_selecionado_e_resumo_sem_leitura(tmp_path: Path) -> None:
    original = ADVENTURE.read_text()
    candidate = tmp_path / "aventura.md"
    draft = (
        original.replace("status: canon", "status: revisao", 1)
        .replace("publicar: true", "publicar: false", 1)
        .replace("aprovado: true", "aprovado: false", 1)
    )
    candidate.write_text(draft)
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(f"origem: {candidate.as_posix()}\n")
    with pytest.raises(AdventureError, match="revisão"):
        validate_adventure(candidate, manifest)

    manifest.write_text("schema_version: 1\n")
    candidate.write_text(original.replace("> **Leia em voz alta:**", "> **Apresentação:**", 1))
    with pytest.raises(AdventureError, match="resumo deve conter"):
        validate_adventure(candidate, manifest)


def test_aventura_recusa_cena_sem_texto_para_mesa(tmp_path: Path) -> None:
    original = ADVENTURE.read_text()
    candidate = tmp_path / "aventura.md"
    before, scene_and_after = original.split("## Cena 1 — O Portão e a Largada", 1)
    scene, after = scene_and_after.split("## Cena 2 — O Circuito de Combate", 1)
    scene = scene.replace("> **Leia em voz alta:**", "> **Descrição:**")
    modified = before + "## Cena 1 — O Portão e a Largada" + scene + "## Cena 2 — O Circuito de Combate" + after
    candidate.write_text(modified)
    manifest = tmp_path / "manifest.yml"
    manifest.write_text(f"origem: {candidate.as_posix()}\n")
    with pytest.raises(AdventureError, match="cena sem leitura em voz alta"):
        validate_adventure(candidate, manifest)


def test_aventura_recusa_declaracao_negativa_no_material_final(tmp_path: Path) -> None:
    original = ADVENTURE.read_text()
    candidate = tmp_path / "aventura.md"
    candidate.write_text(original + "\nEsta aventura não concede Marco.\n")
    manifest = tmp_path / "manifest.yml"
    manifest.write_text("schema_version: 1\n")
    with pytest.raises(AdventureError, match="material final descreve ausência"):
        validate_adventure(candidate, manifest)


def test_mapas_legados_da_estacao_permanecem_svg_validos() -> None:
    for audience in ("jogadores", "mestre"):
        path = ROOT / "campanha" / "aventuras" / "recursos" / f"01-estacao-canal-quatro-{audience}.svg"
        root = ElementTree.parse(path).getroot()
        assert root.tag.endswith("svg")


def test_capitulos_de_arco_tem_proveniencia_de_recuperacao() -> None:
    for number in (1, 2, 3):
        path = ROOT / "campanha" / "arcos" / f"arco-{number}" / "README.md"
        metadata = yaml.safe_load(path.read_text().split("---\n", 2)[1])
        assert metadata["status"] == "canon"
        assert metadata["origem"] == "recuperacao-integral-aprovada"
        assert metadata["proveniencia"]["conteudo"] == "transcricao-literal"
