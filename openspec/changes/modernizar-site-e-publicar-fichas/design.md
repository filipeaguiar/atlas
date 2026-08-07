## Context

O site Hugo atual é seguro, responsivo e funcional, mas usa uma apresentação deliberadamente mínima. O conteúdo de regras contém 25 fichas completas sem front matter: nove arquivos de antagonistas principais e quatro compêndios com quatro tenentes cada. Esses arquivos estão nas raízes editoriais, porém ainda não podem passar pelo materializador.

Não há fichas recuperadas para NPCs. Os três arquivos correspondentes no backup estão marcados `recuperacao-pendente` e `publicar: false`; portanto, as novas fichas serão declaradas como redação atual baseada somente nas descrições e funções já existentes nas fontes do projeto. O escopo aprovado inclui professores e funcionários da Aventura 1, oito estudantes recorrentes e a Vanguarda.

## Goals / Non-Goals

**Goals:**

- criar uma identidade visual contemporânea sem prejudicar leitura longa ou acessibilidade;
- tornar navegação, localização e consulta de fichas rápidas durante uma sessão;
- publicar as 25 fichas de inimigos após normalização e auditoria;
- criar fichas completas e jogáveis para os grupos de NPCs aprovados;
- preservar distinção entre estudante, apoio institucional, veterano, tenente e antagonista principal;
- manter manifesto, build estrito e Pages como gates de publicação.

**Non-Goals:**

- recuperar ou completar silenciosamente os stubs antigos de NPCs;
- publicar a Aventura 1 antes de seu gate próprio de aprovação;
- promover imagens aprovadas na curadoria;
- criar fichas de personagens dos jogadores;
- introduzir autenticação, CMS, framework JavaScript ou dependência de tema remoto;
- publicar PDFs.

## Decisions

### Sistema visual local e progressivo

O tema continuará sem bibliotecas externas. CSS local fornecerá fundo em camadas, gradientes discretos, superfícies translúcidas, cards, chips, tipografia fluida, navegação lateral refinada e estados de interação. HTML semântico continuará funcional sem JavaScript; qualquer melhoria interativa futura deverá ser progressiva.

A página inicial ganhará uma composição hero mais forte, métricas editoriais e cards com tratamento por seção. Capítulos terão barra de contexto, largura de leitura controlada e navegação anterior/próxima visual. Em telas estreitas, navegação e cards se reorganizarão sem ocultar conteúdo.

### Fichas como documentos editoriais normais

As fichas continuarão em Markdown canônico e entrarão somente pelo manifesto. O front matter adicionará `tipo: ficha`, `categoria` e `camada: mestre`. O gerador Hugo repassará apenas metadados de apresentação permitidos para aplicar uma classe/layout de ficha, sem expor proveniência interna.

Os nove antagonistas principais permanecerão em arquivos individuais. Os quatro compêndios de tenentes permanecerão agrupados por origem, com quatro fichas cada. NPCs serão organizados em três documentos: equipe do Atlas, estudantes recorrentes e Vanguarda. Essa granularidade equilibra navegação e manutenção e evita duplicar Tomás/Multiplex em duas fichas mecânicas concorrentes.

### Contrato mínimo de ficha

Cada personagem terá nome, papel, escala ou faixa de pontos, descrição de uso, atributos P/H/R, PV e, quando aplicável, PM e PA, perícias, vantagens, desvantagens ou limitações, recursos exclusivos e orientação de interpretação/tática. Categorias inaplicáveis serão omitidas em vez de preenchidas artificialmente.

Estudantes serão construídos próximos de 10 pontos e servirão como colegas, rivais ou apoio, não como protagonistas substitutos. Funcionários terão blocos voltados a suporte e segurança institucional. Vanguarda e antagonistas poderão usar patamares mais altos adequados a veteranos e chefes. Tomás terá uma única ficha que identifica o segredo de Multiplex apenas na camada do Mestre.

### Auditoria mecânica e editorial

A revisão usará as referências locais de 3DeT Victory apenas como consulta, sem publicá-las nem copiar trechos protegidos. Testes estruturais verificarão presença dos campos essenciais, valores numéricos plausíveis, identidades únicas, ausência de termos de recuperação pendente e coerência entre front matter e manifesto.

Expressões incompatíveis com o tom infantil, como morte obrigatória, serão convertidas para derrota, queda ou retirada quando isso não alterar a função mecânica. Tesouros e efeitos permanentes serão revistos para evitar recompensas desproporcionais ou instruções perigosas.

### Índices dentro da seção de Regras

A seção Regras receberá primeiro uma página de fichas de NPCs e depois fichas de inimigos, separadas por subtítulos e cards gerados pela navegação. O site usará categoria e tipo para exibir rótulos visuais, mas o PDF continuará recebendo o mesmo Markdown sem depender do tema.

## Risks / Trade-offs

- **[Fichas novas viram cânone sem playtest]** → Declarar origem como redação atual aprovada, manter valores conservadores e registrar revisão futura como possível sem negar a publicação solicitada.
- **[NPCs adultos roubam protagonismo]** → Técnicas de apoio concedem Ajuda, proteção ou informação; não resolvem Objetivos centrais no lugar dos personagens.
- **[Navegação cresce demais]** → Manter compêndios por grupos e destacar categorias no índice lateral.
- **[Visual moderno reduz legibilidade]** → Preservar contraste, largura de linha, foco visível, redução de movimento e fallback sem transparência.
- **[Conteúdo bruto de inimigos contém inconsistências]** → Auditar todos os 25 blocos antes de adicionar seus arquivos ao manifesto.
- **[Imagens parecem implicitamente aprovadas]** → Não copiar nenhum binário da curadoria nesta mudança.

## Migration Plan

1. Criar testes estruturais para as fichas e o tema.
2. Normalizar e revisar as 25 fichas existentes sem publicá-las ainda.
3. Redigir e validar os três compêndios de NPCs.
4. Implementar o novo sistema visual e metadados de apresentação.
5. Adicionar os documentos ao manifesto em ordem explícita.
6. Executar testes, build estrito e auditoria sem PDFs ou áreas internas.
7. Commitar e enviar para `main`; acompanhar o Pages e revisar o site publicado.
8. Em caso de falha visual, reverter apenas tema/layout; as fichas permanecem fontes canônicas independentes.
