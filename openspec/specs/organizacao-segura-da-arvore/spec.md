# organizacao-segura-da-arvore Specification

## Purpose
TBD - created by archiving change configurar-backup-github-e-organizar-projeto. Update Purpose after archive.
## Requirements
### Requirement: Classificação das camadas do projeto
O projeto MUST distinguir fontes canônicas, adaptações editoriais, recuperação pendente, planejamento interno, histórico e saídas geradas, preservando a hierarquia definida em `AGENTS.md`.

#### Scenario: Documento interno
- **WHEN** um arquivo pertence a `desenvolvimento/`
- **THEN** ele é classificado como interno e não pode ser incluído no produto

#### Scenario: Fonte de recuperação pendente
- **WHEN** um arquivo possui `status: recuperacao-pendente`
- **THEN** ele é classificado como marcador não canônico e não publicável, sem ser removido automaticamente

#### Scenario: Saída gerada
- **WHEN** um arquivo pertence a `publicacao/conteudo/` ou `build/`
- **THEN** ele é tratado como descartável somente se puder ser reproduzido pelas fontes e ferramentas rastreadas

### Requirement: Política conservadora de rastreamento
A política Git MUST preservar fontes, inventários, marcadores, stubs, arquivos OpenSpec, planejamento, histórico necessário e arquivos `.keep` estruturais, ignorando somente caches e saídas comprovadamente regeneráveis.

#### Scenario: Cache Python
- **WHEN** um arquivo está em `__pycache__/` ou possui extensão `.pyc`
- **THEN** ele pode ser ignorado e removido sem integrar o baseline

#### Scenario: Estrutura vazia intencional
- **WHEN** um diretório necessário é preservado por um arquivo `.keep`
- **THEN** o `.keep` permanece rastreado e não é tratado como cache

### Requirement: Limpeza por lista positiva
Toda remoção MUST operar sobre uma lista explícita de caminhos aprovados e MUST excluir `.git/`, `openspec/`, fontes, inventários, marcadores, stubs e estruturas de continuidade.

#### Scenario: Remoção de descartáveis conhecidos
- **WHEN** caches ou saídas regeneráveis foram inventariados e aprovados
- **THEN** somente os caminhos listados são removidos

#### Scenario: Busca destrutiva global proposta
- **WHEN** uma operação tenta remover arquivos ou diretórios vazios a partir de toda a raiz do projeto
- **THEN** a operação é rejeitada antes da execução

### Requirement: Organização isolada e reversível
A organização MUST ocorrer em branch separada criada somente após a confirmação do backup remoto, e suas remoções MUST ser revisáveis em um diff antes do commit.

#### Scenario: Backup ainda não confirmado
- **WHEN** o baseline remoto ainda não foi verificado
- **THEN** nenhuma branch de limpeza executa remoções

#### Scenario: Diff contém fonte ou marcador
- **WHEN** o diff de organização remove uma fonte, um marcador de recuperação ou um inventário
- **THEN** o commit de organização é bloqueado até decisão explícita e revisão do escopo

### Requirement: Preservação editorial
A organização MUST NOT canonizar questões abertas, reescrever aventuras ou misturar conteúdo de Pacotes de Antagonista.

#### Scenario: Arquivo aberto durante a organização
- **WHEN** um documento registra uma decisão pendente ou hipótese de trabalho
- **THEN** seu conteúdo permanece não canônico e não é convertido em fato pela reorganização

### Requirement: Validação pós-organização
Após a limpeza, o projeto MUST validar o manifesto operacional, rematerializar os documentos atualmente aprovados e confirmar as contagens estruturais protegidas.

#### Scenario: Organização válida
- **WHEN** a limpeza aprovada termina
- **THEN** o manifesto permanece válido, três documentos atuais podem ser materializados, os 94 marcadores e os 23 stubs permanecem presentes e nenhuma fonte interna entra na publicação

#### Scenario: Regressão detectada
- **WHEN** uma validação falha ou uma contagem protegida muda inesperadamente
- **THEN** a organização não é considerada concluída e deve ser corrigida ou revertida
