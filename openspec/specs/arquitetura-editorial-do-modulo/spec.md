# arquitetura-editorial-do-modulo Specification

## Purpose
TBD - created by archiving change consolidar-arquitetura-editorial. Update Purpose after archive.
## Requirements
### Requirement: Hierarquia editorial inequívoca
O projeto MUST manter uma única fonte editável para cada conteúdo e MUST distinguir fontes canônicas, adaptações editoriais, planejamento interno, recuperação, histórico e saídas geradas.

#### Scenario: Conteúdo canônico integral
- **WHEN** um capítulo possui conteúdo integral aprovado em `cenario/`, `campanha/`, `regras/` ou `apendices/`
- **THEN** esse arquivo é sua fonte canônica e qualquer cópia em `publicacao/conteudo/` é derivada

#### Scenario: Planejamento interno
- **WHEN** um arquivo pertence a `desenvolvimento/`
- **THEN** ele não pode ser tratado como fonte do produto nem incluído pelo manifesto

#### Scenario: Adaptação editorial
- **WHEN** um documento em `publicacao/fontes/` adapta fontes canônicas
- **THEN** ele deve declarar aprovação e rastrear suas fontes sem substituí-las silenciosamente

### Requirement: Manifesto operacional único
`publicacao/manifest.yml` MUST ser a única lista positiva operacional de documentos publicados, com origem e destino explícitos por documento.

#### Scenario: Materialização normal
- **WHEN** a publicação é materializada
- **THEN** somente documentos ativos em `publicacao/manifest.yml` são copiados

#### Scenario: Manifesto histórico
- **WHEN** uma arquitetura anterior precisa ser preservada para auditoria
- **THEN** seu manifesto permanece em `historico/` e não é consultado pelo fluxo operacional

#### Scenario: Documento fora do manifesto
- **WHEN** uma fonte existe mas não está ativa no manifesto operacional
- **THEN** ela não entra em `publicacao/conteudo/` nem no sumário da release

### Requirement: Separação entre sumário-alvo e sumário da release
O projeto MUST usar `SUMMARY.md` como mapa da arquitetura modular pretendida e MUST gerar o sumário real da release a partir do manifesto operacional.

#### Scenario: Capítulo pendente no sumário-alvo
- **WHEN** `SUMMARY.md` referencia um marcador `recuperacao-pendente`
- **THEN** a referência descreve a arquitetura-alvo sem tornar o capítulo publicável

#### Scenario: Sumário da release
- **WHEN** o materializador gera `publicacao/conteudo/SUMMARY.md`
- **THEN** o arquivo lista apenas documentos ativos e válidos do manifesto

### Requirement: Caminhos canônicos estáveis para regras
A seção de regras MUST usar uma sequência única de caminhos numerados de acordo com a ordem editorial aprovada, sem duas posições iguais ou referências ativas aos nomes modulares anteriores.

#### Scenario: Migração de marcador
- **WHEN** um marcador de regra é movido para o caminho canônico-alvo
- **THEN** seu conteúdo e estado de recuperação permanecem equivalentes e o caminho anterior é registrado no mapa de migração

#### Scenario: Referência após migração
- **WHEN** documentos ativos referenciam um capítulo de regras
- **THEN** usam exclusivamente o caminho canônico-alvo

#### Scenario: Operações do Atlas
- **WHEN** a numeração das regras é consolidada
- **THEN** `regras/05-operacoes-do-atlas.md` permanece a fonte canônica integral em sua posição atual

### Requirement: Destino estável das aventuras
Aventuras completas e aprovadas MUST usar `campanha/aventuras/` como área de fonte, enquanto `publicacao/stubs/` MUST permanecer não publicável.

#### Scenario: Stub de aventura
- **WHEN** uma aventura possui `status: stub-gerado` ou `publicar: false`
- **THEN** ela permanece fora do manifesto operacional

#### Scenario: Aventura aprovada futuramente
- **WHEN** uma aventura completa for aprovada em mudança posterior
- **THEN** ela recebe caminho numerado estável em `campanha/aventuras/` antes de ser ativada no manifesto

### Requirement: Fronteiras de publicação
O materializador MUST rejeitar fontes em `desenvolvimento/`, `historico/`, `recuperacao/` e `publicacao/stubs/`, além de arquivos pendentes ou declarados não publicáveis.

#### Scenario: Fonte interna declarada no manifesto
- **WHEN** uma entrada ativa aponta para uma raiz proibida
- **THEN** a validação falha sem copiar o documento

#### Scenario: Marcador declarado no manifesto
- **WHEN** uma entrada ativa aponta para `status: recuperacao-pendente`
- **THEN** a validação falha sem materializar a publicação
