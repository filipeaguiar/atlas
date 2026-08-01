## Context

A camada publicável contém a introdução integral, nove capítulos fundamentais de cenário e duas fontes de regras, mas os seis capítulos que organizam a campanha ainda são marcadores `recuperacao-pendente`. A introdução canônica já estabelece a premissa do Mestre, os três arcos, a progressão esperada e a estrutura de 23 aventuras. Ela também mistura fatos fixos, resultados narrativos que precisam permanecer condicionais e elementos variáveis dos doze Pacotes de Antagonista.

A reconstrução precisa ser declarada como texto novo aprovado, não como recuperação do original. `desenvolvimento/` pode registrar matriz, revisão e invariantes, mas não serve como autoridade narrativa nem entra no livro. A segunda operação ocorre na Aventura 14; sua captura física é condicional, a Aventura 15 trata das consequências e a 16 encerra o Arco II.

## Goals / Non-Goals

**Goals:**

- reconstruir seis capítulos estruturais úteis ao Mestre com proveniência explícita;
- separar fato fixo, opção de Pacote, consequência condicional, segredo do Mestre e exemplo de mesa;
- apresentar os três arcos como mudanças de responsabilidade, não roteiros obrigatórios;
- manter a estrutura de 6, 10 e 7 aventuras e os Marcos de licença;
- preparar uma base estável para planejar as 23 aventuras;
- reduzir exatamente seis marcadores e ativar exatamente seis documentos.

**Non-Goals:**

- detalhar qualquer uma das 23 aventuras;
- escolher antagonista, Tenente Principal, Frentes, pistas ou vínculos com personagens jogadores;
- reescrever os capítulos `campanha/04` a `campanha/15` ou os Pacotes;
- ativar stubs de aventuras;
- reconstruir regras ausentes, elenco ou fichas;
- apresentar os capítulos do Mestre como material seguro para jogadores;
- alterar regras de 3DeT Victory ou gerar o PDF final.

## Decisions

### 1. Usar uma matriz factual específica da campanha

Antes da escrita, será criada uma matriz não publicável em `desenvolvimento/planejamento/`. Cada entrada terá formulação autorizada, classe, fonte integral, seção e capítulos permitidos. As classes mínimas serão `fixo`, `segredo-do-mestre`, `resultado-condicional`, `opcao-de-pacote`, `progressao` e `exemplo-editorial`.

A fonte primária será `publicacao/fontes/introducao/01-introducao.md`. Capítulos canônicos ativos de cenário e regras poderão apoiar explicações já aprovadas. Marcadores, inventário, histórico e documentos internos não poderão fundamentar afirmações narrativas.

**Alternativa rejeitada:** escrever diretamente a partir da introdução. A mistura entre estrutura fixa e desfechos aparentes tornaria fácil transformar uma operação em captura obrigatória ou uma opção de Pacote em cânone universal.

### 2. Fixar seis responsabilidades editoriais

- `campanha/01-premissa-e-tom.md`: contrato da campanha, tom, público do capítulo e papel da nova geração;
- `campanha/02-estrutura-narrativa.md`: funcionamento de aventuras, Chamados, informação, consequências, Marcos e agência;
- `campanha/03-arcos.md`: mapa de 23 aventuras, progressão e transições entre os três arcos;
- `campanha/arcos/arco-1/README.md`: candidatura, ingresso, formação e licença provisória;
- `campanha/arcos/arco-2/README.md`: atuação em Belamar, investigação crescente e licença definitiva;
- `campanha/arcos/arco-3/README.md`: convergência do Retorno, revelações e clímax condicionado às ações dos personagens.

Referências cruzadas substituirão repetição extensa. O capítulo geral apresenta o mapa; cada arco detalha pressões, mudanças e possibilidades.

**Alternativa rejeitada:** reunir tudo em `campanha/03-arcos.md`. Isso reduziria navegação e deixaria pouca base para conectar futuramente as aventuras a seus arcos.

### 3. Tratar a estrutura como pressões e Marcos, não resultados obrigatórios

Números de aventuras, início da investigação, operações de captura e Marcos institucionais podem permanecer fixos. Êxito, fracasso, captura física, ordem de pistas dentro do espaço permitido e relações pessoais serão descritos como estados condicionais ou consequências adaptáveis.

A Aventura 14 sempre contém a segunda operação. A Aventura 15 sempre responde ao resultado produzido, e a 16 encerra o arco com a mudança institucional. Nenhum texto pressuporá silenciosamente que a captura física ocorreu.

**Alternativa rejeitada:** reproduzir literalmente todos os desfechos resumidos na introdução. Isso entraria em conflito com a agência exigida pelo projeto.

### 4. Publicar segredos apenas na camada declarada do Mestre

Os capítulos poderão explicar Tomás/Multiplex, Vestígios, Retorno e estrutura secreta quando isso for necessário ao preparo do Mestre e estiver autorizado pela introdução. Cada capítulo que contiver essas informações será claramente marcado como material do Mestre. Referências em capítulos públicos de cenário continuarão protegidas.

Detalhes dependentes do Pacote serão descritos como campos a selecionar, nunca como verdade única. A reconstrução não antecipará mecanismos concretos dos doze overlays.

**Alternativa rejeitada:** remover todos os segredos dos fundamentos da campanha. Isso impediria que o Mestre compreendesse a progressão e preparasse pistas de forma responsável.

### 5. Fazer a transição editorial de modo atômico e verificável

Os seis marcadores terão hashes registrados antes da substituição. Após aprovação individual, receberão `status: canon`, `origem: reescrita-aprovada`, `publicar: true`, indicação de camada do Mestre e fontes factuais. O inventário preservará o hash e registrará que o original integral não foi recuperado.

A atualização final deverá resultar em 79 marcadores pendentes, 23 stubs, 97 documentos de legado, 15 reescritas aprovadas acumuladas e 18 documentos ativos no manifesto. Verificadores validarão escopo, proveniência, condicionais, fronteiras de segredo e materialização.

**Alternativa rejeitada:** ativar capítulos antes de atualizar inventário e verificadores. Isso criaria divergência entre estado físico e estado editorial.

## Risks / Trade-offs

- **[A introdução usa formulações que parecem desfechos fixos]** → A matriz classificará operações separadamente de resultados e a revisão procurará linguagem de captura obrigatória.
- **[Segredos do Mestre podem vazar para capítulos públicos]** → Validadores separarão explicitamente caminhos de cenário público e campanha do Mestre.
- **[Os capítulos podem virar sinopses lineares das 23 aventuras]** → O escopo proíbe títulos e enredos detalhados e exige pressões, alternativas e consequências adaptáveis.
- **[Opções dos Pacotes podem ser generalizadas]** → Toda afirmação variável será rotulada como escolha de preparação ou possibilidade, sem selecionar overlay.
- **[Repetição entre introdução, mapa e capítulos de arco]** → Cada arquivo terá responsabilidade principal e referências cruzadas revisadas.
- **[A contagem editorial pode divergir durante aprovação parcial]** → Inventário e manifesto refletirão apenas capítulos individualmente aprovados; a meta 79/18 só será aceita com os seis completos.
