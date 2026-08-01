## ADDED Requirements

### Requirement: Segredos publicáveis respeitam a camada do Mestre
Uma reescrita de fundamentos da campanha MAY incluir segredos autorizados para preparação, mas MUST declarar sua camada do Mestre e MUST preservar a distinção entre conhecimento editorial, conhecimento de NPC e conhecimento inicial dos personagens.

#### Scenario: Identidade de Multiplex no capítulo do Mestre
- **WHEN** um fundamento da campanha explica que Tomás é Multiplex
- **THEN** a informação é apresentada como segredo do Mestre e não como fato conhecido pelos alunos no início

#### Scenario: Referência a capítulo público
- **WHEN** o fundamento remete a Vanguarda ou Tragédia em capítulo público de cenário
- **THEN** a referência não altera nem contamina a versão pública desse capítulo com a verdade secreta

### Requirement: Operação fixa não implica resultado físico fixo
A reescrita MUST distinguir a ocorrência estrutural de uma operação das consequências produzidas pelas decisões dos personagens.

#### Scenario: Segunda operação na Aventura 14
- **WHEN** a estrutura registra a segunda operação de captura na Aventura 14
- **THEN** não afirma que a captura física necessariamente acontece e encaminha qualquer resultado para as consequências da Aventura 15

#### Scenario: Preparação para estados alternativos
- **WHEN** êxito, impedimento, retirada ou complicação são resultados coerentes
- **THEN** o texto orienta o Mestre a preservar o estado produzido e adaptar pressões posteriores sem invalidar a ação dos personagens

### Requirement: Transição dos fundamentos da campanha é auditável
A substituição dos seis marcadores estruturais MUST preservar hashes, declarar que o original integral não foi recuperado e manter inventário, manifesto e estado físico consistentes.

#### Scenario: Seis capítulos aprovados
- **WHEN** todos os fundamentos da campanha passam pela revisão
- **THEN** o inventário acumula 15 estados `reescrito-aprovado`, a contagem pendente passa de 85 para 79 e o manifesto contém 18 documentos ativos

#### Scenario: Capítulo reprovado
- **WHEN** um capítulo contém fato sem fonte, resultado obrigatório indevido ou variável de Pacote apresentada como fixa
- **THEN** ele não é ativado e as contagens refletem apenas os capítulos efetivamente aprovados
