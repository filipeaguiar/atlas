---
titulo: "Plano de implementação da publicação final"
tipo: planejamento-interno
status: ativo
publicar: false
produto: "Instituto Atlas e a Tragédia de Belamar"
---

# Plano de implementação da publicação final

> **Estado desta implementação — 31/07/2026:** `PUB-001`, `PUB-002` e `CONT-001` a `CONT-003` foram concluídas neste pacote. Para incorporá-las ao projeto, copie a árvore para a pasta principal, preservando os caminhos relativos.


Este arquivo é um instrumento interno de produção. Ele não deve ser incluído no `SUMMARY.md` da publicação, materializado como capítulo nem aparecer no PDF final.

## Objetivo de conclusão

Entregar uma publicação completa e jogável contendo:

- introdução;
- cenário;
- campanha;
- 23 aventuras completas;
- regras e fichas;
- instrumentos de consulta;
- mapas, handouts e ilustrações;
- créditos, licença e expediente;
- PDF final validado.

## Princípios de execução

- As fontes canônicas continuam em `cenario/`, `campanha/`, `regras/` e `apendices/`.
- `build/` nunca é editado manualmente.
- Os arquivos internos de planejamento e continuidade devem ficar fora da árvore materializada para publicação.
- Cada aventura depende do estado consolidado ao término da aventura anterior.
- O texto publicado contém apenas material útil ao leitor ou ao Mestre. Processos de geração, checklists editoriais, justificativas de design e arquivos de estado permanecem internos.
- Marcos definem mudanças de estado, não resultados obrigatórios de cenas.
- Aventuras devem preparar situações, aceitar consequências e preservar a agência dos jogadores.
- O Pacote de Antagonista escolhido funciona como overlay. Não misturar Pacotes diferentes sem decisão editorial explícita.

---

# Convenções do backlog

- `[ ]` não iniciado
- `[-]` em andamento
- `[x]` concluído
- `BLOQUEADA POR:` dependência que precisa ser concluída antes
- `ENTREGA:` arquivo, ativo ou resultado verificável
- `ACEITE:` condição mínima para considerar a tarefa concluída

---

# Fase 0 — Governança e preparação do projeto

## PUB-001 — Registrar este backlog no projeto

- [x] Criar `desenvolvimento/planejamento/publicacao-final.md`.
- [x] Copiar este plano para o arquivo.
- [x] Confirmar que ele não aparece no `publicacao/conteudo/SUMMARY.md`.
- [x] Confirmar que `materialize_publication.py` não o copia para a camada pública.
- [x] Adicionar um link para ele no índice interno de desenvolvimento, caso exista.

**ENTREGA:** backlog interno preparado no caminho canônico.  
**ACEITE:** arquivo com `publicar: false`, fora do sumário público e da lista explícita de materialização.  
**EVIDÊNCIA:** `desenvolvimento/planejamento/publicacao-final.md` neste pacote; o relatório público atual registra zero documentos não publicáveis copiados.

## PUB-002 — Auditar o estado atual das fontes canônicas

- [x] Listar capítulos existentes em `cenario/`, `campanha/`, `regras/` e `apendices/`.
- [x] Identificar duplicações entre fontes atuais, arquivos históricos e conteúdo materializado.
- [x] Confirmar a versão canônica de cada conceito.
- [x] Marcar arquivos históricos como somente leitura.
- [x] Produzir uma tabela `documento → estado → pendência → dependências`.
- [x] Comparar os capítulos canônicos com a release mais recente.
- [x] Registrar quais capítulos ainda não entram no manifesto de publicação.

**ENTREGA:** `desenvolvimento/planejamento/auditoria-de-conteudo.md`.  
**ACEITE:** fontes, derivados, históricos, lacunas e conflitos de versão estão classificados.  
**EVIDÊNCIA:** auditoria incluída neste pacote.

## PUB-003 — Revisar questões em aberto

- [ ] Ler `apendices/questoes-em-aberto.md`.
- [ ] Remover questões já respondidas nas fontes atuais.
- [ ] Separar questões que exigem decisão antes das aventuras.
- [ ] Separar opções que devem continuar abertas para cada Mestre.
- [ ] Vincular cada decisão pendente a uma tarefa deste backlog.
- [ ] Não converter uma questão em cânone sem aprovação explícita.

**ENTREGA:** arquivo de questões em aberto atualizado.  
**ACEITE:** nenhuma questão obsoleta permanece marcada como pendente.

## PUB-004 — Definir critérios globais de pronto

- [ ] Definir critérios editoriais para capítulos.
- [ ] Definir critérios mecânicos para fichas e encontros.
- [ ] Definir critérios de continuidade para aventuras.
- [ ] Definir critérios visuais para imagens e mapas.
- [ ] Definir critérios técnicos para PDF.
- [ ] Registrar a regra de que termos internos não podem aparecer na publicação.
- [ ] Registrar a lista de comandos de validação obrigatórios.

**ENTREGA:** `desenvolvimento/planejamento/definition-of-done.md`.  
**ACEITE:** todas as tarefas posteriores podem apontar para critérios objetivos.

---

# Fase 1 — Sistema interno de continuidade da campanha

Esta fase deve ser concluída antes da escrita sequencial das aventuras.

## CONT-001 — Criar a estrutura interna de continuidade

- [x] Criar `desenvolvimento/continuidade/`.
- [x] Criar `desenvolvimento/continuidade/README.md`.
- [x] Criar `desenvolvimento/continuidade/estado-inicial.yml`.
- [x] Criar `desenvolvimento/continuidade/transicoes/`.
- [x] Criar `desenvolvimento/continuidade/snapshots/`.
- [x] Criar `desenvolvimento/continuidade/briefings/`.
- [x] Garantir que essa árvore não seja materializada para publicação.

**ENTREGA:** estrutura interna de arquivos.  
**ACEITE:** existe um local único para estado, transições e contexto de cada aventura.  
**EVIDÊNCIA:** diretórios `transicoes/`, `snapshots/` e `briefings/` criados no pacote.

## CONT-002 — Definir o esquema do estado da campanha

O estado precisa registrar apenas fatos úteis para manter continuidade editorial.

- [x] Definir identificação da aventura e do arco.
- [x] Definir estado institucional dos personagens: candidato, aluno, licença provisória ou licença definitiva.
- [x] Definir faixa de pontuação esperada.
- [x] Definir estado de cada NPC recorrente:
  - [x] vivo, morto, desaparecido, sequestrado, ferido ou indisponível;
  - [x] localização conhecida;
  - [x] função atual;
  - [x] relação com os personagens;
  - [x] confiança, suspeita ou conflito relevante;
  - [x] fatos que conhece;
  - [x] fatos que acredita incorretamente;
  - [x] descobertas recentes;
  - [x] última aparição;
  - [x] disponibilidade para a aventura seguinte.
- [x] Definir estado da Vanguarda e de cada sequestro.
- [x] Definir estado de Tomás e do segredo Multiplex.
- [x] Definir estado do Tenente Principal.
- [x] Definir presença e atividade do grande antagonista.
- [x] Definir progresso das Frentes do Pacote selecionado.
- [x] Definir pistas:
  - [x] conteúdo;
  - [x] fonte;
  - [x] quem conhece;
  - [x] se os personagens tiveram acesso;
  - [x] redundâncias existentes;
  - [x] interpretação provável;
  - [x] payoff previsto.
- [x] Definir estado de locais, objetos, Vestígios e recursos.
- [x] Definir consequências públicas e institucionais.
- [x] Definir promessas narrativas ainda sem payoff.
- [x] Definir ganchos abertos.
- [x] Definir âncoras pessoais dos PCs quando eles existirem.
- [x] Definir decisões ainda não canonizadas separadamente.

**ENTREGA:** `desenvolvimento/continuidade/schema.yml` e documentação no README.  
**ACEITE:** mortes, sequestros, descobertas e mudanças de relação podem ser representados por campos e enumerações estáveis.  
**EVIDÊNCIA:** esquema YAML validado sintaticamente.

## CONT-003 — Consolidar o estado inicial da campanha

- [x] Ler as fontes canônicas de cenário e campanha.
- [x] Registrar o estado dos candidatos antes da Aventura 1.
- [x] Registrar todos os NPCs recorrentes disponíveis no início.
- [x] Registrar o que cada professor e membro da Vanguarda sabe.
- [x] Registrar o estado público da Tragédia de Belamar.
- [x] Registrar os segredos reais separadamente do conhecimento dos NPCs.
- [x] Registrar o Pacote selecionado como variável ainda não preenchida, quando necessário.
- [x] Registrar o Tenente Principal como variável ainda não preenchida, quando necessário.
- [x] Validar o estado contra `apendices/questoes-em-aberto.md`.

**ENTREGA:** `desenvolvimento/continuidade/estado-inicial.yml`.  
**ACEITE:** candidatos, Instituto, NPCs recorrentes, Vanguarda, conhecimento público, segredos fixos e variáveis ainda abertas estão registrados.  
**EVIDÊNCIA:** estado inicial validado contra o esquema documental e contra as questões em aberto identificadas na auditoria.

## CONT-004 — Criar o modelo de transição de aventura

Cada aventura deve produzir um arquivo interno `transicoes/NN.yml`.

- [ ] Incluir o snapshot de entrada utilizado.
- [ ] Incluir fatos novos introduzidos pela aventura.
- [ ] Incluir mudanças obrigatórias do marco estrutural.
- [ ] Incluir resultados condicionais.
- [ ] Incluir consequências de sucesso parcial, falha e retirada.
- [ ] Incluir mudanças de conhecimento por NPC.
- [ ] Incluir mudanças de estado físico ou disponibilidade.
- [ ] Incluir mudanças de relação.
- [ ] Incluir pistas consumidas, reforçadas ou ainda ausentes.
- [ ] Incluir ganchos encerrados e novos ganchos.
- [ ] Incluir promessas criadas e payoffs realizados.
- [ ] Incluir recursos adquiridos, perdidos ou danificados.
- [ ] Incluir o estado mínimo necessário para a aventura seguinte.
- [ ] Incluir alertas de continuidade para o próximo autor.

**ENTREGA:** `desenvolvimento/continuidade/modelo-transicao.yml`.  
**ACEITE:** o arquivo consegue representar “NPC descobriu X”, “NPC foi sequestrado” e “NPC morreu” sem alterar retroativamente a aventura anterior.

## CONT-005 — Criar o modelo de briefing para a aventura seguinte

- [ ] Gerar um resumo curto do estado vigente.
- [ ] Listar NPCs disponíveis e indisponíveis.
- [ ] Listar o que cada NPC importante sabe.
- [ ] Listar fatos que não podem ser contraditos.
- [ ] Listar consequências que precisam aparecer ou ser reconhecidas.
- [ ] Listar pistas que precisam de reforço.
- [ ] Listar promessas que se aproximam de payoff.
- [ ] Listar decisões ainda abertas.
- [ ] Listar requisitos do marco estrutural da próxima aventura.
- [ ] Listar conteúdo do Pacote selecionado aplicável à próxima aventura.
- [ ] Listar âncoras de PCs ainda não utilizadas.

**ENTREGA:** `desenvolvimento/continuidade/modelo-briefing.md`.  
**ACEITE:** um agente que leia o briefing e as fontes obrigatórias consegue iniciar a aventura seguinte sem perder o estado anterior.

## CONT-006 — Automatizar snapshots e briefings

- [ ] Criar `tools/build_campaign_state.py`.
- [ ] Ler `estado-inicial.yml`.
- [ ] Aplicar transições em ordem numérica.
- [ ] Gerar `snapshots/NN-entrada.yml`.
- [ ] Gerar `snapshots/NN-saida.yml`.
- [ ] Gerar `briefings/NN-proxima-aventura.md`.
- [ ] Detectar referências a NPCs inexistentes.
- [ ] Detectar transições fora de ordem.
- [ ] Detectar estados impossíveis, como morto e disponível ao mesmo tempo.
- [ ] Detectar conhecimento adquirido antes da pista correspondente.
- [ ] Detectar sequestro repetido sem libertação ou explicação.
- [ ] Permitir campos condicionais sem escolher pelo grupo.
- [ ] Produzir relatório de inconsistências.

**ENTREGA:** script e testes.  
**ACEITE:** o estado de entrada da Aventura N+1 é reproduzível a partir do estado inicial e das transições 1…N.

## CONT-007 — Criar verificador de separação editorial

- [ ] Criar teste que procure caminhos de `desenvolvimento/continuidade/` no material publicado.
- [ ] Procurar termos como “snapshot”, “pipeline”, “estado interno”, “prompt”, “agente” e “handoff” nos capítulos públicos.
- [ ] Permitir termos legítimos em contexto ficcional apenas quando revisados.
- [ ] Integrar a verificação ao build.
- [ ] Falhar a build quando material interno for incluído.

**ENTREGA:** `tools/check_internal_content.py`.  
**ACEITE:** regras e raciocínio de produção não podem vazar para o PDF.

---

# Fase 2 — Planejamento macro das 23 aventuras

## ADV-PLAN-001 — Criar o plano geral interno das aventuras

- [ ] Criar `desenvolvimento/aventuras/plano-geral.md`.
- [ ] Registrar as 23 posições da campanha.
- [ ] Registrar o arco de cada aventura:
  - [ ] Aventuras 1–6: Arco I;
  - [ ] Aventuras 7–16: Arco II;
  - [ ] Aventuras 17–23: Arco III.
- [ ] Registrar o estado inicial e final esperado de cada aventura.
- [ ] Registrar o tipo primário e secundário de cada aventura.
- [ ] Registrar quais relações devem avançar.
- [ ] Registrar quais locais de Belamar serão apresentados.
- [ ] Registrar distribuição de professores e alunos recorrentes.
- [ ] Registrar aparições do Tenente Principal.
- [ ] Registrar aparições dos demais tenentes.
- [ ] Registrar atividade indireta do grande antagonista.
- [ ] Registrar distribuição de pistas com redundância.
- [ ] Registrar oportunidades de contrajogo.
- [ ] Registrar progressão de XP e Marcos.
- [ ] Registrar oportunidades para âncoras pessoais de PCs.
- [ ] Não criar títulos ou premissas definitivas para posições ainda não aprovadas.

**ENTREGA:** plano macro interno.  
**ACEITE:** não existem duas aventuras consecutivas com a mesma função, oposição e procedimento central sem intenção explícita.

## ADV-PLAN-002 — Resolver marcos ainda sem posição exata

- [x] Fixar a segunda operação de captura na Aventura 14, conforme DEC-001.
- [ ] Definir quando a Licença Definitiva é concedida dentro do encerramento do Arco II.
- [ ] Definir quando cada Frente do antagonista avança.
- [ ] Definir onde entram pelo menos duas formas investigáveis de interferir no mecanismo final.
- [ ] Definir onde a função prática dos Vestígios começa a ser compreendida.
- [ ] Definir onde o Vestígio de Solar é preparado.
- [ ] Definir onde cada inconsistência histórica pode ser descoberta.
- [ ] Definir como falhas anteriores alteram, mas não bloqueiam, os marcos.
- [ ] Atualizar as fontes canônicas quando decisões forem aprovadas.

**ENTREGA:** marcos aprovados e vinculados às aventuras.  
**ACEITE:** o Arco III não depende de informação ou recurso introduzido apenas no final.

## ADV-PLAN-003 — Criar matriz de continuidade de NPCs

- [ ] Listar todos os NPCs recorrentes.
- [ ] Definir função narrativa de cada um ao longo dos três arcos.
- [ ] Marcar aparições mínimas necessárias.
- [ ] Marcar descobertas que cada NPC pode realizar.
- [ ] Marcar riscos de morte, ferimento, desaparecimento ou sequestro.
- [ ] Marcar relações que devem evoluir.
- [ ] Marcar quem pode substituir funções operacionais de NPCs indisponíveis.
- [ ] Evitar que um NPC desapareça da campanha sem explicação.
- [ ] Vincular cada mudança ao arquivo de transição correspondente.

**ENTREGA:** `desenvolvimento/aventuras/matriz-npcs.md`.  
**ACEITE:** todo NPC recorrente possui trajetória ou função identificável.

## ADV-PLAN-004 — Criar matriz de pistas e payoffs por aventura

- [ ] Importar a matriz de pistas existente.
- [ ] Atribuir fontes diferentes às pistas estruturais.
- [ ] Garantir redundância para verdades indispensáveis.
- [ ] Separar o que os PCs podem descobrir do que NPCs podem descobrir.
- [ ] Registrar pistas falsas apenas quando houver forma justa de corrigi-las.
- [ ] Registrar o payoff previsto de cada pista.
- [ ] Identificar pistas específicas de cada Pacote.
- [ ] Não misturar pistas incompatíveis entre Pacotes.
- [ ] Validar que a revelação de Multiplex pode ser concluída pelos jogadores.
- [ ] Validar que o confronto final possui contrajogos previamente investigáveis.

**ENTREGA:** matriz de pistas revisada.  
**ACEITE:** nenhuma verdade indispensável depende de uma única rolagem, cena ou NPC.

## ADV-PLAN-005 — Aprovar o template público de aventura

O template público pode conter apenas conteúdo útil para condução.

- [ ] Título e posição na campanha.
- [ ] Visão geral para o Mestre.
- [ ] Estado inicial relevante.
- [ ] Elenco e motivações.
- [ ] Locais.
- [ ] Dossiê ou situação inicial.
- [ ] Objetivo Maior e objetivos secundários.
- [ ] Pressões simultâneas.
- [ ] Complicação.
- [ ] Situações e cenas.
- [ ] Pistas.
- [ ] Reações da oposição.
- [ ] Consequências e adaptações.
- [ ] Encerramento e debriefing.
- [ ] Recompensas e progressão.
- [ ] Fichas, mapas e handouts.
- [ ] Ajustes pelo Pacote selecionado, quando necessários.
- [ ] Ajustes por tamanho e composição do grupo.

Não incluir:

- [ ] prompts;
- [ ] checklists de geração;
- [ ] arquivos de estado;
- [ ] justificativas de design;
- [ ] instruções para agentes;
- [ ] notas de pipeline;
- [ ] decisões internas ainda não aprovadas.

**ENTREGA:** template canônico para aventuras publicáveis.  
**ACEITE:** o template pode entrar diretamente no livro após preenchimento.

---

# Fase 3 — Produção das aventuras

## Fluxo obrigatório para cada aventura

Cada tarefa `ADV-NN` deve executar estes passos, além das exigências específicas:

1. [ ] Ler as diretrizes obrigatórias indicadas em `AGENTS.md`.
2. [ ] Ler o README do arco.
3. [ ] Ler o briefing de continuidade gerado para a aventura.
4. [ ] Ler apenas o Pacote de Antagonista selecionado.
5. [ ] Confirmar tipo primário, tipo secundário e mudança de estado.
6. [ ] Escrever primeiro a estrutura ficcional e as escolhas.
7. [ ] Adicionar mecânicas de 3DeT Victory.
8. [ ] Fazer passe de pistas, agência e falha com consequências.
9. [ ] Fazer passe de NPCs e continuidade.
10. [ ] Fazer passe de tom para jogadores jovens.
11. [ ] Criar ou solicitar mapas, handouts e fichas específicas.
12. [ ] Escrever a transição interna da aventura.
13. [ ] Gerar o snapshot e o briefing da próxima.
14. [ ] Revisar o texto público para remover conteúdo interno.
15. [ ] Marcar `publicar: true` somente após aprovação e validação.

---

## ADV-01 — Escrever a Aventura 1: Exame de Admissão

**BLOQUEADA POR:** CONT-001 a CONT-005, ADV-PLAN-001.

- [ ] Apresentar o Instituto Atlas, professores e candidatos recorrentes.
- [ ] Construir provas que avaliem mais que combate.
- [ ] Incluir a emergência real que rompe a lógica da simulação.
- [ ] Permitir que os candidatos escolham prioridades e formas de ajudar.
- [ ] Registrar primeiras impressões e relações dos NPCs.
- [ ] Registrar quem percebeu quais competências dos personagens.
- [ ] Definir consequências para desempenho forte, parcial ou problemático.
- [ ] Encerrar com aprovação, admissão condicionada ou solução equivalente que preserve a campanha.
- [ ] Atualizar o estado dos personagens de candidatos para alunos.
- [ ] Produzir a transição `01.yml` e o briefing da Aventura 2.

**ACEITE:** a aventura apresenta o idioma da campanha e produz um estado claro de entrada no Instituto.

## ADV-02 — Escrever a Aventura 2 do Arco I

**BLOQUEADA POR:** ADV-01 e snapshot de saída da Aventura 1.

- [ ] Aprovar a premissa no plano geral antes de redigir.
- [ ] Testar uma dimensão do heroísmo diferente da Aventura 1.
- [ ] Reconhecer consequências e relações criadas no Exame.
- [ ] Desenvolver ao menos um professor e um aluno recorrente.
- [ ] Introduzir ou aprofundar um espaço cotidiano do Atlas.
- [ ] Plantar no máximo pistas discretas da trama maior.
- [ ] Atualizar conhecimentos, relações e disponibilidade dos NPCs.
- [ ] Produzir a transição `02.yml` e o briefing da Aventura 3.

**ACEITE:** a aventura amplia a vida escolar sem repetir o Exame.

## ADV-03 — Escrever a Aventura 3 do Arco I

**BLOQUEADA POR:** ADV-02.

- [ ] Aprovar premissa, tipos e mudança de estado.
- [ ] Retomar ao menos uma consequência anterior.
- [ ] Apresentar um problema escolar ou atividade externa com escolhas reais.
- [ ] Avançar a formação da Equipe de Campo.
- [ ] Dar protagonismo a NPCs diferentes dos usados na Aventura 2.
- [ ] Registrar novas descobertas de NPCs e PCs.
- [ ] Produzir a transição `03.yml` e o briefing da Aventura 4.

**ACEITE:** o grupo começa a funcionar como equipe sem já estar plenamente formado.

## ADV-04 — Escrever a Aventura 4 do Arco I

**BLOQUEADA POR:** ADV-03.

- [ ] Aprovar premissa, tipos e mudança de estado.
- [ ] Criar uma provação qualitativamente diferente das anteriores.
- [ ] Colocar em tensão controle de poderes, ética ou proteção de terceiros.
- [ ] Fazer Tomás observar ou orientar sem resolver o problema.
- [ ] Desenvolver uma relação que terá valor no Arco II.
- [ ] Registrar mudanças de confiança, suspeita ou rivalidade.
- [ ] Produzir a transição `04.yml` e o briefing da Aventura 5.

**ACEITE:** a aventura prepara responsabilidade de campo, não apenas competência técnica.

## ADV-05 — Escrever a Aventura 5 do Arco I

**BLOQUEADA POR:** ADV-04.

- [ ] Aprovar premissa, tipos e mudança de estado.
- [ ] Retomar uma promessa ou falha das aventuras 2–4.
- [ ] Preparar a avaliação final da licença sem antecipar sua solução.
- [ ] Mostrar consequências institucionais das decisões do grupo.
- [ ] Reforçar a relação dos personagens com Tomás e com o Atlas.
- [ ] Atualizar quem acredita que a equipe está ou não preparada.
- [ ] Produzir a transição `05.yml` e o briefing da Aventura 6.

**ACEITE:** o clímax do arco parece consequência da formação anterior.

## ADV-06 — Escrever a Aventura 6: conclusão do Arco I

**BLOQUEADA POR:** ADV-05.

- [ ] Construir a avaliação decisiva para a licença provisória.
- [ ] Exigir controle, investigação, resgate, cooperação, julgamento e adaptação.
- [ ] Incluir acontecimento real ou complicação não simulada.
- [ ] Não depender de vitória em combate.
- [ ] Fazer relações e aprendizados anteriores alterarem opções.
- [ ] Definir consequências institucionais de falha parcial.
- [ ] Conceder a licença provisória de forma coerente com os resultados.
- [ ] Atualizar autonomia, responsabilidades e acesso a Chamados.
- [ ] Produzir a transição `06.yml` e o briefing da Aventura 7.
- [ ] Executar revisão completa do Arco I.

**ACEITE:** o estado final do arco é “heróis em treinamento autorizados a responder a Chamados”.

## ADV-07 — Escrever a Aventura 7: primeiro Chamado do Arco II

**BLOQUEADA POR:** ADV-06 e revisão do Arco I.

- [ ] Aprovar premissa e tipo de ocorrência.
- [ ] Apresentar o fluxo da Central e da supervisão remota.
- [ ] Mostrar diferença entre exercício e situação real.
- [ ] Dar aos personagens autonomia compatível com licença provisória.
- [ ] Introduzir um novo setor ou comunidade de Belamar.
- [ ] Incluir uma vitória clara possível.
- [ ] Plantar pista discreta sem dominar a aventura.
- [ ] Produzir a transição `07.yml` e o briefing da Aventura 8.

**ACEITE:** a aventura cumpre a promessa de atuação heroica real.

## ADV-08 — Escrever a Aventura 8 do Arco II

**BLOQUEADA POR:** ADV-07.

- [ ] Escolher tipo primário diferente da Aventura 7.
- [ ] Reconhecer consequência pública ou institucional do primeiro Chamado.
- [ ] Aprofundar um NPC recorrente.
- [ ] Introduzir nova pressão que não seja apenas oposição mais forte.
- [ ] Permitir solução por abordagens diferentes.
- [ ] Avançar uma Frente do Pacote sem revelar todo o metaplot.
- [ ] Produzir a transição `08.yml` e o briefing da Aventura 9.

**ACEITE:** a variedade de Chamados fica evidente.

## ADV-09 — Escrever a Aventura 9 do Arco II

**BLOQUEADA POR:** ADV-08.

- [ ] Escolher tipo primário diferente das aventuras 7 e 8.
- [ ] Integrar uma consequência de missão anterior.
- [ ] Dar espaço para uma âncora pessoal de PC ou reservar slot claramente.
- [ ] Mostrar reação de autoridades, imprensa, comunidade ou Instituto.
- [ ] Introduzir ou desenvolver um tenente sem exigir confronto definitivo.
- [ ] Atualizar o que o Tenente Principal sabe sobre a equipe.
- [ ] Produzir a transição `09.yml` e o briefing da Aventura 10.

**ACEITE:** o antagonismo começa a observar ou responder aos personagens.

## ADV-10 — Escrever a Aventura 10 do Arco II

**BLOQUEADA POR:** ADV-09.

- [ ] Fechar o primeiro movimento do Arco II.
- [ ] Entregar uma aventura de super-heróis completa, não apenas preparação de metaplot.
- [ ] Consolidar suspeitas dispersas sem tornar a resposta óbvia.
- [ ] Aprofundar a relação com Tomás.
- [ ] Preparar plausivelmente a oportunidade do primeiro sequestro.
- [ ] Registrar quais NPCs reconhecem um padrão.
- [ ] Produzir a transição `10.yml` e o briefing da Aventura 11.

**ACEITE:** o grupo viveu a profissão antes de a trama do Retorno assumir o primeiro plano.

## ADV-11 — Escrever a Aventura 11: primeiro sequestro da Vanguarda

**BLOQUEADA POR:** ADV-10.

- [ ] Definir qual membro ativo da Vanguarda é o primeiro alvo.
- [ ] Construir meios e oportunidade plausíveis para a ação inimiga.
- [ ] Não usar invulnerabilidade de roteiro.
- [ ] Permitir que os personagens salvem pessoas, preservem provas ou alterem custos mesmo se o sequestro ocorrer.
- [ ] Tornar investigável a seleção deliberada de alvos.
- [ ] Registrar quem testemunhou ou descobriu o quê.
- [ ] Atualizar o membro da Vanguarda para sequestrado ou registrar resultado alternativo previsto.
- [ ] Mudar a postura da campanha de resposta para investigação ativa.
- [ ] Produzir a transição `11.yml` e o briefing da Aventura 12.

**ACEITE:** o ponto médio transforma a ameaça abstrata em adversário ativo.

## ADV-12 — Escrever a Aventura 12 do Arco II

**BLOQUEADA POR:** ADV-11.

- [ ] Mostrar consequências concretas do primeiro sequestro.
- [ ] Permitir investigação iniciada pelos personagens.
- [ ] Manter um Chamado ou problema heroico real em primeiro plano.
- [ ] Mostrar reação do Instituto, da Vanguarda e da cidade.
- [ ] Fazer o Tenente Principal responder à interferência da equipe.
- [ ] Reforçar pistas por fontes diferentes.
- [ ] Produzir a transição `12.yml` e o briefing da Aventura 13.

**ACEITE:** a campanha preserva a premissa episódica enquanto a investigação ganha intenção.

## ADV-13 — Escrever a Aventura 13 do Arco II

**BLOQUEADA POR:** ADV-12.

- [ ] Aprovar função específica no plano geral.
- [ ] Integrar uma âncora pessoal de PC.
- [ ] Retomar ao menos uma relação construída no Arco I.
- [ ] Avançar uma Frente inimiga como reação a ações anteriores.
- [ ] Permitir descoberta relevante sem depender de uma única rolagem.
- [ ] Atualizar conhecimento individual dos NPCs.
- [ ] Produzir a transição `13.yml` e o briefing da Aventura 14.

**ACEITE:** o metaplot torna-se pessoal sem apagar a aventura presente.

## ADV-14 — Escrever a Aventura 14: segunda operação de captura

**BLOQUEADA POR:** ADV-13.

- [ ] Aprovar função específica no plano geral.
- [ ] Variar o tipo de ocorrência.
- [ ] Colocar consequência anterior no centro da situação.
- [ ] Desenvolver um tenente ou aliado ainda pouco utilizado.
- [ ] Oferecer contrajogo investigável ligado ao mecanismo do Pacote.
- [ ] Executar a segunda operação de captura na Aventura 14, conforme DEC-001.
- [ ] Tornar reconhecível que a Vanguarda está sendo escolhida deliberadamente.
- [ ] Preservar três saídas: captura impedida, captura com custos ao antagonista ou captura com vantagem ampla do antagonista.
- [ ] Registrar separadamente o estado dramático obrigatório e o resultado físico condicional da captura.
- [ ] Produzir a transição `14.yml` e o briefing da Aventura 15.

**ACEITE:** a escalada decorre de ação e reação, não apenas de ameaça maior.

## ADV-15 — Escrever a Aventura 15: consequências da segunda operação

**BLOQUEADA POR:** ADV-14.

- [ ] Aprovar função específica no plano geral.
- [ ] Reconhecer o resultado concreto da operação da Aventura 14.
- [ ] Mostrar consequências para Instituto, Vanguarda, cidade e investigação.
- [ ] Adaptar a aventura aos três estados de saída previstos na Aventura 14.
- [ ] Consolidar suspeitas sobre a Tragédia de Belamar.
- [ ] Mostrar custos da ausência dos membros da Vanguarda.
- [ ] Preparar a avaliação ou decisão institucional da licença definitiva.
- [ ] Produzir a transição `15.yml` e o briefing da Aventura 16.

**ACEITE:** a equipe demonstra iniciativa e não depende apenas de despachos da Central.

## ADV-16 — Escrever a Aventura 16: conclusão do Arco II

**BLOQUEADA POR:** ADV-15.

- [ ] Encerrar o arco institucional com a Licença Definitiva estudantil.
- [ ] Mostrar que a equipe conquistou autonomia.
- [ ] Tornar clara a ameaça maior em movimento sem revelar tudo prematuramente.
- [ ] Atualizar autoridade, responsabilidades e acesso operacional.
- [ ] Consolidar pistas e ganchos necessários ao Arco III.
- [ ] Garantir que o novo estado não dependa de um único resultado.
- [ ] Produzir a transição `16.yml` e o briefing da Aventura 17.
- [ ] Executar revisão completa do Arco II.

**ACEITE:** os personagens são heróis com autonomia justamente quando Belamar perde respostas seguras.

## ADV-17 — Escrever a Aventura 17: terceiro sequestro

**BLOQUEADA POR:** ADV-16 e revisão do Arco II.

- [ ] Tornar inequívoca a seleção deliberada da geração anterior.
- [ ] Construir meios e oportunidade plausíveis para o terceiro sequestro.
- [ ] Permitir alterações significativas de custo, provas, vítimas e recursos.
- [ ] Levar os personagens da correlação a uma hipótese investigável.
- [ ] Mostrar que a Vanguarda não resolverá o problema automaticamente.
- [ ] Atualizar estados dos membros capturados e disponíveis.
- [ ] Produzir a transição `17.yml` e o briefing da Aventura 18.

**ACEITE:** a pergunta “por que essas pessoas?” torna-se central e investigável.

## ADV-18 — Escrever a Aventura 18: quarto sequestro

**BLOQUEADA POR:** ADV-17.

- [ ] Construir o quarto sequestro sem anular decisões dos jogadores.
- [ ] Completar a remoção imediata dos quatro membros ativos da Vanguarda ou registrar variantes previstas.
- [ ] Mostrar a ausência da Vanguarda na vida de Belamar.
- [ ] Fazer surgir a necessidade de localizar o último sobrevivente conhecido.
- [ ] Consolidar informações sobre Multiplex sem revelar Tomás diretamente.
- [ ] Atualizar capacidade operacional do Instituto e da cidade.
- [ ] Produzir a transição `18.yml` e o briefing da Aventura 19.

**ACEITE:** a busca por Multiplex decorre de evidências e ausência, não de exposição arbitrária.

## ADV-19 — Escrever a Aventura 19: Onde Está Multiplex?

**BLOQUEADA POR:** ADV-18.

- [ ] Reunir pistas plantadas nos arcos anteriores.
- [ ] Transformar visitantes, hábitos, conhecimentos e registros em evidências.
- [ ] Permitir que os jogadores concluam que Tomás é Multiplex.
- [ ] Preparar caminhos alternativos caso algumas pistas tenham sido perdidas.
- [ ] Tratar a revelação como mudança emocional e operacional.
- [ ] Atualizar o conhecimento de cada NPC sobre a identidade de Tomás.
- [ ] Atualizar a relação entre professor e alunos.
- [ ] Produzir a transição `19.yml` e o briefing da Aventura 20.

**ACEITE:** a revelação é descoberta pelos jogadores e muda o estado da campanha.

## ADV-20 — Escrever a Aventura 20: confronto com o Tenente Principal

**BLOQUEADA POR:** ADV-19.

- [ ] Pagar a relação construída com o Tenente Principal.
- [ ] Preparar um encontro com objetivos além de reduzir PV.
- [ ] Preservar agência e motivação própria do tenente.
- [ ] Revelar o verdadeiro antagonista sem invalidar o arco do tenente.
- [ ] Reinterpretar operações anteriores com evidências verificáveis.
- [ ] Tornar compreensível a motivação geral do antagonista.
- [ ] Fornecer objetivo concreto para as três aventuras seguintes.
- [ ] Produzir a transição `20.yml` e o briefing da Aventura 21.

**ACEITE:** os personagens sabem o que estava sendo preparado e contra quem estão agindo.

## ADV-21 — Escrever a Aventura 21: preparar a resposta

**BLOQUEADA POR:** ADV-20.

- [ ] Dar tempo e agência para os personagens formularem um plano.
- [ ] Fazer aliados, relações e recursos conquistados importarem.
- [ ] Tornar suficientemente compreendida a função prática dos Vestígios.
- [ ] Disponibilizar pelo menos duas formas investigáveis de interferir no processo final.
- [ ] Preparar a localização ou forma do Vestígio de Solar.
- [ ] Confrontar a pergunta temática do antagonista antes do clímax.
- [ ] Fazer Tomás aceitar que precisa confiar nos personagens.
- [ ] Registrar preparações que alteram a Aventura 22 e o final.
- [ ] Produzir a transição `21.yml` e o briefing da Aventura 22.

**ACEITE:** a solução final é preparada por decisões dos personagens, não entregue posteriormente.

## ADV-22 — Escrever a Aventura 22: captura de Tomás e ponto de não retorno

**BLOQUEADA POR:** ADV-21.

- [ ] Usar o Pacote para explicar como o inimigo cria oportunidade plausível.
- [ ] Não usar captura inevitável sem contrajogo.
- [ ] Permitir que preparações anteriores alterem dificuldade, opções, recursos e danos.
- [ ] Permitir que os personagens preservem algo importante mesmo se Tomás for capturado.
- [ ] Colocar o novo Clarão artificial em movimento.
- [ ] Transferir o comando da resposta para os personagens.
- [ ] Consolidar acesso ao local final.
- [ ] Atualizar Tomás como capturado ou registrar variantes previstas.
- [ ] Produzir a transição `22.yml` e o briefing da Aventura 23.

**ACEITE:** existe urgência real, mas as decisões anteriores continuam importando.

## ADV-23 — Escrever a Aventura 23: final e epílogo

**BLOQUEADA POR:** ADV-22.

- [ ] Construir o confronto final a partir do Pacote selecionado.
- [ ] Usar os Vestígios, o mecanismo e o Vestígio de Solar definidos anteriormente.
- [ ] Incluir múltiplos objetivos e condições de sucesso.
- [ ] Incluir pelo menos duas formas preparadas de interferir no processo.
- [ ] Ajustar o encontro por objetivos, terreno, ameaças secundárias e economia de ações.
- [ ] Não ultrapassar configurações canônicas apenas por tamanho do grupo.
- [ ] Tornar a condição Sugoi interrompível e investigável, quando ocorrer.
- [ ] Fazer relações, aliados e consequências anteriores aparecerem.
- [ ] Resolver ou transformar a pergunta temática do antagonista.
- [ ] Incluir consequências imediatas.
- [ ] Incluir debriefing final.
- [ ] Incluir epílogos para Instituto, Belamar, Vanguarda, Tomás, NPCs e PCs.
- [ ] Definir o novo estado dos personagens.
- [ ] Produzir a transição final `23.yml`.
- [ ] Executar revisão completa do Arco III e da campanha.

**ACEITE:** o final resolve o plano, paga a preparação e mostra que tipo de heróis Belamar ganhou.

---

# Fase 4 — Capítulos auxiliares da publicação

## DOC-001 — Escrever “Preparando a campanha”

- [ ] Explicar a proposta e o tom.
- [ ] Orientar escolha do grande antagonista.
- [ ] Orientar escolha do Tenente Principal.
- [ ] Orientar preenchimento dos vínculos do Pacote.
- [ ] Explicar como usar as Frentes.
- [ ] Explicar como usar aventuras, Chamados e retorno ao hub.
- [ ] Explicar progressão por arcos.
- [ ] Explicar adaptações por número de jogadores.
- [ ] Explicar como usar consequências sem bloquear continuidade.
- [ ] Explicar sessão zero e expectativas.
- [ ] Remover qualquer referência ao pipeline interno de continuidade.

**ENTREGA:** capítulo canônico e publicável.  
**ACEITE:** um Mestre consegue preparar a campanha sem consultar documentos de desenvolvimento.

## DOC-002 — Escrever “Criando os heróis do Atlas”

- [ ] Definir pontuação inicial.
- [ ] Explicar candidatos, alunos e equipes.
- [ ] Oferecer perguntas de conceito.
- [ ] Orientar origens e manifestação de poderes.
- [ ] Orientar vínculos com Belamar, Atlas, família e colegas.
- [ ] Orientar nomes civis e heroicos.
- [ ] Orientar função principal na equipe.
- [ ] Integrar especializações, Kits e Técnicas.
- [ ] Incorporar a preservação da identidade mecânica.
- [ ] Orientar crescimento sem impor classes.
- [ ] Incluir criação de relações iniciais.
- [ ] Incluir limites adequados ao tom.

**ENTREGA:** capítulo para jogadores.  
**ACEITE:** o grupo consegue criar personagens apropriados sem ler segredos do Mestre.

## DOC-003 — Escrever “Oposição, perigos e coadjuvantes”

- [ ] Criar perfis rápidos de civis e multidões.
- [ ] Criar agentes de emergência.
- [ ] Criar heróis profissionais genéricos.
- [ ] Criar seguranças e criminosos comuns.
- [ ] Criar tropas tecnológicas, místicas, super-humanas e cósmicas.
- [ ] Criar drones, robôs e criaturas.
- [ ] Criar veículos e objetivos destrutíveis.
- [ ] Criar incêndios, colapsos, inundações e riscos urbanos.
- [ ] Criar regras ou notas de ajuste por escala.
- [ ] Validar contra as convenções mecânicas do projeto.
- [ ] Evitar substituir as fichas específicas das aventuras.

**ENTREGA:** capítulo de regras/fichas.  
**ACEITE:** aventuras não precisam reinventar oposição cotidiana.

## DOC-004 — Criar linha do tempo e quadro de progressão

- [ ] Resumir os três arcos.
- [ ] Mapear as 23 aventuras.
- [ ] Mostrar estado institucional por aventura.
- [ ] Mostrar faixa de pontuação esperada.
- [ ] Mostrar licenças e Marcos.
- [ ] Mostrar sequestros previstos.
- [ ] Mostrar introdução e função dos Vestígios.
- [ ] Mostrar revelações estruturais.
- [ ] Separar informação do jogador de informação do Mestre quando necessário.
- [ ] Garantir consistência com os snapshots internos, sem expor o pipeline.

**ENTREGA:** apêndice publicável.  
**ACEITE:** o Mestre visualiza toda a campanha em poucas páginas.

## DOC-005 — Criar folhas de campanha e handouts reutilizáveis

- [ ] Ficha da Equipe de Campo.
- [ ] Quadro de vínculos.
- [ ] Registro de licença.
- [ ] Formulário de Chamado.
- [ ] Dossiê da Central.
- [ ] Folha de debriefing.
- [ ] Controle de pistas para o Mestre.
- [ ] Controle das Frentes.
- [ ] Quadro da Vanguarda.
- [ ] Registro de NPCs aliados e rivais.
- [ ] Registro de consequências públicas.
- [ ] Folha de evolução individual.
- [ ] Preparar versões para impressão.

**ENTREGA:** apêndices e arquivos destacáveis.  
**ACEITE:** todos os formulários são usáveis sem consultar arquivos internos.

## DOC-006 — Criar referência rápida do Mestre

- [ ] Resumir Graus de ocorrência.
- [ ] Resumir licenças.
- [ ] Resumir estrutura de Chamado.
- [ ] Resumir testes, Ajuda e PA do módulo.
- [ ] Resumir Objetivos, XP e Marcos.
- [ ] Resumir encontros modulares.
- [ ] Resumir resgate e investigação.
- [ ] Resumir os 16 tenentes.
- [ ] Resumir os 12 grandes antagonistas.
- [ ] Incluir referências de página após diagramação.
- [ ] Validar legibilidade em duas ou quatro páginas.

**ENTREGA:** apêndice de consulta rápida.  
**ACEITE:** procedimentos mais frequentes podem ser consultados sem busca extensa.

## DOC-007 — Criar glossário

- [ ] Levantar termos próprios.
- [ ] Definir termos de cenário sem revelar segredos indevidos.
- [ ] Definir termos de Mestre em seção apropriada.
- [ ] Incluir Clarão, Vestígio, Vanguarda, Retorno, Chamado, Central, Agência Atlas, licenças, Ciclo Heroico, Frente, Pacote de Antagonista e Tenente Principal.
- [ ] Revisar consistência de grafia e capitalização.
- [ ] Criar links ou referências cruzadas.

**ENTREGA:** `apendices/glossario.md`.  
**ACEITE:** todos os termos próprios importantes possuem definição consistente.

## DOC-008 — Criar índice remissivo

- [ ] Definir ferramenta ou formato de geração.
- [ ] Marcar nomes, locais, conceitos e regras.
- [ ] Gerar índice após paginação estabilizada.
- [ ] Revisar remissões duplicadas.
- [ ] Incluir referências úteis, não todas as ocorrências.
- [ ] Regenerar na release candidate.

**ENTREGA:** índice remissivo final.  
**ACEITE:** entradas levam às páginas corretas do PDF final.

## DOC-009 — Criar créditos, licença e expediente

- [ ] Registrar autoria.
- [ ] Registrar revisão.
- [ ] Registrar ilustrações e mapas.
- [ ] Registrar diagramação.
- [ ] Registrar versão e data.
- [ ] Definir licença de distribuição.
- [ ] Redigir aviso de compatibilidade com 3DeT Victory.
- [ ] Registrar marcas de seus titulares.
- [ ] Registrar fontes e recursos licenciados.
- [ ] Registrar contato ou pasta do projeto.
- [ ] Revisar juridicamente a redação possível antes da publicação.

**ENTREGA:** front matter completo.  
**ACEITE:** a publicação identifica responsabilidades, direitos e versão.

## DOC-010 — Escrever orientação para mesas com jogadores jovens

- [ ] Definir tom e limites.
- [ ] Orientar sessão zero.
- [ ] Orientar ferramentas simples de segurança.
- [ ] Orientar consequências sem crueldade gráfica.
- [ ] Orientar rivalidades sem humilhação persistente.
- [ ] Orientar adultos como apoio sem retirar protagonismo.
- [ ] Orientar ausência de jogadores.
- [ ] Orientar conversa após cenas tensas.
- [ ] Decidir se entra como capítulo próprio ou seção de preparação.

**ENTREGA:** seção publicável.  
**ACEITE:** o módulo sustenta explicitamente o público jovem pretendido.

---

# Fase 5 — Mapas, ilustrações e handouts

## ART-001 — Criar inventário visual completo

- [ ] Listar ilustrações existentes e aprovadas.
- [ ] Listar personagens sem retrato.
- [ ] Listar locais sem mapa ou key art.
- [ ] Listar aventuras que exigem mapa.
- [ ] Listar pistas que exigem handout.
- [ ] Listar diagramas e infográficos necessários.
- [ ] Definir prioridade por dependência editorial.
- [ ] Registrar direitos e origem de cada ativo.

**ENTREGA:** `assets/inventario-visual.md`.  
**ACEITE:** toda imagem planejada possui finalidade, local e status.

## ART-002 — Produzir mapas gerais

- [ ] Mapa de Belamar.
- [ ] Mapa da Ilha da Aurora.
- [ ] Mapa do Parque Solar.
- [ ] Mapa geral do Instituto Atlas.
- [ ] Planta funcional da Central de Operações, se necessária.
- [ ] Versões com e sem marcadores.
- [ ] Escala e legenda consistentes.
- [ ] Aprovação e registro em `assets/imagens/aprovadas.md`.

**ENTREGA:** mapas gerais aprovados.  
**ACEITE:** mapas são legíveis no PDF e úteis na mesa.

## ART-003 — Produzir mapas específicos das aventuras

- [ ] Identificar necessidade durante cada `ADV-NN`.
- [ ] Criar briefing visual canônico.
- [ ] Produzir versão para Mestre.
- [ ] Produzir versão para jogadores quando necessário.
- [ ] Validar elementos secretos.
- [ ] Registrar versão aprovada.
- [ ] Vincular ao arquivo da aventura.

**ENTREGA:** mapas vinculados às 23 aventuras.  
**ACEITE:** nenhuma aventura exige mapa inexistente sem alternativa textual clara.

## ART-004 — Produzir retratos e ilustrações editoriais

- [ ] Corpo docente.
- [ ] Vanguarda.
- [ ] Alunos recorrentes.
- [ ] 16 tenentes.
- [ ] 12 grandes antagonistas.
- [ ] Personagens secundários essenciais das aventuras.
- [ ] Cenas de abertura dos arcos.
- [ ] Capa e contracapa.
- [ ] Registrar apenas versões aprovadas.

**ENTREGA:** conjunto visual aprovado.  
**ACEITE:** identidade visual consistente e nenhum ativo rejeitado entra no build.

## ART-005 — Produzir handouts

- [ ] Licenças.
- [ ] Dossiês da Central.
- [ ] Registros históricos.
- [ ] Recortes ou comunicados.
- [ ] Diagramas do mecanismo.
- [ ] Pistas dos Vestígios.
- [ ] Material específico dos Pacotes.
- [ ] Versões sem informação de Mestre.
- [ ] Arquivos para impressão.

**ENTREGA:** handouts associados às aventuras.  
**ACEITE:** cada handout possui instrução clara de quando entregar.

---

# Fase 6 — Revisão integrada

## QA-001 — Revisão de continuidade completa

- [ ] Regerar todos os snapshots 1–23.
- [ ] Verificar estados de todos os NPCs.
- [ ] Verificar conhecimentos e descobertas.
- [ ] Verificar mortes, ferimentos, ausências e sequestros.
- [ ] Verificar evolução de relações.
- [ ] Verificar localização de objetos e Vestígios.
- [ ] Verificar Frentes do antagonista.
- [ ] Verificar pistas e payoffs.
- [ ] Verificar promessas não resolvidas.
- [ ] Verificar que o final usa apenas elementos preparados.
- [ ] Corrigir fontes canônicas e aventuras, não apenas snapshots.

**ENTREGA:** relatório de continuidade sem erros críticos.  
**ACEITE:** nenhuma aventura contradiz o estado consolidado anterior.

## QA-002 — Revisão dos três arcos

- [ ] Aplicar checklist de arco ao Arco I.
- [ ] Aplicar checklist de arco ao Arco II.
- [ ] Aplicar checklist de arco ao Arco III.
- [ ] Verificar mudança de estado entre arcos.
- [ ] Verificar ritmo e variedade.
- [ ] Verificar progressão de relações.
- [ ] Verificar agência nos marcos.
- [ ] Verificar que consequências anteriores retornam.
- [ ] Verificar convergência e payoff no Arco III.

**ENTREGA:** relatório de estrutura dos arcos.  
**ACEITE:** cada arco possui pergunta, experiência, mudança e novo estado claros.

## QA-003 — Revisão mecânica

- [ ] Validar pontuação e escala.
- [ ] Validar pré-requisitos de Técnicas.
- [ ] Validar Desvantagens.
- [ ] Validar encontros modulares.
- [ ] Validar chefes como encontros com objetivos.
- [ ] Validar contrajogos.
- [ ] Validar XP e Marcos.
- [ ] Validar ajustes por tamanho de grupo.
- [ ] Validar regras de licenças e Chamados.
- [ ] Comparar com o Manual 3DeT Victory.

**ENTREGA:** relatório mecânico.  
**ACEITE:** não existem fichas ilegais ou encontros sem forma justa de interação.

## QA-004 — Revisão editorial

- [ ] Revisar coerência de voz.
- [ ] Revisar ortografia e gramática.
- [ ] Padronizar nomes e capitalização.
- [ ] Padronizar termos de cenário e mecânicos.
- [ ] Remover selos de desenvolvimento.
- [ ] Remover perguntas internas.
- [ ] Remover justificativas e instruções para agentes.
- [ ] Remover referências a arquivos internos.
- [ ] Revisar referências cruzadas.
- [ ] Revisar spoilers entre seções de jogador e Mestre.

**ENTREGA:** texto de publicação revisado.  
**ACEITE:** o livro lê como obra final, não como documentação de projeto.

## QA-005 — Revisão de adequação ao público

- [ ] Verificar intensidade de violência.
- [ ] Verificar ameaças a jovens personagens.
- [ ] Verificar se falhas não produzem humilhação automática.
- [ ] Verificar linguagem acessível.
- [ ] Verificar representação de adultos e instituições.
- [ ] Verificar tratamento de sequestros e perdas.
- [ ] Verificar ferramentas de segurança.
- [ ] Verificar que o protagonismo permanece com os jogadores.

**ENTREGA:** relatório de adequação.  
**ACEITE:** o material permanece apropriado ao público pretendido.

## QA-006 — Revisão visual e acessibilidade

- [ ] Verificar contraste.
- [ ] Verificar tamanho de fonte.
- [ ] Verificar legibilidade de tabelas.
- [ ] Verificar mapas em página e tela.
- [ ] Verificar imagens aprovadas.
- [ ] Verificar legendas e créditos.
- [ ] Adicionar texto alternativo na versão digital quando suportado.
- [ ] Verificar páginas órfãs e quebras.
- [ ] Verificar impressão em escala de cinza quando relevante.

**ENTREGA:** relatório visual.  
**ACEITE:** PDF legível em tela e impressão.

---

# Fase 7 — Publicação e release final

## REL-001 — Atualizar manifesto e sumário

- [ ] Adicionar cenário.
- [ ] Adicionar campanha.
- [ ] Adicionar as 23 aventuras aprovadas.
- [ ] Adicionar regras e fichas.
- [ ] Adicionar apêndices.
- [ ] Adicionar créditos e licença.
- [ ] Confirmar ordem editorial.
- [ ] Confirmar `publicar: true` apenas em arquivos completos.
- [ ] Remover stubs da release final.

**ENTREGA:** `publication.yml` e `SUMMARY.md` finais.  
**ACEITE:** todos os capítulos esperados entram uma única vez.

## REL-002 — Executar validações automatizadas

- [ ] Executar `python tools/check_links.py`.
- [ ] Executar verificador de conteúdo interno.
- [ ] Executar verificador de continuidade.
- [ ] Executar testes das ferramentas.
- [ ] Executar materialização.
- [ ] Executar geração do PDF.
- [ ] Verificar relatórios e corrigir erros.
- [ ] Repetir até build limpa.

**ENTREGA:** build sem erros.  
**ACEITE:** nenhum alerta crítico permanece.

## REL-003 — Produzir release candidate

- [ ] Definir número da versão.
- [ ] Gerar PDF.
- [ ] Gerar hash.
- [ ] Gerar relatório de capítulos.
- [ ] Verificar contagem de páginas.
- [ ] Fazer leitura integral do PDF.
- [ ] Testar links internos.
- [ ] Testar sumário.
- [ ] Testar índice remissivo.
- [ ] Testar impressão de páginas representativas.
- [ ] Registrar problemas encontrados.

**ENTREGA:** release candidate.  
**ACEITE:** apenas correções finais permanecem.

## REL-004 — Correções finais

- [ ] Corrigir problemas da release candidate nas fontes canônicas.
- [ ] Regerar continuidade quando aventuras mudarem.
- [ ] Regerar índice e referências de página.
- [ ] Regerar PDF.
- [ ] Repetir QA de regressão.
- [ ] Aprovar capa, expediente e versão.

**ENTREGA:** candidato final aprovado.  
**ACEITE:** zero erros bloqueadores e nenhuma pendência editorial obrigatória.

## REL-005 — Publicar versão final

- [ ] Gerar PDF final.
- [ ] Gerar pacote de handouts.
- [ ] Gerar pacote de mapas.
- [ ] Gerar fichas destacáveis.
- [ ] Gerar changelog.
- [ ] Atualizar `LATEST.json`.
- [ ] Arquivar relatórios.
- [ ] Registrar formalmente o identificador da versão final.
- [ ] Publicar nos canais definidos.
- [ ] Preservar fontes e assets usados na release.

**ENTREGA:** publicação final completa.  
**ACEITE:** leitor recebe livro, mapas, handouts e materiais auxiliares coerentes com a mesma versão.

---

# Dependências resumidas

```text
PUB-001..004
    ↓
CONT-001..007
    ↓
ADV-PLAN-001..005
    ↓
ADV-01 → ADV-02 → ... → ADV-23
    ↓
QA-001..006
    ↓
REL-001..005
```

As tarefas `DOC-*` e `ART-*` podem avançar em paralelo depois da auditoria, mas devem ser revisadas novamente após a conclusão das aventuras.

---

# Regra de passagem de estado entre aventuras

Uma aventura só pode ser marcada como concluída quando:

- [ ] seu arquivo público está aprovado;
- [ ] sua transição interna está registrada;
- [ ] o snapshot de saída foi gerado;
- [ ] o briefing da próxima aventura foi gerado;
- [ ] mortes, sequestros, ferimentos e ausências foram atualizados;
- [ ] descobertas foram atribuídas às pessoas corretas;
- [ ] pistas e conhecimentos foram atualizados separadamente;
- [ ] consequências condicionais possuem tratamento previsto;
- [ ] a próxima aventura foi revisada contra o novo estado;
- [ ] nenhuma informação interna vazou para a publicação.

A Aventura N+1 não deve ser redigida a partir da memória do autor. Ela deve usar:

1. fontes canônicas;
2. briefing `N+1`;
3. snapshot de entrada `N+1`;
4. Pacote selecionado;
5. diretrizes do arco e de aventuras.

---

# Critério final do projeto

A publicação está completa quando:

- [ ] todos os capítulos obrigatórios estão escritos;
- [ ] as 23 aventuras estão publicáveis;
- [ ] todo estado relevante possui continuidade verificável;
- [ ] o Pacote escolhido altera a história e o final;
- [ ] o livro não contém documentação de produção;
- [ ] mapas, fichas, ilustrações e handouts estão presentes;
- [ ] glossário, índice, créditos e licença estão completos;
- [ ] a build final não apresenta erros;
- [ ] o PDF foi lido e aprovado integralmente.
