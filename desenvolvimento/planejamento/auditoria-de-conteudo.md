---
titulo: "Auditoria do estado atual das fontes"
tipo: planejamento-interno
status: concluido
publicar: false
data: 2026-07-31
escopo: "PUB-002"
---

# Auditoria do estado atual das fontes

## Resultado executivo

A documentação já possui uma separação funcional entre quatro camadas:

1. **fontes canônicas modulares:** `cenario/`, `campanha/`, `regras/` e `apendices/`;
2. **fontes editoriais da publicação:** `publicacao/fontes/`;
3. **saídas geradas:** `publicacao/conteudo/` e `build/`;
4. **histórico:** `fonte-v0.13/` e versões consolidadas anteriores.

A fonte de verdade continua sendo a camada modular. Arquivos de publicação podem condensar, reorganizar e renomear capítulos, mas não substituem os capítulos canônicos. Arquivos em `build/` e `publicacao/conteudo/` nunca devem ser editados manualmente.

A release mais recente identificada na biblioteca é **`v0.2.0-alpha.1`**. O relatório de materialização associado registra **97 documentos incluídos e zero documentos não publicáveis copiados**. As 23 aventuras completas ainda não fazem parte da publicação.

## Limite desta auditoria

A auditoria foi feita a partir dos documentos do workspace disponíveis na Biblioteca de Arquivos, incluindo cópias produzidas em momentos diferentes. Como não houve acesso direto à pasta ativa do projeto, nomes que sofreram renumeração entre a árvore modular e `publicacao/fontes/` devem ser confirmados ao incorporar este pacote.

## Hierarquia de autoridade

| Prioridade | Camada | Regra |
|---:|---|---|
| 1 | `cenario/`, `campanha/`, `regras/`, `apendices/` | fonte canônica editável |
| 2 | `publicacao/fontes/` | adaptação editorial derivada das fontes canônicas |
| 3 | `publicacao/conteudo/`, `build/` | saída gerada; nunca editar |
| 4 | `fonte-v0.13/` e consolidados antigos | histórico somente leitura |
| 5 | conversas, prompts e memória de agentes | não são fonte canônica |

## Governança e build

| Documento ou área | Estado | Publicável? | Pendência | Dependências |
|---|---|---:|---|---|
| `README.md` | canônico de governança | não | manter comandos de validação atualizados | ferramentas de build |
| `AGENTS.md` | canônico de governança | não | manter alinhado à árvore real e à política de imagens | todos os capítulos |
| `SUMMARY.md` | mapa da árvore modular | não diretamente | confirmar nomes após renumerações recentes | fontes modulares |
| `publicacao/manifesto.yml` | manifesto ativo | não | manter lista de termos internos proibidos | `publicacao/fontes/` |
| `tools/materialize_publication.py` | gerador ativo | não | impedir qualquer cópia de `desenvolvimento/` | manifesto e fontes públicas |
| `tools/generate_pdf.py` | gerador ativo | não | validação final só após aventuras e paratextos | materialização |
| `build/relatorio-materializacao.md` | saída gerada | não | regenerar a cada release | materialização |
| `desenvolvimento/` | criada por este pacote | não | copiar para a pasta do projeto e manter fora da publicação | nenhuma |

## Cenário

| Fonte canônica | Estado | Uso na publicação | Pendência principal | Dependências |
|---|---|---|---|---|
| `cenario/01-visao-geral.md` | canônico; linguagem de especificação | síntese, não cópia direta | reescrita editorial | introdução |
| `cenario/02-extraordinarios.md` | canônico; diversidade aberta | síntese | não fechar origem única dos poderes | cenário geral |
| `cenario/03-sociedade-heroica.md` | canônico; regulamentação ampla aberta | síntese | distinguir licença interna do Atlas de legislação nacional/internacional | AHI e direito heroico |
| `cenario/04-belamar-e-atlas.md` | canônico | base factual direta | ampliar bairros e locais quando aventuras exigirem | aventuras |
| `cenario/05-programa-de-campo.md` | canônico | base operacional | nenhuma lacuna impeditiva para a Aventura 1 | hub do Atlas |
| `cenario/06-tomas-valenca.md` | canônico | base de personagem | limite, memória e custo das cópias permanecem abertos | regras de Tomás |
| `cenario/07-central-de-operacoes.md` | canônico | base operacional | nenhuma lacuna impeditiva | hub e Chamados |
| `cenario/08-corpo-docente.md` | canônico | elenco recorrente | professores não detalhados só devem surgir quando necessários | aventuras escolares |
| `cenario/09-vanguarda.md` | canônico | base de personagem e mistério | identidades civis dos quatro membros ativos permanecem secretas e não nomeadas | campanha do Retorno |
| `cenario/10-tragedia-memoria-publica.md` | canônico | versão pública | manter separada da verdade secreta | campanha/05 |
| `cenario/11-instituto-atlas-hub-jogavel.md` | canônico e operacional | principal fonte do hub | revisar links após qualquer renumeração | aventuras 1–16 |
| `cenario/12-alunos-recorrentes.md` | canônico | elenco recorrente | relações com PCs só podem nascer em jogo | aventuras escolares |
| `cenario/antagonistas/README.md` e quatro categorias | canônicos | catálogo de opções | nenhum antagonista escolhido por padrão | Pacotes |
| `cenario/tenentes/*` | 16 perfis canônicos | perfis de cenário | Tenente Principal depende do Pacote | regras e aventuras |

### NPCs recorrentes já disponíveis

- Direção e corpo docente: Álvaro Siqueira, Dalva Menezes, Lívia Monteiro/Métrica, Caio Ventura/Impacto, Janaína Rocha/Âncora, Raul Farias/Vestígio, Dra. Samira Nasser, Beatriz Leal e Tomás Valença.
- Alunos recorrentes: Lia Vasconcelos/Atalho, Ravi Moura/Trama, Cecília Dantas/Prumo, Noah Sato/Gambito, Malu Serrano/Rasura, Ícaro Tavares/Refrão, Sofia Mendonça/Pulso e Dante Arcos/Órbita.
- Vanguarda clássica: Solar, Multiplex, Prisma, Colosso, Oráculo e Vetora.

Nenhum dos oito alunos possui por padrão ligação secreta com Vanguarda, Multiplex, Vestígios ou o Retorno.

## Campanha

| Fonte canônica | Estado | Uso na publicação | Pendência principal | Dependências |
|---|---|---|---|---|
| `campanha/01-premissa-e-tom.md` | especificação canônica | interno; base para síntese | não materializar diretamente | introdução e aventuras |
| `campanha/02-estrutura-narrativa.md` | canônico de estrutura | síntese operacional | transformar princípios em procedimentos de Mestre | aventuras |
| `campanha/03-arcos.md` | canônico | visão geral | manter marcos como mudanças de estado | plano das 23 aventuras |
| `campanha/arcos/arco-1/README.md` | canônico | estrutura do Arco I | detalhar Aventuras 1–6 | estado inicial |
| `campanha/arcos/arco-2/README.md` | canônico | estrutura do Arco II | detalhar Aventuras 7–16 | continuidade do Arco I |
| `campanha/arcos/arco-3/README.md` | canônico | estrutura do Arco III | detalhar Aventuras 17–23 | pistas e sequestros |
| `campanha/04-tomas-e-a-campanha.md` | canônico | base do mentor | relação concreta com PCs nasce em jogo | aventuras 1–22 |
| `campanha/05-segredos-da-tragedia.md` | canônico secreto | dossiê do Mestre | preservar separação do conhecimento público | Pacote |
| `campanha/06-clarao-artificial-e-vestigios.md` | núcleo fixo + variáveis | dossiê do Mestre | mecanismo concreto depende do Pacote | Pacote selecionado |
| `campanha/07-retorno-e-sequestros.md` | canônico de estrutura | visão cronológica | conflito de posição do segundo sequestro descrito abaixo | plano geral |
| `campanha/08-confronto-final.md` | canônico de estrutura | regras do clímax | detalhamento depende do Pacote | Aventura 23 |
| `campanha/09-arquitetura-editorial.md` | especificação interna | não materializar | manter separado do livro | build |
| `campanha/10-principios-de-design.md` | especificação interna | não materializar | converter apenas em texto novo ao Mestre | aventuras |
| `campanha/11-diretrizes-de-design-de-aventuras.md` | manual interno | não materializar | usar como checklist de autoria | todas as aventuras |
| `campanha/12-diretrizes-de-design-de-antagonistas.md` | manual interno | não materializar | usar ao escolher Pacote | antagonistas |
| `campanha/13-diretrizes-de-estrutura-de-arcos.md` | manual interno | não materializar | usar no plano macro | três arcos |
| `campanha/14-diretrizes-de-pacotes-de-antagonista.md` | manual interno | não materializar | resolver inconsistência de cronologia | Pacotes |
| `campanha/15-colegas-e-rivalidades.md` | canônico de uso | síntese ao Mestre | equipe contraponto só depois de conhecer os PCs | aventuras escolares |
| `campanha/antagonistas/*` | 12 Pacotes completos | um overlay por campanha | selecionar um Pacote antes de escrever metaplot específico | PCs e decisão do Mestre |

### Estrutura fixa identificada

- 23 aventuras principais: 6 no Arco I, 10 no Arco II e 7 no Arco III.
- Aventura 1: ingresso no Atlas.
- Aventura 6: licença provisória.
- Aventura 11: primeiro sequestro e mudança para investigação ativa.
- Aventura 16: licença definitiva.
- Aventuras 17–23: convergência do Retorno.
- Aventura 19: descoberta de Tomás como Multiplex.
- Aventura 20: payoff do Tenente Principal.
- Aventura 21: plano formulado pelos personagens.
- Aventura 22: captura de Tomás.
- Aventura 23: tentativa final do Clarão artificial.

### Cronologia dos sequestros consolidada

A decisão editorial `DEC-001` consolidou os quatro marcos nas Aventuras **11, 14, 17 e 18**. A Aventura 14 contém a segunda operação de captura e confirma a seleção deliberada da Vanguarda; a Aventura 15 trata de suas consequências; a Aventura 16 conclui o arco institucional. A posição do marco é fixa, mas o resultado físico da captura permanece condicional às ações dos personagens.

## Regras

A árvore modular e a árvore editorial usam numerações diferentes. A publicação recente materializa os capítulos abaixo, derivados das fontes canônicas:

| Conteúdo | Fonte modular observada | Caminho editorial recente | Estado |
|---|---|---|---|
| convenções e separação ficção/regras | `regras/05-separacao-cenario-e-regras.md` e `regras/README.md` | `regras/01-convencoes-do-cenario.md` | publicável por síntese |
| pontuação, escala e progressão | `regras/02-objetivos-xp-e-marcos.md` + `regras/03-pontuacao-e-escala.md` | `regras/02-pontuacao-escala-e-progressao.md` | fechado para início: 10 pontos, Ningen |
| testes, equipe e PA | `regras/01-testes-equipe-e-pa.md` | `regras/03-testes-equipe-e-pa.md` | canônico |
| objetivos, XP e Marcos | `regras/02-objetivos-xp-e-marcos.md` | `regras/04-objetivos-xp-e-marcos.md` | canônico; depende das aventuras |
| operações do Atlas | cenário + regras | `regras/05-operacoes-do-atlas.md` | adaptação editorial |
| encontros modulares | `regras/04-antagonistas-e-encontros.md` | `regras/06-configuracoes-modulares-e-encontros.md` | canônico |
| tenentes | `regras/06` a `09` na árvore modular | `regras/07` a `10` na publicação | 16 fichas fechadas |
| alunos recorrentes | `regras/10-ancoras-mecanicas-alunos-recorrentes.md` | `regras/11-ancoras-mecanicas-alunos-recorrentes.md` | canônico |
| grandes antagonistas | `regras/antagonistas-principais/*` | mesmo agrupamento | 12 fichas fechadas |

A renumeração não constitui duplicação conceitual quando a camada pública é gerada. Ela se torna risco apenas se autores passarem a editar as duas versões como fontes independentes.

## Apêndices

| Fonte | Estado | Publicável? | Pendência |
|---|---|---:|---|
| `apendices/questoes-em-aberto.md` | interno e parcialmente obsoleto | não | executar PUB-003; várias questões do Atlas já foram respondidas |
| `apendices/matriz-de-pistas.md` | instrumento canônico do Mestre | sim, após revisão | completar distribuição pelas 23 aventuras |
| `apendices/mapa-migracao-v0.13.md` | auditoria histórica | não | manter somente leitura |

### Questões obsoletas detectadas

O arquivo de questões em aberto ainda pergunta por história, fundadora, modelo financeiro, quantidade e idade dos alunos, equipes, Exame de Admissão, licenças, chegada dos Chamados, graus, despacho, equipes profissionais e retirada de ocorrências. Esses pontos já foram respondidos em `cenario/11-instituto-atlas-hub-jogavel.md` e capítulos relacionados.

Também já foram definidos a aparência atual de Tomás e o modo geral como ele evita exibir cópias juntas. Permanecem realmente abertos o limite exato, compartilhamento de memória, custo/limitação do poder e evolução concreta da relação com Vetora.

## Duplicações e derivados

| Tipo | Exemplos | Tratamento |
|---|---|---|
| histórico consolidado | `fonte-v0.13/`, bíblias e módulos v0.x | somente leitura |
| build modular | `build/modulo-completo.md` | regenerar; nunca editar |
| materialização pública | `publicacao/conteudo/*` | regenerar; nunca editar |
| PDF preliminar | `build/modulo-publicacao.pdf`, releases alpha | artefato de revisão |
| fontes editoriais | `publicacao/fontes/*` | editáveis apenas como adaptação editorial, sempre rastreando fonte canônica |
| arquivos de continuidade | `desenvolvimento/continuidade/*` | internos; nunca materializar |

## Conteúdo que ainda não entra na publicação final

- este backlog e toda a árvore `desenvolvimento/`;
- questões em aberto e mapa de migração;
- prompts, snapshots, transições, briefings e handoffs;
- justificativas e manuais de design internos;
- stubs das aventuras;
- aventuras ainda incompletas ou não aprovadas;
- versões históricas e relatórios de build.

## Condições de aceite verificadas

- [x] Fontes canônicas classificadas por área.
- [x] Camadas derivadas e históricas identificadas.
- [x] Release atual comparada com as fontes.
- [x] Conteúdo não publicável identificado.
- [x] Questões obsoletas e decisões bloqueantes registradas.
- [x] Cronologia do segundo sequestro consolidada na Aventura 14 por decisão explícita.
- [x] A Aventura 1 possui base canônica suficiente para iniciar planejamento após validação do estado inicial.

## Próximas dependências

1. `PUB-003`: limpar `apendices/questoes-em-aberto.md` sem converter novas propostas em cânone.
2. `PUB-004`: definir critérios globais de pronto.
3. `CONT-004` a `CONT-006`: modelos de transição, briefing e compilação de estado.
4. `ADV-PLAN-001`: plano macro das 23 aventuras.
