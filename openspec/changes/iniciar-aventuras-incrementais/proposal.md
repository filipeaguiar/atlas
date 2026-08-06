## Why

A campanha já possui premissa, estrutura de três arcos e marcos fixos, mas ainda não possui um mapa operacional das 23 aventuras nem uma aventura publicável que sirva de padrão. Produzir incrementalmente, começando por um piloto, permite validar estrutura, agência, mecânicas e apresentação antes de expandir a saga sem transformar lacunas ou escolhas do Pacote de Antagonista em cânone.

## What Changes

- Criar um mapa editorial da saga completa em Mermaid, com 23 posições, arcos, Marcos, dependências e pontos condicionais claramente diferenciados.
- Registrar no mapa apenas funções já aprovadas; posições ainda indefinidas permanecem identificadas como lacunas editoriais, não como fatos canônicos.
- Definir um contrato reutilizável para aventuras do Mestre, centrado em situação, pressões, pistas redundantes, Objetivos, consequências e estados possíveis.
- Produzir **Aventura 1 — Exame de Admissão** como piloto publicável do fluxo incremental.
- Integrar a aventura aprovada ao manifesto e ao PDF do Mestre sem publicar planejamento, stubs ou materiais internos.
- Validar conteúdo, mecânicas de 3DeT Victory, links, proveniência e renderização antes de usar o modelo nas aventuras seguintes.

## Capabilities

### New Capabilities

- `mapa-editorial-da-saga`: representação Mermaid auditável dos três arcos e das 23 aventuras, preservando fatos fixos, decisões de Pacote, resultados condicionais e lacunas.
- `aventura-incremental-publicavel`: estrutura, validação e publicação individual de aventuras jogáveis para o Mestre, começando pelo Exame de Admissão.

### Modified Capabilities

Nenhuma.

## Impact

- Novos documentos em `campanha/arcos/` e `campanha/aventuras/`, sujeitos a front matter e aprovação individual.
- Atualização positiva e ordenada de `publicacao/manifest.yml` somente após validação da aventura piloto.
- Possíveis ajustes de CSS para diagramas Mermaid materializados e para páginas de aventura.
- Novos testes e verificações editoriais para estrutura de aventura, separação de camadas e integridade do PDF.
- Consulta seletiva ao backup e às referências locais, sem indexação integral, cópia automática ou publicação dessas fontes.
