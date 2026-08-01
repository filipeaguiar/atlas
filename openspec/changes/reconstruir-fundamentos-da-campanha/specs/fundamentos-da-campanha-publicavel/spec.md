## ADDED Requirements

### Requirement: Premissa e tom orientam o Mestre
O capítulo de premissa e tom MUST apresentar a campanha como formação de jovens Extraordinários, atuação responsável em Belamar e confronto progressivo com o legado da Vanguarda, declarando quando o conteúdo contém segredos do Mestre.

#### Scenario: Mestre conhece o contrato da campanha
- **WHEN** o Mestre lê a premissa
- **THEN** compreende o papel do Atlas, da nova geração, das consequências e do mistério sem receber um roteiro de decisões obrigatórias

#### Scenario: Leitor jogador encontra limite de informação
- **WHEN** um trecho aborda Tomás, Vestígios ou Retorno
- **THEN** o capítulo identifica que a seção pertence ao Mestre e não é informação inicial dos personagens

### Requirement: Estrutura narrativa preserva agência
O capítulo de estrutura narrativa MUST preparar situações, objetivos, pressões, pistas redundantes e consequências, e MUST NOT exigir uma sequência única de ações dos personagens.

#### Scenario: Solução inesperada
- **WHEN** os personagens resolvem uma pressão por abordagem coerente não prevista
- **THEN** a estrutura permite incorporar o resultado sem invalidar o Marco ou a função da aventura

#### Scenario: Informação indispensável
- **WHEN** uma revelação é necessária para a continuidade da campanha
- **THEN** o capítulo exige múltiplas rotas de acesso e não a condiciona a uma única rolagem

### Requirement: Mapa de arcos fixa progressão sem fixar desfechos
O mapa geral MUST organizar 23 aventuras em seis no Arco I, dez no Arco II e sete no Arco III, com progressão aproximada e Marcos de responsabilidade, sem tornar resultados físicos contingentes em fatos inevitáveis.

#### Scenario: Transição entre arcos
- **WHEN** a campanha conclui um arco
- **THEN** a mudança é expressa por responsabilidade, autonomia, informação e relações, além de pontuação

#### Scenario: Ritmo de progressão
- **WHEN** o Mestre consulta a progressão esperada
- **THEN** encontra 10 pontos no início, cerca de 16 ao fim do Arco I, 26–27 ao fim do Arco II e cerca de 35 ao fim do Arco III, todos em escala Ningen salvo efeito temporário estabelecido

### Requirement: Arco I conduz à licença provisória
O capítulo do Arco I MUST estruturar candidatura, ingresso, formação e avaliação para licença provisória, mantendo professores e veteranos como apoio sem retirar o protagonismo dos personagens.

#### Scenario: Formação no Atlas
- **WHEN** o Mestre prepara as seis primeiras aventuras
- **THEN** encontra oportunidades de controle, cooperação, investigação, resgate e julgamento que podem ser enfrentadas por abordagens diferentes

#### Scenario: Marco da licença provisória
- **WHEN** o Arco I termina
- **THEN** os personagens passam de candidatos em formação a equipe autorizada a receber Chamados sob supervisão remota

### Requirement: Arco II combina Chamados e investigação crescente
O capítulo do Arco II MUST apresentar variedade de ocorrências em Belamar, crescimento gradual do mistério e conquista da licença definitiva, sem fazer cada Chamado depender do Retorno.

#### Scenario: Variedade antes do padrão
- **WHEN** o Mestre organiza o início do Arco II
- **THEN** somente parte dos Chamados contém sinais do Retorno e os demais continuam relevantes para cidade, relações e formação

#### Scenario: Segunda operação de captura
- **WHEN** a campanha chega à Aventura 14
- **THEN** ocorre a segunda operação de captura, seu resultado físico permanece condicionado às ações dos personagens, a Aventura 15 trata das consequências e a 16 conclui o arco

### Requirement: Arco III converge sem predeterminar a vitória
O capítulo do Arco III MUST organizar revelações, pressão sobre a Vanguarda, identidade de Multiplex, ameaça do Clarão artificial e confronto final como problemas investigáveis, preservando escolhas e contrajogo.

#### Scenario: Revelação de Tomás
- **WHEN** os personagens investigam a identidade de Multiplex
- **THEN** a campanha oferece evidências e relações que permitem concluir que ele é Tomás, em vez de depender apenas de exposição por um NPC

#### Scenario: Estado crítico do Clarão artificial
- **WHEN** o processo alcança estado crítico no clímax
- **THEN** qualquer escala Sugoi do antagonista é temporária, possui fonte investigável e pode ser enfrentada por objetivos além da redução de PV

### Requirement: Pacotes permanecem alternativas de preparação
Os fundamentos da campanha MUST distinguir núcleo estrutural de escolhas dos doze Pacotes e MUST NOT selecionar antagonista, Tenente Principal, mecanismo, Frentes, pistas ou vínculos por padrão.

#### Scenario: Mestre ainda não escolheu Pacote
- **WHEN** o Mestre lê os fundamentos antes de selecionar um overlay
- **THEN** compreende os arcos e Marcos sem encontrar uma opção apresentada como cânone universal

#### Scenario: Exemplo variável
- **WHEN** o texto exemplifica tecnologia, símbolo, ressonância, procedimento ou outro sinal
- **THEN** apresenta o elemento como possibilidade dependente do Pacote ou da preparação

### Requirement: Capítulos estruturais ficam prontos para publicação
Os seis capítulos MUST possuir metadados de reescrita aprovada, proveniência, referências cruzadas válidas, tom apropriado e conteúdo completo para o Mestre.

#### Scenario: Ativação no manifesto
- **WHEN** um dos seis capítulos é publicado
- **THEN** seu inventário registra `reescrito-aprovado`, seu front matter declara a camada do Mestre e nenhuma nota de pipeline aparece no corpo

#### Scenario: Materialização completa
- **WHEN** os seis capítulos são aprovados
- **THEN** a publicação materializa 18 documentos ativos sem copiar fontes internas, marcadores ou stubs
