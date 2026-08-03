## Why

O novo projeto será reconstruído gradualmente a partir de `Atlas.bkp`, sem importar a árvore antiga de uma só vez. Um índice local e descartável ajudará a localizar contexto nos documentos já aprovados, desde que nunca transforme a cópia de segurança, marcadores ou material interno em fonte canônica.

## What Changes

- Adicionar Chonkie 1.7 como dependência Python bloqueada por `uv`.
- Criar um indexador local de Markdown com fragmentação recursiva e metadados de proveniência.
- Oferecer índices separados para audiência pública e do Mestre.
- Recusar documentos sem front matter aprovado, fontes fora das raízes permitidas e caminhos internos ou derivados.
- Gerar apenas JSON descartável sob `build/retrieval/`, sem embeddings ou banco vetorial.
- Registrar que `Atlas.bkp` é consulta somente leitura e nunca é indexado diretamente.

## Capabilities

### New Capabilities
- `indexacao-editorial-local`: gera fragmentos determinísticos de fontes aprovadas sem alterar sua autoridade editorial.

### Modified Capabilities

## Impact

A mudança cria configuração Python, lockfile, ferramenta de indexação, testes e documentação de governança. Não recupera documentos, não adiciona conteúdo canônico, não usa serviços externos e não integra embeddings.
