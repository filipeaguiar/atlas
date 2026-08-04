## ADDED Requirements

### Requirement: Materialização preserva ordem e proveniência
O materializador MUST copiar apenas fontes validadas para `publicacao/conteudo/`, gerar sumário e documento combinado e registrar hash de cada origem.

#### Scenario: Materialização repetida
- **WHEN** manifesto e fontes permanecem iguais
- **THEN** a seleção, ordem, hashes e digest de entrada permanecem iguais

#### Scenario: Saída antiga presente
- **WHEN** uma nova materialização começa
- **THEN** a área derivada é reconstruída sem tratar arquivos antigos como fontes

### Requirement: HTML e PDF são gerados localmente
O sistema MUST converter Markdown materializado em HTML estilizado e usar Google Chrome headless para produzir o PDF versionado sem acesso de rede.

#### Scenario: Ambiente válido
- **WHEN** Chrome e dependências Python estão disponíveis
- **THEN** o build produz HTML e PDF não vazios com capa e sumário

#### Scenario: Chrome indisponível
- **WHEN** nenhum executável aceito é encontrado
- **THEN** o build falha com instrução para configurar `CHROME_BIN`

### Requirement: Estrutura visual atende ao preview editorial
O PDF MUST apresentar capa, identificação de versão, sumário navegável, hierarquia de títulos, seções, tabelas legíveis, quebras de capítulo e numeração de páginas.

#### Scenario: Capítulo inicia
- **WHEN** um novo documento do manifesto é renderizado
- **THEN** ele começa em página nova e recebe âncora estável no sumário

#### Scenario: Versão de desenvolvimento
- **WHEN** a versão contém marcador `dev`
- **THEN** capa ou rodapé informa claramente que se trata de material em desenvolvimento

### Requirement: Handout separa orientação e página entregável
O gerador MUST renderizar metadados de uso para o Mestre e isolar o corpo entregável após quebra de página, sem gerar PDF público ou arquivo independente automaticamente.

#### Scenario: Handout renderizado
- **WHEN** um handout possui orientação, condição de entrega e revelações no front matter
- **THEN** essas instruções aparecem antes da página entregável no módulo

#### Scenario: Handout sem metadados obrigatórios
- **WHEN** um item declarado como handout não informa sua orientação de uso
- **THEN** a validação falha antes de gerar o PDF

### Requirement: Modo incremental registra lacunas
O build padrão MAY aceitar links ou recursos locais ainda indisponíveis, mas MUST registrá-los no relatório e MUST NOT ocultar a pendência.

#### Scenario: Link aponta para capítulo futuro
- **WHEN** o alvo não existe e o modo incremental está ativo
- **THEN** o PDF é produzido e o relatório identifica origem e alvo ausente

#### Scenario: Fonte do manifesto ausente
- **WHEN** o próprio documento declarado não existe
- **THEN** o build falha mesmo em modo incremental

### Requirement: Modo estrito bloqueia pendências
O parâmetro `--strict` MUST transformar links e recursos locais ausentes em erros.

#### Scenario: Release sem lacunas
- **WHEN** todas as fontes, links e recursos são válidos
- **THEN** o modo estrito produz o mesmo conjunto ordenado de conteúdo sem avisos de integridade

#### Scenario: Link quebrado em modo estrito
- **WHEN** qualquer fonte contém referência local sem alvo
- **THEN** nenhum PDF estrito é considerado concluído

### Requirement: Relatório descreve cada artefato
Cada execução bem-sucedida MUST gerar relatório com versão, modo, navegador, fontes, hashes, avisos, digest e caminhos dos artefatos.

#### Scenario: PDF incremental concluído
- **WHEN** o Chrome termina com sucesso e o arquivo não está vazio
- **THEN** o relatório associa explicitamente o PDF ao manifesto e aos hashes processados

### Requirement: Áreas proibidas nunca entram no livro
O gerador MUST recusar `referencias/`, índices Chonkie, planejamento, recuperação, histórico, stubs e saídas geradas como fontes.

#### Scenario: Livro de regras externo no manifesto
- **WHEN** um arquivo integral de referência é declarado direta ou indiretamente
- **THEN** o build falha antes de copiar conteúdo protegido
