## Why

O projeto agora possui baseline e backup remoto, mas ainda apresenta duas arquiteturas de manifesto, numeração divergente nas regras, referências quebradas e um inventário de recuperação que não confirma a existência física dos 94 marcadores. Antes de recuperar ou reescrever conteúdo, é necessário estabelecer uma arquitetura editorial única e verificável para que cada novo capítulo tenha destino, autoridade e caminho de publicação inequívocos.

## What Changes

- Definir uma árvore editorial definitiva para fontes canônicas, adaptações públicas, aventuras, assets, desenvolvimento, recuperação, histórico e saídas geradas.
- Estabelecer `publicacao/manifest.yml` como único manifesto operacional e retirar a ambiguidade de `publicacao/manifesto.yml`, preservando seu valor histórico fora do fluxo ativo.
- **BREAKING**: normalizar a nomenclatura e a numeração planejada dos capítulos de regras, com mapa explícito de migração e atualização coordenada das referências; caminhos antigos deixam de ser referências editoriais ativas.
- Corrigir os cinco links quebrados de `regras/README.md` sem tratar marcadores pendentes como conteúdo recuperado.
- Definir o sumário-alvo do módulo e separar claramente índice de fontes, índice da publicação e capítulos ainda não disponíveis.
- Criar um inventário operacional que confronte caminhos esperados com arquivos físicos, status, publicabilidade, origem e destino editorial.
- Definir o ciclo de vida de cada marcador: preservar, recuperar, reescrever com aprovação, substituir por migração registrada ou retirar do escopo.
- Ampliar as validações para detectar marcador ausente, status incompatível, fonte interna ativada, destino duplicado, link local quebrado e divergência entre manifesto, sumário e inventário.
- Atualizar documentação e ferramentas para usar a arquitetura consolidada.
- Não recuperar conteúdo ausente, escrever aventuras ou gerar o PDF final nesta mudança.

## Capabilities

### New Capabilities

- `arquitetura-editorial-do-modulo`: Define camadas, fontes de verdade, caminhos canônicos, manifesto operacional único, sumários e migrações editoriais necessárias ao módulo final.
- `integridade-da-recuperacao-editorial`: Mantém inventário físico verificável, ciclo de vida dos marcadores e validações cruzadas de caminhos, status, links e publicabilidade.

### Modified Capabilities

Nenhuma.

## Impact

- `AGENTS.md`, `README.md`, `SUMMARY.md`, `ORGANIZACAO.md` e documentação de publicação e recuperação.
- `publicacao/manifest.yml`, `publicacao/manifesto.yml` e registros históricos relacionados.
- Caminhos e links da seção `regras/`, com migração auditável dos marcadores afetados.
- `recuperacao/inventario.json`, relatórios de árvore e verificadores de integridade.
- `tools/check_recovery.py` e `tools/materialize_publication.py`; poderá ser criado um verificador específico de links e arquitetura.
- Nenhum fato narrativo novo será canonizado, nenhum marcador será preenchido silenciosamente e nenhuma fonte interna entrará no produto.
