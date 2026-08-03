## ADDED Requirements

### Requirement: Somente fontes aprovadas são indexadas
O indexador MUST processar apenas Markdown das raízes editoriais permitidas com `status: canon` e MUST recusar fontes internas, históricas, pendentes ou derivadas.

#### Scenario: Marcador pendente
- **WHEN** um arquivo possui `status: recuperacao-pendente`
- **THEN** nenhum fragmento desse arquivo aparece no índice

#### Scenario: Cópia de segurança externa
- **WHEN** `Atlas.bkp` existe ao lado do projeto
- **THEN** o indexador não lê nem resolve caminhos fora da raiz atual

### Requirement: Audiências permanecem isoladas
O indexador MUST gerar perfis separados para conteúdo público e conteúdo do Mestre.

#### Scenario: Segredo do Mestre
- **WHEN** um documento declara `camada: mestre` ou `conteudo_para_jogadores: false`
- **THEN** ele pode entrar no índice do Mestre e não entra no índice público

### Requirement: Fragmentos preservam proveniência
Cada fragmento MUST registrar caminho, hash da fonte, índices, contagem, cabeçalho aplicável e metadados editoriais.

#### Scenario: Índice regenerado sem alterações
- **WHEN** as mesmas fontes e configuração são processadas novamente
- **THEN** o JSON e os IDs dos fragmentos permanecem idênticos

### Requirement: Índice é derivado e descartável
A saída MUST permanecer sob `build/retrieval/` e MUST NOT alterar fontes ou participar da publicação.

#### Scenario: Execução normal
- **WHEN** o comando de indexação termina
- **THEN** somente o JSON derivado configurado é criado ou substituído
