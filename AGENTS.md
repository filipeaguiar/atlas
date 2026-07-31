# AGENTS.md

## Escopo

Estas instruções regem a árvore reconstruída de **Instituto Atlas e a Tragédia de Belamar**.

## Hierarquia das fontes

1. Consulte primeiro `cenario/`, `campanha/`, `regras/` e `apendices/`; aventuras completas e aprovadas pertencem a `campanha/aventuras/`.
2. Arquivos com `status: recuperacao-pendente` não são fonte canônica e não podem ser citados como conteúdo existente.
3. `publicacao/fontes/` contém apenas adaptações editoriais aprovadas e deve rastrear suas fontes canônicas.
4. `publicacao/manifest.yml` é a única lista positiva operacional da publicação.
5. `SUMMARY.md` é o sumário-alvo das fontes; `publicacao/conteudo/SUMMARY.md` é uma saída gerada da release.
6. `publicacao/conteudo/` e `build/` são saídas descartáveis.
7. `historico/` e `recuperacao/` servem apenas para auditoria e recuperação.
8. `desenvolvimento/` contém planejamento, continuidade e decisões internas; nunca deve entrar no livro.

## Cânone e lacunas

- Não transforme uma questão em aberto em cânone sem aprovação explícita.
- Não complete silenciosamente conteúdo ausente durante a recuperação.
- Preserve a distinção entre fato fixo, opção do Pacote de Antagonista, consequência condicional e hipótese de trabalho.
- A segunda operação de captura ocorre na Aventura 14; a captura física é condicional. A Aventura 15 trata das consequências e a 16 conclui o Arco II.

## Escrita de aventuras

- Prepare situações e pressões, não sequências obrigatórias.
- Preserve a agência dos personagens e aceite soluções inesperadas coerentes.
- Informação indispensável não depende de uma única rolagem.
- Professores e veteranos oferecem apoio sem tomar o protagonismo.
- Use as regras de 3DeT Victory, incluindo Ganho, Perda, Ajuda, Pontos de Ação, Objetivos, XP e Marcos.
- Mantenha o tom apropriado para crianças e pré-adolescentes, sem crueldade gráfica.

## Publicação

- Um arquivo só entra no produto quando `publicacao/manifest.yml` o declara e ele não está marcado `publicar: false`.
- Stubs, prompts, checklists, decisões internas, estados de continuidade e notas de pipeline não entram na publicação.
- Stubs permanecem em `publicacao/stubs/`; quando uma aventura estiver completa e aprovada, ela deve migrar para `campanha/aventuras/` antes de entrar no manifesto.
- O materializador deve recusar fontes dentro de `desenvolvimento/`, `historico/`, `recuperacao/` e `publicacao/stubs/`.
