## Why

O projeto foi reconstruído sem histórico de versão e contém fontes canônicas, marcadores de recuperação, documentos internos e saídas geradas misturados. Antes de reorganizar ou remover arquivos, é necessário preservar um baseline verificável em um repositório privado e estabelecer regras que tornem a limpeza reversível, auditável e compatível com a futura publicação do módulo em PDF.

## What Changes

- Criar no GitHub um repositório privado chamado `atlas`, após verificar autenticação, proprietário e ausência de segredos que não devam ser enviados.
- Registrar a árvore recuperada em um commit inicial, criar uma tag de baseline e publicar ambos no remoto privado.
- Confirmar a visibilidade privada e a integridade do baseline remoto antes de qualquer remoção.
- Definir uma política de rastreamento que preserve fontes, marcadores, inventários, planejamento e estruturas necessárias, separando apenas caches e saídas comprovadamente regeneráveis.
- Classificar a árvore por fonte canônica, recuperação, desenvolvimento interno, histórico e saída gerada.
- Realizar a organização em branch própria, com inventário prévio, diffs revisáveis e possibilidade de restauração.
- Restringir limpezas a alvos explicitamente aprovados; proibir buscas destrutivas globais que alcancem `.git`, OpenSpec, estruturas editoriais ou diretórios de continuidade.
- Remover somente caches e saídas regeneráveis nesta mudança. Marcadores `recuperacao-pendente` e fontes históricas só poderão ser removidos após decisão individual registrada sobre seu destino.
- Validar, depois da organização, o manifesto operacional, referências essenciais, inventário de recuperação e capacidade de rematerializar a publicação atual.

## Capabilities

### New Capabilities

- `backup-remoto-do-projeto`: Preservação verificável da árvore recuperada em repositório privado, com commit e tag de baseline, validação do remoto e procedimento de restauração.
- `organizacao-segura-da-arvore`: Classificação das camadas do projeto e limpeza controlada, reversível e limitada a arquivos comprovadamente descartáveis.

### Modified Capabilities

Nenhuma.

## Impact

- Repositório Git local recém-inicializado e novo repositório privado no GitHub.
- Arquivos de governança e política de rastreamento na raiz do projeto.
- Estrutura de `cenario/`, `campanha/`, `regras/`, `apendices/`, `desenvolvimento/`, `recuperacao/`, `historico/`, `publicacao/`, `assets/`, `build/` e `tools/`.
- Scripts de validação e materialização existentes, que deverão continuar funcionando após a organização.
- Nenhum conteúdo narrativo novo será canonizado e nenhuma aventura será implementada nesta mudança.
