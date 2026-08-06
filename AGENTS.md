# Campanha de RPG — Herdeiros da Vanguarda (Regras Operacionais para IA)

## Diretrizes de Criação de Conteúdo e Cânone

O foco principal deste projeto é a criação do **módulo de campanha para RPG** para o sistema **3DeT Victory**. Este arquivo dita as **Regras Operacionais** do repositório. Para diretrizes de roteiro e game design, consulte os arquivos dentro da pasta `campanha/`.

### Regra de Ouro do Cânone
- **Nunca invente cânone ou preencha lacunas silenciosamente.**
- Não transforme uma "questão em aberto" em cânone sem aprovação explícita do usuário.
- Preserve a distinção entre: fato fixo do cenário, opção do Pacote de Antagonista, consequência condicional e hipótese de trabalho.

### Estrutura e Camadas (Pastas)
- **Fontes Editoriais Aprovadas:** `cenario/`, `campanha/`, `regras/` e `apendices/`.
- **Aventuras:** Aventuras *completas e aprovadas* pertencem a `campanha/aventuras/`. Enquanto forem rascunhos (stubs), devem ficar em `publicacao/stubs/` e nunca devem ser publicadas.
- **Multimídia e Especificações:** Preserve as fontes e estruturas da pasta `assets/`. Propostas, designs e tarefas de agentes devem ser mantidas em `openspec/`.
- **Referências Externas:** Os arquivos em `referencias/` são os livros base do 3DeT Victory.
- **Áreas Internas:** `desenvolvimento/`, `historico/` e `recuperacao/` são de uso interno. `build/` e `publicacao/conteudo/` são descartáveis.

### Prompts Personalizados e Geração de Conteúdo
- Todo novo conteúdo do módulo deve ser planejado e gerado utilizando **prompts personalizados**, garantindo que as IAs respeitem o escopo e separação de camadas.
- A saída das gerações deve ser direcionada para as pastas de fontes editoriais aprovadas.

### Uso do Chonkie (Indexação e Fragmentação)
- A ferramenta Chonkie serve para fragmentar fontes já aprovadas, bem como obter fragmentos de regras e de outros tipos a partir dos materiais de referência.
- O índice não define cânone, não comprova proveniência e não substitui a leitura da fonte.
- Nunca indexe a cópia `.bkp`, marcadores pendentes, stubs, histórico ou planejamento interno.
- Preserve índices separados para conteúdo público e conteúdo do Mestre.
- Não versione arquivos sob `build/retrieval/`.

---

## Processo de Recuperação e Backup (Secundário)

A restauração de conteúdo antigo não é o objetivo central, mas como o repositório de backup possui grande volume de informações úteis, aplicam-se estas regras:

### Reconstrução Seletiva
- Este repositório é a nova árvore editorial.
- O diretório `/home/filipe/Documentos/Projetos/Atlas.bkp` é para **consulta somente leitura**; nunca copie sua árvore integralmente nem a indexe diretamente.
- A recuperação deve ocorrer um documento por vez, exigindo revisão, proveniência e aprovação explícitas.
- O conteúdo da cópia de segurança não se torna canônico apenas por existir. Arquivos marcados com `status: recuperacao-pendente` não são fontes canônicas.
