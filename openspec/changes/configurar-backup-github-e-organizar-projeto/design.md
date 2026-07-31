## Context

A árvore atual foi reconstruída sem histórico Git. Ela contém 94 marcadores de recuperação, 23 stubs não publicáveis, uma fonte editorial completa, duas fontes completas de regras, documentação interna, inventários históricos e saídas geradas. O repositório Git foi inicializado, mas ainda não possui commits nem arquivos rastreados. A publicação operacional materializa somente três documentos, e a recuperação depende da preservação dos caminhos e metadados pendentes.

A mudança envolve um serviço externo, o GitHub, e operações potencialmente destrutivas no sistema de arquivos. Por isso o backup remoto verificável deve preceder qualquer limpeza.

## Goals / Non-Goals

**Goals:**

- criar um repositório GitHub privado chamado `atlas` no proprietário autenticado pelo `gh`;
- preservar fontes, marcadores, inventários e planejamento em um commit e uma tag de baseline;
- comprovar que o commit e a tag existem no remoto privado;
- estabelecer rastreamento e classificação coerentes para a árvore;
- remover somente caches e saídas comprovadamente regeneráveis;
- manter materialização e verificações operacionais funcionando;
- tornar toda organização posterior revisável e reversível.

**Non-Goals:**

- recuperar ou reescrever os 94 documentos pendentes;
- escrever as 23 aventuras;
- selecionar Pacote de Antagonista ou canonizar questões abertas;
- construir o gerador do PDF final;
- remover marcadores, fontes históricas ou estruturas de continuidade;
- tornar o repositório público.

## Decisions

### 1. Verificar antes de publicar

A aplicação verificará `gh auth status`, o proprietário autenticado, a inexistência ou situação do repositório de destino e possíveis credenciais ou arquivos sensíveis antes do primeiro commit e push. Se `atlas` já existir, a operação será interrompida para decisão explícita, sem alterar ou sobrescrever o remoto existente.

Alternativa considerada: criar o remoto imediatamente. Rejeitada porque um repositório homônimo ou conteúdo sensível pode produzir perda ou exposição acidental.

### 2. Usar `main`, commit inicial e tag imutável de baseline

A branch inicial será renomeada para `main`. A árvore preservável será registrada em um commit inicial e marcada por uma tag anotada `recovery-baseline-v1`. O SHA local deverá coincidir com as referências remotas antes da limpeza.

Alternativa considerada: depender apenas do estado local. Rejeitada porque não protege contra perda da pasta ou do diretório `.git`.

### 3. Ignorar somente artefatos comprovadamente regeneráveis

A política inicial de rastreamento excluirá caches Python e saídas geradas como `tools/__pycache__/`, `*.pyc`, `publicacao/conteudo/` e `build/`. Serão preservados no Git os marcadores `recuperacao-pendente`, `publicacao/fontes-legado-97/`, inventários, stubs, arquivos OpenSpec, documentos internos e arquivos `.keep` estruturais.

A exclusão de uma saída pressupõe que suas fontes e ferramentas estejam rastreadas. Se uma verificação mostrar conteúdo único em uma área considerada gerada, ela será preservada até decisão posterior.

Alternativa considerada: ignorar toda a reconstrução e versionar apenas documentos publicáveis. Rejeitada porque eliminaria a capacidade de auditar e retomar a recuperação.

### 4. Separar baseline e organização

O baseline será criado e enviado a partir de `main`. A organização ocorrerá em branch dedicada, depois da confirmação remota. Cada grupo de remoções terá inventário prévio e diff posterior. Mudanças de conteúdo não serão misturadas à limpeza.

Alternativa considerada: limpar antes do primeiro commit. Rejeitada porque arquivos não rastreados não podem ser restaurados pelo Git.

### 5. Proibir limpeza global da raiz

Nenhuma tarefa usará `find . ... -delete` ou equivalente sobre toda a raiz. Remoções serão feitas por lista positiva de caminhos descartáveis. `.git/`, `openspec/`, `assets/`, estruturas de continuidade e fontes editoriais ficam fora de qualquer limpeza genérica.

### 6. Validar o estado pós-organização

A mudança deverá confirmar:

- remoto privado e referências sincronizadas;
- árvore Git sem mudanças inesperadas;
- manifesto operacional válido;
- materialização reproduzível dos três documentos atuais;
- ausência de fontes internas no conteúdo gerado;
- permanência dos 94 marcadores e dos 23 stubs;
- registro explícito de qualquer referência já quebrada que não pertença ao escopo desta mudança.

## Risks / Trade-offs

- **[Segredo enviado ao remoto]** → executar inspeção prévia e interromper diante de credenciais suspeitas.
- **[Repositório `atlas` já existe]** → não reutilizar, sobrescrever ou apagar sem aprovação explícita.
- **[Confiança indevida no Git local]** → exigir push e comparação dos SHAs no remoto privado.
- **[Saída classificada incorretamente como regenerável]** → validar reprodução antes da remoção e preservar qualquer conteúdo único.
- **[Histórico privado contém material removido depois]** → aceitar isso como objetivo do baseline; manter o repositório privado.
- **[Organização vira reescrita editorial]** → limitar a mudança a governança, rastreamento e descartáveis.
- **[Limpeza quebra referências existentes]** → não remover marcadores nesta mudança e executar verificações antes e depois.

## Migration Plan

1. Inspecionar autenticação do `gh`, proprietário e destino remoto.
2. Inspecionar arquivos sensíveis e classificar artefatos regeneráveis.
3. Criar política de rastreamento mínima.
4. Renomear a branch para `main` e registrar o commit inicial.
5. Criar a tag anotada `recovery-baseline-v1`.
6. Criar `atlas` como repositório privado e enviar branch e tag.
7. Verificar visibilidade, remoto, SHA da branch e SHA da tag.
8. Criar branch dedicada à organização.
9. Remover somente caches e saídas regeneráveis aprovadas.
10. Executar validações, revisar o diff e registrar a organização em commit separado.
11. Enviar a branch de organização sem incorporá-la automaticamente a `main`.

**Rollback:** antes do commit de organização, usar restauração a partir do índice; depois dele, restaurar caminhos ou reverter o commit usando `recovery-baseline-v1` como referência. O remoto ou a tag não serão reescritos.

## Open Questions

- Qual conta ou organização aparecerá como proprietária no `gh auth status`? A aplicação usará o proprietário autenticado, mas deverá reportá-lo antes da criação.
- O repositório `atlas` já existe nesse proprietário? Se existir, será necessária uma nova decisão de nome ou destino.
