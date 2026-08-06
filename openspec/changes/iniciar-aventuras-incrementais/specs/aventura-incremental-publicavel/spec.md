## ADDED Requirements

### Requirement: Estrutura narrativa do capítulo
Cada aventura SHALL apresentar, nesta ordem: título; resumo diretamente abaixo do título, sem subtítulo “Resumo para o Mestre” e com bloco para leitura em voz alta; seção `A história até aqui`; cenas nomeadas; e material final de consulta com desafios ou oponentes pertinentes, experiência e encerramento. Função estrutural, proveniência e estado editorial SHALL permanecer nos metadados ou no planejamento, sem seções expositivas no capítulo.

#### Scenario: Documento incompleto
- **WHEN** uma aventura candidata omite uma parte obrigatória ou insere seções de planejamento entre `A história até aqui` e as cenas
- **THEN** a verificação editorial impede sua aprovação para publicação

#### Scenario: Resumo inicial
- **WHEN** o leitor abre o capítulo
- **THEN** encontra após o título uma síntese da aventura e um texto para apresentar aos jogadores antes de `A história até aqui`

### Requirement: Sequência pronta e agência dos jogadores
A aventura SHALL fornecer uma sequência principal, elenco, obstáculos, parâmetros mecânicos e transições definidos, reduzindo decisões de preparação do Mestre. Alternativas entre cenas MUST declarar gatilho, conteúdo, consequência e ponto de retorno ou avanço. A sequência MUST NOT exigir uma solução específica dentro de cada cena nem a derrota de todos os desafios por um único método.

#### Scenario: Mestre prepara o capítulo
- **WHEN** o Mestre lê a aventura
- **THEN** ele encontra a sequência, os NPCs, os desafios, as metas e as consequências já selecionados, sem precisar montar a sessão a partir de opções

#### Scenario: Grupo encontra abordagem inesperada
- **WHEN** os personagens superam um desafio por cooperação, negociação, capacidade apropriada ou uso criativo do ambiente
- **THEN** a aventura reconhece o resultado e segue para a transição preparada sem invalidar a solução

#### Scenario: Alternativa entre cenas
- **WHEN** uma decisão ou resultado abre um ramo diferente da sequência principal
- **THEN** o capítulo informa o gatilho, a cena alternativa completa, sua consequência e onde a sequência continua

### Requirement: Informação indispensável redundante
Cada conclusão indispensável SHALL possuir pelo menos três caminhos de descoberta, e uma única falha de teste MUST NOT bloquear a continuidade da aventura ou da campanha.

#### Scenario: Falha em uma investigação
- **WHEN** o grupo falha em um caminho de obtenção de informação essencial
- **THEN** permanecem outros caminhos acessíveis, com custo, atraso ou complicação coerente em vez de bloqueio

### Requirement: Uso das regras de 3DeT Victory
A aventura SHALL aplicar de forma verificável Ganho, Perda, Ajuda, Pontos de Ação, Objetivos, XP e Marcos quando pertinentes, distinguindo regra publicada de procedimento específico da campanha.

#### Scenario: Objetivo além do combate
- **WHEN** derrotar um adversário não resolve a prioridade da ocorrência
- **THEN** a aventura identifica um Objetivo Maior ligado à proteção, estabilização, investigação ou outra necessidade concreta

### Requirement: Descrição evocativa integrada à narrativa
O resumo e cada cena principal SHALL incluir um bloco breve de texto evocativo que possa ser lido em voz alta sem revelar informação reservada. NPCs, localidades, acontecimentos, desafios e oponentes SHALL ser descritos na cena em que aparecem, em vez de depender de capítulos intermediários de preparação. NPCs recorrentes SHALL possuir sinais visuais, postura e orientação de interpretação suficientes para serem reconhecidos em cena.

#### Scenario: Mestre inicia uma cena
- **WHEN** o Mestre chega a uma nova cena principal
- **THEN** encontra no próprio fluxo da cena espaço, elementos interativos, NPCs presentes, acontecimentos e mecânicas pertinentes, além de um bloco “Leia em voz alta”

#### Scenario: NPC recorrente reaparece
- **WHEN** um professor ou estudante já apresentado volta à cena
- **THEN** o Mestre dispõe de sinais reconhecíveis de aparência, voz ou comportamento para interpretá-lo consistentemente

### Requirement: Protagonismo dos personagens
Professores, veteranos e a Central SHALL oferecer contexto, recursos ou apoio sem resolver a decisão central no lugar dos personagens.

#### Scenario: Adulto poderoso presente
- **WHEN** um professor ou veterano participa da ocorrência
- **THEN** ele assume apoio ou outra frente enquanto uma prioridade decisiva permanece sob responsabilidade dos personagens

### Requirement: Estados e consequências persistentes
A aventura SHALL descrever múltiplos estados possíveis de encerramento e consequências concretas para pessoas, lugares, provas, relações e responsabilidades.

#### Scenario: Êxito parcial
- **WHEN** o grupo cumpre o Objetivo Maior mas perde uma prova ou permite uma retirada
- **THEN** a aventura preserva o êxito e registra a perda como consequência, sem converter o resultado em fracasso total

### Requirement: Separação entre núcleo e Pacote
Elementos dependentes do Pacote de Antagonista MUST ser marcados como variáveis e MUST NOT receber identidade, motivação, sinal ou contrajogo padrão antes da escolha aprovada.

#### Scenario: Aventura neutra quanto ao Pacote
- **WHEN** uma aventura funciona sem ligação necessária ao Retorno
- **THEN** ela permanece completa e jogável sem introduzir uma pista obrigatória do Pacote

### Requirement: Exame de Admissão como piloto
A primeira aventura SHALL apresentar o Instituto Atlas, permitir formação da equipe e avaliar controle, cooperação, resgate e julgamento sem depender do antagonista principal.

#### Scenario: Conclusão do exame
- **WHEN** a Aventura 1 termina
- **THEN** os personagens possuem consequências individualizadas e uma transição jogável para sua entrada no Atlas, sem receber ainda a licença provisória do fim do arco

### Requirement: Gate explícito de aprovação
Uma aventura nova SHALL permanecer não publicável durante a redação e revisão, e somente SHALL receber estado canônico, `publicar: true` e entrada no manifesto após aprovação explícita.

#### Scenario: Primeiro rascunho concluído
- **WHEN** o texto do Exame de Admissão está completo mas ainda não foi aprovado pelo usuário
- **THEN** ele permanece fora do manifesto e do PDF

#### Scenario: Aprovação do piloto
- **WHEN** o usuário aprova explicitamente o texto revisado
- **THEN** a proveniência e os metadados são finalizados, a aventura entra na posição ordenada do manifesto e uma nova versão incremental do PDF pode ser gerada

### Requirement: Proveniência e recuperação controlada
Conteúdo consultado no backup SHALL ser tratado individualmente, e o projeto MUST distinguir transcrição recuperada, adaptação e texto novo.

#### Scenario: Stub ou recuperação pendente encontrado
- **WHEN** uma fonte candidata possui estado `recuperacao-pendente` ou é apenas um stub
- **THEN** ela não é citada como texto existente nem copiada automaticamente para a aventura

### Requirement: Encerramento afirmativo e consultável
O material final SHALL informar fichas pertinentes, XP efetivamente disponível, consequências e procedimento de encerramento em linguagem afirmativa. Ele MUST NOT listar elementos ausentes nem declarar recompensas que a aventura não concede.

#### Scenario: Aventura sem oponente ou Marco
- **WHEN** uma categoria não se aplica ao capítulo
- **THEN** ela é omitida do material final, sem frases negativas sobre sua ausência

### Requirement: Adequação de tom
A aventura SHALL manter tom apropriado para crianças e pré-adolescentes, sem crueldade gráfica, preservando risco, consequência e responsabilidade heroica.

#### Scenario: Personagens em perigo
- **WHEN** uma pressão ameaça NPCs ou personagens
- **THEN** a descrição comunica urgência e consequência sem detalhamento gráfico inadequado
