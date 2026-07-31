#!/usr/bin/env python3
"""Verifica a integridade da reconstrução e impede que marcadores virem publicação."""

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


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # All YAML files must parse.
    for path in list(ROOT.rglob('*.yml')) + list(ROOT.rglob('*.yaml')):
        try:
            yaml.safe_load(path.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'YAML inválido: {path.relative_to(ROOT)}: {exc}')

    # No pending placeholder may be active in the current manifest.
    manifest = yaml.safe_load((ROOT / 'publicacao/manifest.yml').read_text(encoding='utf-8'))
    active_sources = []
    for section in manifest.get('secoes', []):
        for doc in section.get('documentos', []):
            if doc.get('publicar', True):
                active_sources.append(doc['origem'])
    for rel in active_sources:
        path = ROOT / rel
        text = path.read_text(encoding='utf-8') if path.exists() else ''
        if 'status: recuperacao-pendente' in text or 'publicar: false' in text:
            errors.append(f'Fonte pendente ativada: {rel}')
        if rel.startswith(('desenvolvimento/', 'historico/', 'recuperacao/', 'publicacao/stubs/')):
            errors.append(f'Fonte interna ativada: {rel}')

    # DEC-001 checks.
    functions = yaml.safe_load((ROOT / 'desenvolvimento/planejamento/funcoes-aventuras.yml').read_text(encoding='utf-8'))['aventuras']
    if int(functions[14]['arco']) != 2 or functions[14].get('resultado_fisico') != 'condicional':
        errors.append('Aventura 14 não contém a segunda operação condicional')
    if 'consequências da segunda operação' not in functions[15]['funcao']:
        errors.append('Aventura 15 não contém as consequências da segunda operação')
    if 'licença definitiva' not in functions[16]['funcao']:
        errors.append('Aventura 16 não encerra o arco com licença definitiva')

    # No stale mapping may survive outside historical source snapshots.
    stale = re.compile(r'Aventura 15.{0,120}(segundo sequestro|segunda (?:operação de )?captura)', re.I | re.S)
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in {'.md', '.yml', '.yaml', '.py'}:
            continue
        if 'historico' in path.parts or 'fontes-legado-97' in path.parts or path.name == 'check_recovery.py':
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        if stale.search(text):
            errors.append(f'Mapeamento antigo encontrado: {path.relative_to(ROOT)}')

    inventory = json.loads((ROOT / 'recuperacao/inventario.json').read_text(encoding='utf-8'))
    warnings.append(f"Marcadores pendentes: {len(inventory['marcadores_pendentes'])}")

    if errors:
        for item in errors:
            print(f'ERRO: {item}', file=sys.stderr)
        return 1
    print('Recuperação operacional válida.')
    for item in warnings:
        print(f'AVISO: {item}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
