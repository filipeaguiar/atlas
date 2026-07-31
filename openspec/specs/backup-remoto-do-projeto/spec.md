# backup-remoto-do-projeto Specification

## Purpose
TBD - created by archiving change configurar-backup-github-e-organizar-projeto. Update Purpose after archive.
## Requirements
### Requirement: Verificação prévia do destino remoto
O processo MUST verificar a autenticação do GitHub CLI, identificar o proprietário autenticado e verificar a existência do repositório `atlas` antes de criar ou enviar qualquer conteúdo.

#### Scenario: Destino disponível
- **WHEN** o GitHub CLI está autenticado e não existe um repositório `atlas` no proprietário selecionado
- **THEN** o processo pode prosseguir para a inspeção e criação do baseline

#### Scenario: Repositório homônimo existente
- **WHEN** já existe um repositório `atlas` no proprietário selecionado
- **THEN** o processo interrompe a criação sem sobrescrever, apagar ou enviar conteúdo ao repositório existente

#### Scenario: Autenticação indisponível
- **WHEN** o GitHub CLI não possui autenticação válida
- **THEN** o processo interrompe antes de modificar o remoto ou registrar uma origem Git

### Requirement: Repositório obrigatoriamente privado
O sistema MUST criar o repositório `atlas` com visibilidade privada e MUST confirmar essa visibilidade pela API ou pelo GitHub CLI antes de autorizar qualquer limpeza local.

#### Scenario: Repositório privado confirmado
- **WHEN** o repositório foi criado e sua visibilidade remota é consultada
- **THEN** a consulta retorna visibilidade privada e o processo registra a confirmação

#### Scenario: Visibilidade não privada
- **WHEN** a consulta remota não confirma visibilidade privada
- **THEN** nenhuma limpeza local é autorizada e o processo é interrompido para correção

### Requirement: Inspeção de conteúdo sensível
O processo MUST inspecionar a árvore a ser versionada para identificar credenciais, chaves privadas, tokens e arquivos locais sensíveis antes do primeiro push.

#### Scenario: Nenhum segredo detectado
- **WHEN** a inspeção não encontra material sensível conhecido
- **THEN** a criação do commit de baseline pode prosseguir

#### Scenario: Material suspeito detectado
- **WHEN** a inspeção identifica uma credencial, chave, token ou arquivo sensível
- **THEN** o push é bloqueado até que o item seja avaliado e tratado explicitamente

### Requirement: Baseline rastreável
O projeto MUST possuir um commit inicial na branch `main` e uma tag anotada `recovery-baseline-v1` que preservem todas as fontes, marcadores, inventários, stubs, documentos internos e estruturas necessárias à recuperação.

#### Scenario: Baseline criado
- **WHEN** a política de rastreamento foi aplicada e os arquivos preserváveis foram adicionados
- **THEN** um commit inicial e a tag `recovery-baseline-v1` apontam para um estado recuperável da árvore

#### Scenario: Marcador de recuperação no baseline
- **WHEN** um arquivo possui `status: recuperacao-pendente`
- **THEN** ele permanece rastreado no baseline, salvo decisão individual aprovada em mudança posterior

### Requirement: Verificação do backup remoto
O processo MUST enviar `main` e `recovery-baseline-v1` ao remoto privado e MUST comparar as referências locais e remotas antes de considerar o backup concluído.

#### Scenario: Referências sincronizadas
- **WHEN** o push termina com sucesso
- **THEN** o SHA remoto de `main` e a referência remota da tag correspondem ao baseline local

#### Scenario: Push parcial ou divergente
- **WHEN** a branch ou a tag não existe no remoto ou aponta para referência divergente
- **THEN** o backup não é considerado concluído e nenhuma limpeza local é autorizada

### Requirement: Restauração documentada
O projeto MUST registrar um procedimento de restauração que use o commit ou a tag de baseline sem reescrever ou remover a referência remota protegida.

#### Scenario: Arquivo removido por engano
- **WHEN** um arquivo rastreado é removido durante a organização
- **THEN** o procedimento permite restaurá-lo a partir de `recovery-baseline-v1`
