## ADDED Requirements

### Requirement: Proveniência por afirmação
Toda afirmação factual introduzida nos capítulos reescritos MUST estar autorizada por uma matriz interna que indique fonte integral, classificação e capítulos permitidos.

#### Scenario: Fato com fonte aprovada
- **WHEN** uma afirmação deriva da introdução canônica ou das regras integrais
- **THEN** a matriz registra caminho, seção, formulação permitida e capítulos que podem utilizá-la

#### Scenario: Informação encontrada apenas em desenvolvimento
- **WHEN** um detalhe aparece somente em `desenvolvimento/`, inventário, relatório ou memória de agente
- **THEN** ele não é publicado como fato nesta mudança

### Requirement: Limites abertos funcionam como restrições
Questões abertas MUST ser registradas na matriz como limites negativos e MUST NOT receber resposta implícita nos capítulos.

#### Scenario: Origem do Clarão
- **WHEN** um capítulo menciona o Clarão
- **THEN** não define sua causa, natureza verdadeira ou relação universal com poderes

#### Scenario: AHI e legislação mundial
- **WHEN** sociedade heroica ou licenças são explicadas
- **THEN** o texto não inventa estrutura, jurisdição ou normas globais ainda abertas

### Requirement: Reescrita declarada honestamente
Um marcador substituído por texto novo MUST declarar `origem: reescrita-aprovada` e MUST NOT ser registrado como conteúdo integral recuperado.

#### Scenario: Capítulo reescrito aprovado
- **WHEN** o texto passa por todas as validações editoriais
- **THEN** seu status muda para `canon`, sua publicabilidade torna-se verdadeira e o inventário registra `reescrito-aprovado`

#### Scenario: Texto ainda incompleto
- **WHEN** um capítulo não atende aos requisitos ou possui afirmação sem proveniência
- **THEN** o marcador permanece não publicável e não é ativado no manifesto

### Requirement: Segredos protegidos por camada
A reescrita de cenário público MUST NOT incluir fatos reservados à campanha, ao Pacote de Antagonista ou ao conhecimento exclusivo do Mestre.

#### Scenario: Identidade de Tomás
- **WHEN** Vanguarda, Multiplex ou a Tragédia aparecem em capítulo público
- **THEN** o texto não revela que Tomás Valença é Multiplex

#### Scenario: Vestígios e Retorno
- **WHEN** sobreviventes da Vanguarda são descritos
- **THEN** o texto não menciona Vestígios, sexto Vestígio, sequestros planejados ou sobrevivência do antagonista

### Requirement: Elaboração sem novo fato estrutural
A reescrita MAY melhorar organização, explicação e aplicação em mesa, mas MUST NOT criar novos nomes próprios, números, datas, instituições, relações ou eventos sem aprovação explícita adicional.

#### Scenario: Exemplo de jogo sem fonte factual
- **WHEN** o texto precisa ilustrar uma possibilidade de uso
- **THEN** formula o exemplo como opção para a mesa, não como acontecimento estabelecido do cenário

#### Scenario: Novo fato necessário
- **WHEN** a escrita depende de detalhe não autorizado pela matriz
- **THEN** a execução pausa e propõe atualização dos artefatos antes de incorporar o detalhe

### Requirement: Transição auditável do inventário
A substituição dos nove marcadores MUST atualizar inventário, contagens e manifesto atomicamente, preservando o histórico de que o original não foi recuperado.

#### Scenario: Nove capítulos aprovados
- **WHEN** todos os capítulos são ativados
- **THEN** o inventário registra nove estados `reescrito-aprovado`, a contagem pendente passa de 94 para 85 e o manifesto contém 12 documentos ativos

#### Scenario: Apenas parte aprovada
- **WHEN** algum capítulo falha na revisão
- **THEN** somente capítulos individualmente aprovados podem mudar de estado, e contagens e manifesto refletem exatamente o resultado físico

### Requirement: Descoberta posterior do original
Se uma fonte integral original for encontrada durante a reescrita, o processo MUST pausar para escolher explicitamente entre recuperação, comparação ou manutenção da reescrita.

#### Scenario: Original localizado
- **WHEN** surge um arquivo que pode ser a versão integral do marcador
- **THEN** ele é preservado para auditoria e não é mesclado silenciosamente ao texto novo
