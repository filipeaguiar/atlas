## ADDED Requirements

### Requirement: Cobertura completa dos inimigos aprovados
A publicação SHALL incluir fichas completas para os nove antagonistas principais e os dezesseis tenentes existentes, após normalização de metadados e revisão editorial.

#### Scenario: Antagonistas principais
- **WHEN** o build percorre a seção de fichas de inimigos
- **THEN** Arquiteto, Ascendente, Hierofante, Mãe da Maré, Mecenas, Regente, Rei do Véu, Titã e Zero possuem fichas manifestadas

#### Scenario: Tenentes
- **WHEN** o build percorre os compêndios tecnológico, místico, super-humano e cósmico
- **THEN** cada compêndio contém quatro tenentes nomeados e mecanicamente completos

### Requirement: Cobertura completa dos NPCs aprovados
A publicação SHALL incluir fichas de redação atual para professores e funcionários apresentados na Aventura 1, os oito estudantes recorrentes e os seis integrantes da Vanguarda.

#### Scenario: Equipe do Atlas
- **WHEN** o Mestre consulta o compêndio da equipe do Atlas
- **THEN** Beatriz Leal, Álvaro Siqueira, Dalva Menezes, Dra. Samira Nasser, Lívia Monteiro, Caio Ventura, Janaína Rocha, Raul Farias e Tomás Valença possuem orientação e bloco mecânico

#### Scenario: Estudantes recorrentes
- **WHEN** o Mestre consulta o compêndio de estudantes
- **THEN** Lia, Ravi, Cecília, Noah, Malu, Ícaro, Sofia e Dante possuem fichas próximas ao patamar inicial dos personagens

#### Scenario: Vanguarda
- **WHEN** o Mestre consulta o compêndio da Vanguarda
- **THEN** Solar, Multiplex, Prisma, Colosso, Oráculo e Vetora possuem fichas de veteranos, sendo o bloco de Multiplex referenciado pela identidade secreta de Tomás sem criar estatísticas contraditórias

### Requirement: Estrutura mínima de ficha
Cada ficha SHALL informar nome, função de jogo, atributos P/H/R, PV e recursos aplicáveis, perícias, vantagens, limitações e pelo menos uma orientação operacional ou recurso exclusivo.

#### Scenario: Categoria não aplicável
- **WHEN** um personagem não usa PM, PA, tesouro ou técnica de combate
- **THEN** a categoria é omitida ou substituída por suporte aplicável, sem campo artificial vazio

#### Scenario: Consulta durante sessão
- **WHEN** o Mestre abre uma ficha
- **THEN** consegue identificar os números básicos, ações características e comportamento sem consultar planejamento interno

### Requirement: Agência dos personagens preservada
Fichas de professores, funcionários e veteranos SHALL apoiar, proteger, informar ou treinar sem resolver automaticamente Objetivos centrais destinados aos personagens dos jogadores.

#### Scenario: NPC adulto em cena de risco
- **WHEN** um adulto usa sua ficha ao lado da equipe dos jogadores
- **THEN** seus recursos concedem abertura, Ajuda ou contenção, mantendo a ação decisiva com os personagens

#### Scenario: Estudante recorrente em equipe
- **WHEN** um estudante recorrente participa de uma cena
- **THEN** sua especialidade oferece contribuição limitada e não substitui a solução dos jogadores

### Requirement: Proveniência editorial explícita
Fichas novas de NPCs SHALL declarar redação atual aprovada e MUST NOT ser apresentadas como recuperação dos stubs ausentes. Fichas existentes de inimigos SHALL receber metadados que descrevam corretamente sua origem editorial.

#### Scenario: Stub de recuperação pendente
- **WHEN** o pipeline encontra os arquivos antigos de corpo docente, alunos ou âncoras mecânicas
- **THEN** eles permanecem fora do manifesto e nenhum texto é copiado deles

#### Scenario: Ficha nova publicada
- **WHEN** uma ficha de NPC entra no manifesto
- **THEN** seu front matter registra `status: canon`, `publicar: true`, aprovação e origem de redação atual

### Requirement: Consistência mecânica e tom apropriado
As fichas SHALL usar terminologia de 3DeT Victory de forma consistente e MUST NOT depender de crueldade gráfica, morte obrigatória ou recompensa perigosa para funcionar.

#### Scenario: Efeito originalmente baseado em morte
- **WHEN** uma ficha bruta ativa um efeito por morte
- **THEN** a revisão o expressa por derrota, queda ou retirada mantendo função mecânica adequada

#### Scenario: Auditoria estrutural
- **WHEN** testes verificam os documentos manifestados
- **THEN** identidades, campos essenciais, valores e metadados obrigatórios passam sem referências a recuperação pendente

### Requirement: Seleção positiva e ordem
As fichas SHALL entrar no site e no livro somente após inclusão explícita e ordenada em `publicacao/manifest.yml`.

#### Scenario: Ficha canônica fora do manifesto
- **WHEN** uma ficha válida existe, mas não está declarada
- **THEN** ela não aparece no site publicado

#### Scenario: Compêndios manifestados
- **WHEN** todos os compêndios aprovados são adicionados à seção Regras
- **THEN** o site os publica na ordem NPCs, Vanguarda, tenentes e antagonistas principais definida pelo manifesto
