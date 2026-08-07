from __future__ import annotations

import re
from pathlib import Path

import yaml

from tools.materialize_publication import split_front_matter

ROOT = Path(__file__).resolve().parents[1]
TENANT_FILES = [ROOT / "regras" / f"0{number}-fichas-tenentes-{kind}.md" for number, kind in [
    (7, "tecnologicos"), (8, "misticos"), (9, "super-humanos")
]] + [ROOT / "regras" / "10-fichas-tenentes-cosmicos.md"]
BOSS_FILES = sorted((ROOT / "regras" / "antagonistas-principais").glob("*.md"))
NPC_FILES = [
    ROOT / "regras" / "11-fichas-equipe-atlas.md",
    ROOT / "regras" / "12-fichas-alunos-recorrentes.md",
    ROOT / "regras" / "13-fichas-vanguarda.md",
]

EXPECTED_TENANTS = {
    "Nexo", "Bastião", "Contramedida", "Rastro", "Véspera", "Custódio", "Sutura", "Presságio",
    "Estandarte", "Ruptura", "Síncope", "Rasante", "Meridiano", "Eclipse", "Paralaxe", "Peregrino",
}
EXPECTED_BOSSES = {"Arquiteto", "Ascendente", "Hierofante", "Mãe da Maré", "Mecenas", "Regente", "Rei do Véu", "Titã", "Zero"}
EXPECTED_STAFF = {"Beatriz Leal", "Álvaro Siqueira", "Dalva Menezes", "Dra. Samira Nasser", "Lívia Monteiro", "Caio Ventura", "Janaína Rocha", "Raul Farias", "Tomás Valença"}
EXPECTED_STUDENTS = {"Lia Vasconcelos", "Ravi Moura", "Cecília Dantas", "Noah Sato", "Malu Serrano", "Ícaro Tavares", "Sofia Mendonça", "Dante Arcos"}
EXPECTED_VANGUARD = {"Solar", "Multiplex", "Prisma", "Colosso", "Oráculo", "Vetora"}


def headings(paths: list[Path], level: int = 2) -> set[str]:
    found: set[str] = set()
    marker = "#" * level + " "
    for path in paths:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(marker):
                found.add(line[len(marker):].split(" — ", 1)[0].removeprefix("O ").removeprefix("A "))
    return found


def test_cobertura_de_inimigos_e_npcs() -> None:
    assert EXPECTED_TENANTS <= headings(TENANT_FILES)
    assert EXPECTED_BOSSES <= headings(BOSS_FILES, level=1)
    assert EXPECTED_STAFF <= headings([NPC_FILES[0]])
    assert EXPECTED_STUDENTS <= headings([NPC_FILES[1]])
    assert EXPECTED_VANGUARD <= headings([NPC_FILES[2]])


def test_fichas_possuem_front_matter_publicavel_e_estatisticas() -> None:
    for path in TENANT_FILES + BOSS_FILES + NPC_FILES:
        metadata, body, _ = split_front_matter(path.read_text(encoding="utf-8"), str(path))
        assert metadata["status"] == "canon"
        assert metadata["publicar"] is True
        assert metadata["aprovado"] is True
        assert metadata["tipo"] == "ficha"
        assert metadata["categoria"]
        assert re.search(r"P\d+, H\d+, R\d+; \d+ ?PV", body), path
        assert "recuperacao-pendente" not in body
        for line in body.splitlines():
            if re.match(r"(?:- )?\*\*(Perícias|Vantagens|Desvantagens|Limitaç(?:ão|ões)):", line):
                assert line.startswith("- "), f"item mecânico fora de lista: {path}: {line}"


def test_tecnicas_exclusivas_dos_tenentes_sao_listas_separadas() -> None:
    for path in TENANT_FILES:
        _, body, _ = split_front_matter(path.read_text(encoding="utf-8"), str(path))
        assert body.count("### Técnicas exclusivas") == 4, path
        assert len(re.findall(r"^- \*\*Desvantagens:\*\*.*\n\n### Técnicas exclusivas$", body, re.MULTILINE)) == 4, path
        sections = body.split("### Técnicas exclusivas")[1:]
        for section in sections:
            techniques = section.split("**TESOURO**", 1)[0]
            assert len(re.findall(r"^- \*\*[^*]+:\*\*", techniques, re.MULTILINE)) == 2, path


def test_tecnicas_especiais_da_vanguarda_sao_listas_separadas() -> None:
    _, body, _ = split_front_matter(NPC_FILES[2].read_text(encoding="utf-8"), str(NPC_FILES[2]))
    assert body.count("### Técnicas especiais") == 5
    assert len(re.findall(r"^\*\*P\d+, H\d+, R\d+; \d+ PV, \d+ PM, \d+ PA\.\*\*$", body, re.MULTILINE)) == 5
    assert len(re.findall(r"^- \*\*Limitação:\*\*.*\n\n### Técnicas especiais$", body, re.MULTILINE)) == 5
    for section in body.split("### Técnicas especiais")[1:]:
        techniques = re.split(r"^## ", section, maxsplit=1, flags=re.MULTILINE)[0]
        assert len(re.findall(r"^- \*\*[^*]+:\*\*", techniques, re.MULTILINE)) == 3


def test_npcs_sao_redacao_atual_e_nao_copiam_stubs() -> None:
    for path in NPC_FILES:
        metadata, body, _ = split_front_matter(path.read_text(encoding="utf-8"), str(path))
        assert metadata["origem"] == "redacao-atual-aprovada"
        assert "Recuperação pendente" not in body


def test_manifesto_nao_publica_curadoria_de_imagens() -> None:
    manifest = yaml.safe_load((ROOT / "publicacao" / "manifest.yml").read_text())
    origins = [item["origem"] for section in manifest["secoes"] for item in section["documentos"]]
    assert all(not origin.startswith("desenvolvimento/") for origin in origins)
    assert all(not origin.lower().endswith((".png", ".jpg", ".webp")) for origin in origins)
