## Context

A árvore possui nove marcadores fundamentais cuja função já é conhecida pelo sumário, mas cujo conteúdo original não está disponível. Existe, porém, uma introdução editorial completa, aprovada e publicável que sintetiza o mundo, Belamar, o Atlas, a Vanguarda, a Tragédia e a estrutura de jogo. Também existem capítulos integrais sobre Operações do Atlas e regras gerais. Esses documentos permitem escrever uma nova versão conservadora dos fundamentos sem usar planejamento interno como fonte e sem resolver as lacunas registradas em `apendices/questoes-em-aberto.md`.

A principal dificuldade não é técnica, mas epistemológica: o projeto deve distinguir conteúdo recuperado, reescrita aprovada, explicação pública, segredo do Mestre e questão ainda aberta. O texto novo precisa ser útil na mesa sem inventar silenciosamente números, instituições, nomes, cronologias ou explicações cosmológicas.

## Goals / Non-Goals

**Goals:**

- substituir nove marcadores por capítulos completos, coerentes e publicáveis;
- rastrear cada afirmação factual até uma fonte integral aprovada;
- produzir uma apresentação do cenário segura para jogadores, sem segredos da campanha;
- explicar Belamar e o Atlas em termos jogáveis usando apenas elementos estabelecidos;
- atualizar inventário e manifesto de forma auditável;
- reduzir a recuperação pendente de 94 para 85 documentos.

**Non-Goals:**

- reproduzir ou alegar reproduzir o texto original perdido;
- detalhar Tomás, professores ou alunos recorrentes;
- explicar a verdadeira natureza do Clarão;
- definir AHI, legislação mundial ou demografia extraordinária;
- revelar Vestígios, sobrevivência do antagonista, Pacote escolhido ou identidade de Tomás;
- escrever aventuras, antagonistas, fichas ou o PDF.

## Decisions

### 1. Chamar o trabalho de reescrita, não recuperação

Os capítulos usarão `status: canon`, `origem: reescrita-aprovada`, `publicar: true` e uma lista de fontes factuais. O inventário registrará `estado_recuperacao: reescrito-aprovado`. O histórico continuará mostrando que havia um marcador e que o texto integral original não foi recuperado.

Alternativa considerada: manter `origem: biblioteca-do-projeto`. Rejeitada porque sugeriria falsamente recuperação integral.

### 2. Criar matriz factual antes dos capítulos

Será criado um documento interno e não publicável em `desenvolvimento/planejamento/` com uma linha por afirmação ou conjunto coeso de afirmações. Cada registro terá:

- identificador;
- formulação permitida;
- classificação: `fato-fixo`, `memoria-publica`, `limite-aberto` ou `orientacao-de-jogo`;
- fonte integral e seção;
- capítulos autorizados;
- formulações proibidas ou riscos de spoiler.

Fontes permitidas nesta etapa:

- `publicacao/fontes/introducao/01-introducao.md`;
- `regras/README.md`;
- `regras/05-operacoes-do-atlas.md`;
- `AGENTS.md`, apenas para restrições de governança;
- `apendices/questoes-em-aberto.md`, apenas para identificar o que não pode ser definido.

`desenvolvimento/`, inventários e relatórios podem apontar lacunas, mas não fundamentar fatos publicados.

### 3. Proibir novos fatos estruturais não aprovados

A reescrita pode reorganizar, explicar e exemplificar material já aprovado. Exemplos sem fonte devem ser formulados como possibilidades de mesa, não como fatos históricos do mundo. Novos nomes próprios, números, datas, órgãos, bairros, relações ou origens exigirão atualização dos artefatos e aprovação explícita antes de entrar nos capítulos.

Alternativa considerada: completar lacunas criativamente para obter capítulos mais extensos. Rejeitada porque violaria a recuperação controlada e poderia bloquear decisões futuras.

### 4. Separar informação pública de segredos da campanha

Os nove capítulos serão seguros para jogadores. A Vanguarda e a Tragédia serão apresentadas segundo a memória pública disponível:

- Solar morreu salvando Belamar;
- a Vanguarda evacuou a cidade e o responsável foi considerado derrotado;
- Multiplex sobreviveu e desapareceu da vida pública;
- o Parque Solar preserva a memória do desastre.

Não aparecerão a identidade de Tomás, os Vestígios, o sexto Vestígio, a sobrevivência do antagonista ou a operação do Retorno.

### 5. Dividir responsabilidades entre nove capítulos

- `01-visao-geral.md`: proposta do cenário, escala humana e temas de heroísmo responsável.
- `02-extraordinarios.md`: diversidade de capacidades e ausência de origem universal definida.
- `03-sociedade-heroica.md`: convivência social com Extraordinários sem fechar legislação global.
- `04-belamar-e-atlas.md`: cidade litorânea, Ilha da Aurora, Parque Solar e papel geral do Atlas.
- `05-programa-de-campo.md`: formação, licenças, Graus e responsabilidade estudantil.
- `07-central-de-operacoes.md`: Chamados, dossiês, supervisão e debriefing.
- `09-vanguarda.md`: formação clássica, funções públicas e legado.
- `10-tragedia-memoria-publica.md`: versão pública e memória urbana da Tragédia.
- `11-instituto-atlas-hub-jogavel.md`: campus como escola, residência, agência e espaço recorrente de jogo.

Tomás, corpo docente e alunos permanecem nos marcadores `06`, `08` e `12` para mudança posterior.

### 6. Usar estrutura orientada à mesa

Cada capítulo combinará explicação concisa com elementos utilizáveis: perguntas de criação, maneiras de apresentar lugares, pressões cotidianas, expectativas institucionais ou ganchos genéricos. Esses elementos não estabelecerão eventos novos do metaplot.

### 7. Ativar somente depois da validação conjunta

Os nove documentos serão adicionados ao manifesto em uma seção `cenario` somente depois de:

- removerem linguagem interna;
- passarem por validação de links e arquitetura;
- apresentarem proveniência válida;
- não conterem termos proibidos;
- serem classificados no inventário como reescritos e aprovados.

A release materializada passará de 3 para 12 documentos.

## Risks / Trade-offs

- **[Capítulos excessivamente genéricos]** → priorizar procedimentos de mesa e exemplos condicionais em vez de inventar fatos.
- **[Texto público revela o mistério]** → validar termos e afirmações reservadas, mantendo Tragédia e Vanguarda na perspectiva pública.
- **[Introdução é usada como explicação universal]** → rastrear afirmações individualmente e respeitar os limites abertos.
- **[Planejamento interno vaza para o livro]** → impedir `desenvolvimento/` como fonte factual e validar termos internos.
- **[Reescrita é confundida com recuperação]** → metadados e inventário declaram explicitamente `reescrita-aprovada`.
- **[Duplicação entre capítulos]** → definir responsabilidade principal de cada arquivo e usar referências cruzadas.
- **[Contagem de marcadores diverge]** → atualizar nove registros atomicamente e exigir total físico igual a 85.

## Migration Plan

1. Criar branch a partir da `main` consolidada.
2. Inventariar e calcular hashes dos nove marcadores.
3. Construir e validar a matriz factual interna.
4. Escrever os capítulos em três blocos: mundo; Atlas operacional; legado público.
5. Revisar cruzamentos, spoilers, questões abertas e linguagem interna.
6. Alterar metadados somente após cada capítulo estar completo.
7. Atualizar inventário e contagem de marcadores de 94 para 85.
8. Adicionar os nove capítulos ao manifesto na ordem editorial.
9. Executar validadores e materializar 12 documentos.
10. Revisar diff, commit e branch remota.

**Rollback:** restaurar os nove marcadores e o inventário pelo commit anterior. Como a reescrita não será chamada de recuperação integral, nenhum conteúdo original será sobrescrito sem histórico Git.

## Open Questions

Se alguma fonte integral adicional for encontrada durante a implementação, a execução deve pausar para decidir se o capítulo será recuperado ou reescrito. Não se misturam silenciosamente os dois processos.
