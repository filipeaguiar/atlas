## ADDED Requirements

### Requirement: Repositório remoto provisionado com GitHub CLI
O projeto SHALL usar a conta autenticada no `gh` para criar ou associar um repositório GitHub sem sobrescrever silenciosamente histórico remoto divergente.

#### Scenario: Nome remoto disponível
- **WHEN** o nome aprovado para o repositório não existe na conta autenticada
- **THEN** o processo cria o repositório com `gh repo create`, configura `origin` e preserva a branch local `main`

#### Scenario: Repositório compatível já existente
- **WHEN** o repositório de destino já existe e seu histórico é reconhecido como compatível
- **THEN** o processo reutiliza o repositório e configura `origin` sem criar uma duplicata

#### Scenario: Nome ocupado por histórico divergente
- **WHEN** o repositório de destino já existe, mas seu histórico não corresponde ao repositório local
- **THEN** o processo interrompe antes de configurar ou enviar alterações e solicita decisão explícita sobre nome novo, migração ou substituição

### Requirement: Build automatizado do site
O repositório SHALL possuir um workflow que, em push para `main` ou acionamento manual, instale uma versão fixada do Hugo Extended, execute testes e gere o site em modo estrito.

#### Scenario: Alteração válida em main
- **WHEN** uma alteração válida chega à branch `main`
- **THEN** o workflow produz um artefato Pages contendo exclusivamente a saída gerada do site

#### Scenario: Validação editorial falha
- **WHEN** manifesto, fonte, link, recurso ou teste viola uma regra de publicação
- **THEN** o workflow falha e não executa a implantação

### Requirement: Implantação pelo GitHub Pages
O workflow SHALL implantar o artefato estático por meio do ambiente `github-pages`, com permissões mínimas e ações oficiais do GitHub.

#### Scenario: Build aprovado
- **WHEN** o job de build e validação termina com sucesso
- **THEN** um job separado obtém `pages: write` e `id-token: write` e implanta o artefato com `actions/deploy-pages`

#### Scenario: Build reprovado
- **WHEN** o job de build falha
- **THEN** nenhum job de implantação publica uma nova versão

### Requirement: Exclusão de PDFs
O workflow e a configuração do Pages MUST NOT publicar arquivos PDF, saídas do gerador de PDF ou artefatos de release derivados desses arquivos.

#### Scenario: PDFs presentes no build local
- **WHEN** o diretório local `build/` contém PDFs gerados anteriormente
- **THEN** nenhum PDF é copiado para `build/site/` ou incluído no artefato Pages

### Requirement: URL compatível com site de projeto
O build SHALL usar a URL efetiva fornecida pela configuração do GitHub Pages, sem fixar proprietário, repositório ou domínio no tema.

#### Scenario: Repositório publicado em subdiretório
- **WHEN** o Pages fornece uma URL no formato `https://<conta>.github.io/<repositorio>/`
- **THEN** páginas, folhas de estilo, scripts, imagens e navegação funcionam sob esse subdiretório

### Requirement: Artefato sem áreas internas
O artefato enviado ao Pages MUST NOT conter fontes ou derivados de áreas excluídas, incluindo `desenvolvimento/`, `historico/`, `recuperacao/`, `referencias/`, `openspec/`, `publicacao/stubs/`, `publicacao/conteudo/` e outras saídas não selecionadas.

#### Scenario: Arquivo interno presente no repositório
- **WHEN** o workflow constrói o site em um checkout que contém planejamento, referências e histórico
- **THEN** apenas a árvore positiva gerada em `build/site/` é enviada ao Pages

#### Scenario: Verificação negativa encontra vazamento
- **WHEN** a auditoria do artefato encontra caminho ou conteúdo proveniente de área excluída
- **THEN** o build falha antes do upload

### Requirement: Falha operacional segura
O processo SHALL documentar e verificar as pré-condições de remoto, visibilidade e origem GitHub Actions antes do primeiro deploy.

#### Scenario: Pages indisponível para a visibilidade escolhida
- **WHEN** o plano da conta não permite Pages para a visibilidade configurada
- **THEN** o processo interrompe com orientação para tornar o repositório público, ajustar o plano ou escolher outro destino, sem alterar a seleção editorial
