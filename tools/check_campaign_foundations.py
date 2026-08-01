#!/usr/bin/env python3
"""Valida os fundamentos publicáveis da campanha e suas fronteiras narrativas."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML é necessário: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "desenvolvimento" / "planejamento" / "matriz-factual-campanha.yml"
INVENTORY = ROOT / "recuperacao" / "inventario.json"
MANIFEST = ROOT / "publicacao" / "manifest.yml"
ALLOWED_SOURCES = {
    "publicacao/fontes/introducao/01-introducao.md",
    "cenario/01-visao-geral.md",
    "cenario/05-programa-de-campo.md",
    "cenario/07-central-de-operacoes.md",
    "cenario/09-vanguarda.md",
    "cenario/10-tragedia-memoria-publica.md",
    "cenario/11-instituto-atlas-hub-jogavel.md",
    "regras/README.md",
    "regras/05-operacoes-do-atlas.md",
}
REQUIRED_CLASSES = {
    "fixo",
    "progressao",
    "segredo-do-mestre",
    "resultado-condicional",
    "opcao-de-pacote",
    "exemplo-editorial",
}
MANDATORY_CAPTURE_PATTERNS = {
    "quatro capturados": re.compile(r"com quatro sobreviventes em poder", re.I),
    "captura obrigatória de Tomás": re.compile(r"(?:quando|depois que)\s+Tomás\s+(?:é|for)\s+capturado", re.I),
    "Tomás será capturado": re.compile(r"Tomás\s+(?:é|será)\s+capturado", re.I),
    "Vanguarda será capturada": re.compile(r"membros?\s+(?:da\s+)?Vanguarda\s+(?:é|são|será|serão)\s+captur", re.I),
}
ANTAGONISTS = (
    "Arquiteto|Mecenas|Zero|Rei do Véu|Mãe da Maré|Hierofante|Soberano|Titã|"
    "Ascendente|Emissário|Regente|Arauto do Horizonte"
)
SELECTED_PACKAGE = re.compile(rf"(?:o|a)\s+antagonista\s+(?:é|será)\s+(?:{ANTAGONISTS})", re.I)


def split_front_matter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("front matter ausente")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter não terminado")
    data = yaml.safe_load(text[4:end]) or {}
    if not isinstance(data, dict):
        raise ValueError("front matter não é objeto")
    return data, text[end + 5 :]


def active_sources(manifest: dict) -> set[str]:
    return {
        doc["origem"]
        for section in manifest.get("secoes", [])
        for doc in section.get("documentos", [])
        if doc.get("publicar", True)
    }


def main() -> int:
    errors: list[str] = []
    matrix = yaml.safe_load(MATRIX.read_text(encoding="utf-8")) or {}
    targets = set(matrix.get("capitulos_em_escopo", []))
    if len(targets) != 6:
        errors.append(f"Matriz deve conter seis capítulos; encontrou {len(targets)}")
    if matrix.get("metadata", {}).get("publicar") is not False:
        errors.append("Matriz factual deve permanecer não publicável")

    sources = {item.get("caminho") for item in matrix.get("fontes_permitidas", [])}
    if sources != ALLOWED_SOURCES:
        errors.append("Fontes permitidas divergem do contrato da mudança")
    governance_ids = {item.get("id") for item in matrix.get("restricoes_de_governanca", [])}
    source_ids = {item.get("id") for item in matrix.get("fontes_permitidas", [])} | governance_ids
    classes: set[str] = set()
    fact_ids: set[str] = set()
    for fact in matrix.get("fatos_autorizados", []):
        fact_id = fact.get("id")
        if fact_id in fact_ids:
            errors.append(f"ID factual duplicado: {fact_id}")
        fact_ids.add(fact_id)
        classes.add(fact.get("classe"))
        if fact.get("fonte") not in source_ids:
            errors.append(f"Fato usa fonte não autorizada: {fact_id} -> {fact.get('fonte')}")
        if not set(fact.get("capitulos", [])) <= targets:
            errors.append(f"Fato autoriza capítulo fora do escopo: {fact_id}")
    if classes != REQUIRED_CLASSES:
        errors.append(f"Classes factuais divergentes: {sorted(classes)}")

    forbidden_authorities = tuple(matrix.get("fontes_proibidas_como_autoridade_narrativa", []))
    for item in matrix.get("fontes_permitidas", []):
        if item.get("caminho", "").startswith(forbidden_authorities):
            errors.append(f"Fonte narrativa interna ou histórica: {item.get('caminho')}")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    indexed = {item["caminho_atual"]: item for item in inventory.get("documentos_editoriais", [])}
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    active = active_sources(manifest)
    forbidden_terms = manifest.get("termos_proibidos", [])

    bodies: dict[str, str] = {}
    for target in sorted(targets):
        path = ROOT / target
        if not path.is_file():
            errors.append(f"Capítulo ausente: {target}")
            continue
        try:
            fm, body = split_front_matter(path)
        except ValueError as exc:
            errors.append(f"{target}: {exc}")
            continue
        bodies[target] = body
        expected = {
            "status": "canon",
            "origem": "reescrita-aprovada",
            "publicar": True,
            "aprovado": True,
            "reescrita_de_marcador": True,
            "camada": "mestre",
            "conteudo_para_jogadores": False,
        }
        for key, value in expected.items():
            if fm.get(key) != value:
                errors.append(f"{target}: {key} deve ser {value!r}")
        factual_sources = set(fm.get("fontes_fatuais", []))
        if not factual_sources or not factual_sources <= ALLOWED_SOURCES:
            errors.append(f"{target}: fontes factuais ausentes ou não autorizadas")
        if "Material do Mestre" not in body:
            errors.append(f"{target}: aviso de camada do Mestre ausente")
        if len(body.split()) < 650:
            errors.append(f"{target}: conteúdo insuficiente para capítulo completo")
        if "Recuperação pendente" in body or "_A preencher" in body:
            errors.append(f"{target}: marcador ou placeholder remanescente")
        for term in forbidden_terms:
            if term in body:
                errors.append(f"{target}: termo editorial proibido: {term}")
        for label, pattern in MANDATORY_CAPTURE_PATTERNS.items():
            if pattern.search(body):
                errors.append(f"{target}: desfecho físico obrigatório ({label})")
        if SELECTED_PACKAGE.search(body):
            errors.append(f"{target}: Pacote selecionado indevidamente")
        record = indexed.get(target)
        if record is None or record.get("estado_recuperacao") != "reescrito-aprovado":
            errors.append(f"{target}: inventário não registra reescrita aprovada")
        else:
            history = record.get("historico_recuperacao", {})
            if history.get("conteudo_original_recuperado") is not False or not history.get("sha256_marcador_substituido"):
                errors.append(f"{target}: histórico do marcador incompleto")
        if target not in active:
            errors.append(f"{target}: capítulo aprovado ausente do manifesto")

    arc2 = bodies.get("campanha/arcos/arco-2/README.md", "")
    if not re.search(r"Aventura 14.{0,240}captura física (?:é|permanece) condicional", arc2, re.I | re.S):
        errors.append("Arco II não preserva explicitamente a captura física condicional na Aventura 14")
    if not re.search(r"Aventura 15.{0,180}consequ", arc2, re.I | re.S):
        errors.append("Arco II não atribui consequências à Aventura 15")
    if not re.search(r"Aventura 16.{0,180}licença definitiva", arc2, re.I | re.S):
        errors.append("Arco II não conclui com licença definitiva na Aventura 16")

    expected_counts = inventory.get("contagens_esperadas", {})
    required_counts = {
        "marcadores_recuperacao_pendente": 79,
        "stubs_aventura": 23,
        "fontes_legado_97": 97,
        "reescritos_aprovados": 15,
        "documentos_ativos_manifesto": 18,
    }
    for key, value in required_counts.items():
        if expected_counts.get(key) != value:
            errors.append(f"Contagem esperada divergente: {key}={expected_counts.get(key)!r}; deveria ser {value}")

    if errors:
        for error in errors:
            print(f"ERRO: {error}", file=sys.stderr)
        return 1

    print("Fundamentos da campanha válidos.")
    print(f"Capítulos do Mestre aprovados: {len(targets)}")
    print(f"Fatos autorizados: {len(fact_ids)}")
    print("Desfechos físicos obrigatórios encontrados: 0")
    print("Pacotes selecionados indevidamente: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
