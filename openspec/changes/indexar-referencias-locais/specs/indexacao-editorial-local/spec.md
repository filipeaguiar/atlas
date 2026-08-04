## ADDED Requirements

### Requirement: Índices editoriais e externos são isolados
O sistema MUST manter referências externas em banco, configuração e comandos distintos dos índices de fontes editoriais aprovadas.

#### Scenario: Geração do índice editorial
- **WHEN** `build_retrieval_index.py` processa cenário, campanha, regras ou apêndices
- **THEN** nenhum arquivo de `referencias/` é descoberto ou incluído

#### Scenario: Geração do índice de referências
- **WHEN** `index_references.py` processa o catálogo externo
- **THEN** nenhum documento canônico é incluído sem também ser uma referência explicitamente catalogada
