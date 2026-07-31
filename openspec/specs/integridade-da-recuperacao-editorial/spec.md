# integridade-da-recuperacao-editorial Specification

## Purpose
TBD - created by archiving change consolidar-arquitetura-editorial. Update Purpose after archive.
## Requirements
### Requirement: Inventário confrontado com o sistema de arquivos
O inventário de recuperação MUST registrar os documentos editoriais esperados e MUST ser validado contra sua existência física, caminho atual e estado declarado.

#### Scenario: Marcador listado e presente
- **WHEN** um registro é classificado como `recuperacao-pendente`
- **THEN** o caminho físico existe, contém o status esperado e permanece não publicável

#### Scenario: Marcador listado e ausente
- **WHEN** o inventário espera um marcador que não existe no caminho atual
- **THEN** a validação falha e identifica o caminho ausente

#### Scenario: Marcador físico não inventariado
- **WHEN** um arquivo físico possui `status: recuperacao-pendente` mas não aparece no inventário
- **THEN** a validação falha e identifica o registro faltante

### Requirement: Migração de caminhos auditável
Toda mudança de caminho de um documento inventariado MUST registrar caminho anterior, caminho atual e motivo, sem alterar automaticamente seu estado de recuperação.

#### Scenario: Regra renumerada
- **WHEN** um marcador de regras é renomeado durante a consolidação
- **THEN** o inventário preserva o caminho anterior e aponta para o novo caminho físico

#### Scenario: Busca por caminho antigo
- **WHEN** a migração termina
- **THEN** o caminho antigo aparece apenas em histórico ou registros explícitos de migração, nunca como referência editorial ativa

### Requirement: Ciclo de vida explícito dos marcadores
Cada marcador MUST permanecer preservado até receber uma decisão explícita de recuperação, reescrita aprovada, substituição com migração ou retirada de escopo.

#### Scenario: Conteúdo original recuperado
- **WHEN** o conteúdo integral correspondente é recuperado e validado
- **THEN** a substituição do marcador registra origem e aprovação antes de alterar seu status

#### Scenario: Conteúdo precisa ser reescrito
- **WHEN** a versão original não está disponível
- **THEN** o marcador só é substituído por texto novo em mudança própria, sem apresentar a reescrita como recuperação

#### Scenario: Nenhuma decisão aprovada
- **WHEN** não existe decisão sobre o destino do marcador
- **THEN** ele permanece `recuperacao-pendente` e `publicar: false`

### Requirement: Validação de links locais
O projeto MUST detectar links Markdown locais quebrados nas fontes modulares, adaptações editoriais e documentação operacional aplicável.

#### Scenario: Link válido
- **WHEN** um documento referencia um caminho local existente
- **THEN** a validação aceita a referência mesmo que o destino seja um marcador não publicável

#### Scenario: Link quebrado
- **WHEN** um documento referencia um caminho local inexistente
- **THEN** a validação falha e informa documento de origem e destino ausente

#### Scenario: Link histórico intencional
- **WHEN** um documento histórico preserva referência de uma árvore anterior
- **THEN** a regra de links ativos não o interpreta como caminho operacional atual

### Requirement: Coerência entre manifesto, inventário e metadados
As validações MUST comparar entradas do manifesto com o inventário e o front matter das fontes para impedir status ou destinos incompatíveis.

#### Scenario: Fonte ativa aprovada
- **WHEN** uma entrada do manifesto aponta para fonte existente, aprovada e publicável
- **THEN** seu destino é único e a entrada é aceita

#### Scenario: Destino duplicado
- **WHEN** duas entradas ativas usam o mesmo destino
- **THEN** a validação falha antes da materialização

#### Scenario: Status incompatível
- **WHEN** o manifesto ativa uma fonte que o inventário ou front matter classifica como pendente, stub ou não publicável
- **THEN** a validação falha e identifica a divergência

### Requirement: Validações automatizadas bloqueantes
Os verificadores de recuperação e arquitetura MUST retornar código diferente de zero diante de erro e MUST distinguir erros bloqueantes de avisos informativos.

#### Scenario: Projeto íntegro
- **WHEN** caminhos, status, links, manifesto e contagens estão coerentes
- **THEN** os verificadores terminam com sucesso e apresentam resumo verificável

#### Scenario: Regressão estrutural
- **WHEN** um marcador protegido desaparece, um link ativo quebra ou uma fonte interna é ativada
- **THEN** pelo menos um verificador termina com falha antes da publicação
