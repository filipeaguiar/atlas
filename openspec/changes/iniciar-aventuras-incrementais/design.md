## Context

As fontes canônicas atuais fixam 23 aventuras em três arcos, a progressão de licenças, a abertura pelo Exame de Admissão e as funções especiais das Aventuras 14, 15 e 16. Elas não fixam todas as funções intermediárias, o Pacote de Antagonista ou os resultados das operações. Não há aventuras rastreadas no repositório atual, e os documentos de arco referenciados por `campanha/03-arcos.md` ainda estão ausentes.

A escrita precisa avançar sem converter planejamento em cânone, sem depender de uma sequência obrigatória e sem publicar um rascunho apenas porque ele existe na árvore. O PDF já usa seleção positiva por manifesto e fornece o mecanismo final de integração.

## Goals / Non-Goals

**Goals:**

- tornar visível a arquitetura das 23 posições sem preencher silenciosamente lacunas;
- estabelecer um formato repetível para aventuras abertas e jogáveis;
- escrever e revisar a Aventura 1 antes de escalar o processo;
- corrigir os documentos de arco ausentes apenas com fatos já aprovados;
- integrar ao livro somente a versão explicitamente aprovada do piloto.

**Non-Goals:**

- escrever as 23 aventuras nesta mudança;
- escolher um Pacote de Antagonista;
- definir resultados físicos obrigatórios para operações de captura;
- recuperar em massa aventuras, stubs ou planejamento do backup;
- publicar o grafo editorial ou qualquer checklist interno no módulo.

## Decisions

### O grafo Mermaid será uma ferramenta editorial interna

O mapa ficará em `desenvolvimento/planejamento/mapa-da-saga.md`, fora do manifesto. Ele conterá 23 nós agrupados por arco e uma legenda visual para quatro classes: fato fixo, consequência condicional, variável do Pacote e lacuna editorial.

Isso permite mapear a saga completa sem apresentar posições indefinidas como conteúdo do livro. A alternativa de publicar imediatamente o grafo foi rejeitada porque ele conterá estado de planejamento e poderá mudar a cada aventura aprovada.

### O grafo representa progressão e dependências, não roteiro de cenas

A aresta principal indica sucessão editorial das posições. Arestas adicionais só serão usadas para dependências de informação, Marcos ou consequências persistentes. Resultados alternativos serão anotados no mesmo nó ou ligados a estados abstratos, sem criar um “caminho correto”.

### Cada aventura terá um contrato editorial estável e execução pronta

O piloto usará a estrutura definida pelo usuário: título; resumo sem subtítulo próprio e com leitura em voz alta; `A história até aqui`; cenas nomeadas em sequência; e material final de consulta com fichas pertinentes, experiência e encerramento. Função estrutural, proveniência e estado editorial permanecem nos metadados ou no planejamento, sem virar seções do capítulo.

NPCs, lugares, regras, desafios e alternativas aparecem dentro da cena em que entram na narrativa. As cenas terão uma sequência principal e transições prontas, para que o Mestre não precise consultar capítulos intermediários de planejamento. Alternativas são permitidas quando possuem gatilho objetivo, conteúdo definido, consequência própria e ponto explícito de retorno ou avanço. Dentro de cada cena, os jogadores preservam liberdade de abordagem e suas soluções alteram consequências sem exigir improvisação estrutural do Mestre.

### O texto distinguirá preparação e leitura em voz alta

O resumo e cada cena principal terão um bloco breve marcado **Leia em voz alta**. Esses blocos apresentarão ambiente, atmosfera e primeira impressão de NPCs sem antecipar critérios ocultos, consequências ou segredos. Aparência, interpretação e função de cada NPC serão descritas na primeira cena em que ele interagir; localidades e desafios também serão apresentados quando surgirem. Como os perfis integrais não sobreviveram no backup, essas caracterizações permanecem texto novo até aprovação.

### Aprovação e publicação serão etapas separadas

A primeira redação da aventura terá estado de revisão e não entrará no manifesto. Depois de revisão explícita, seus metadados poderão mudar para canônico e publicável; somente então ela será incluída na lista positiva e no PDF. O grafo registra essa passagem de estado, mas não concede aprovação.

### O Exame de Admissão será neutro quanto ao Pacote

A Aventura 1 apresentará Atlas, relações, cooperação, controle, resgate e julgamento. Ela não escolherá antagonista, Tenente Principal, família de sinais ou explicação secreta. Qualquer gancho opcional ligado ao Retorno será identificado como variável e não será necessário para concluir a aventura.

### Recuperação será seletiva e verificável

Fontes candidatas no backup poderão ser consultadas individualmente. Conteúdo incorporado deverá registrar proveniência e distinguir transcrição, adaptação e texto novo. Arquivos `recuperacao-pendente`, stubs e planejamento não serão tratados como texto recuperado existente.

## Risks / Trade-offs

- **[Mapa com aparência de cânone]** → manter o Mermaid em `desenvolvimento/`, usar legenda explícita e proibir sua entrada no manifesto.
- **[Sequência de cenas fechar escolhas dos personagens]** → fixar a preparação e as transições para o Mestre, mas manter abordagens, uso de capacidades e resultados locais abertos aos jogadores.
- **[Falta de Pacote enfraquecer conexões futuras]** → manter o Exame funcionalmente independente e registrar apenas pontos de extensão opcionais.
- **[Aprovação implícita durante implementação]** → interromper a publicação no gate de revisão até manifestação explícita do usuário.
- **[Detalhamento prematuro das 23 posições]** → representar lacunas como lacunas e atualizar o grafo somente por mudanças revisadas.
- **[Mecânicas incorretas de 3DeT Victory]** → consultar o índice local de referências, conferir o texto fonte relevante e não publicar trechos protegidos.

## Migration Plan

1. Auditar seletivamente fontes candidatas e fatos canônicos disponíveis.
2. Criar o grafo editorial inicial e os três documentos de arco com escopo aprovado.
3. Criar modelo e verificações automatizadas de aventura.
4. Redigir a Aventura 1 em estado de revisão.
5. Submeter o piloto à revisão explícita.
6. Após aprovação, tornar o arquivo publicável, adicioná-lo ao manifesto e gerar nova versão incremental do PDF.
7. Usar o piloto aprovado como base para uma mudança separada ou lote pequeno de aventuras seguintes.

A reversão remove o piloto do manifesto e restaura a versão anterior do PDF; fontes e histórico de revisão permanecem rastreáveis.

## Open Questions

- Qual Pacote de Antagonista será usado nas aventuras que dependem do Retorno?
- Quais colegas, professores e relações recorrentes devem estrear no Exame?
- O grafo editorial deverá futuramente ganhar uma versão simplificada e publicável para o Mestre?
