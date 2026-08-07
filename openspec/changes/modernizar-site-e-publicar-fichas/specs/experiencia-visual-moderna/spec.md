## ADDED Requirements

### Requirement: Identidade visual contemporânea
O site SHALL apresentar uma identidade visual coesa e contemporânea por meio de hierarquia tipográfica, cores, superfícies, espaçamento, cards e indicadores consistentes, sem carregar tema ou fonte remota.

#### Scenario: Página inicial
- **WHEN** o visitante abre a página inicial
- **THEN** encontra título, natureza do módulo, versão, estado editorial e acesso visualmente distinto às seções publicadas

#### Scenario: Capítulo de conteúdo
- **WHEN** o visitante abre um capítulo
- **THEN** título, seção, categoria, corpo e navegação sequencial possuem hierarquia visual inequívoca

### Requirement: Apresentação especializada de fichas
O site SHALL reconhecer documentos com `tipo: ficha` e SHALL apresentar seus blocos mecânicos com rótulos, estatísticas e seções distinguíveis durante consulta rápida.

#### Scenario: Ficha de inimigo
- **WHEN** um documento manifestado declara `tipo: ficha` e categoria de inimigo
- **THEN** a página exibe sinalização de ficha do Mestre e tratamento visual próprio sem alterar o conteúdo mecânico

#### Scenario: Ficha de NPC
- **WHEN** um documento manifestado declara categoria de NPC
- **THEN** a página diferencia o grupo de apoio dos antagonistas por rótulo e cor de destaque

#### Scenario: Bloco de atributos
- **WHEN** uma ficha contém P, H, R, PV, PM ou PA em sua linha mecânica
- **THEN** o site apresenta cada estatística em célula própria, legível e identificada, sem alterar o Markdown canônico

#### Scenario: Card completo inspirado em TCG
- **WHEN** o documento contém uma ou mais fichas
- **THEN** cada personagem é apresentado em um único card com moldura, cabeçalho, corpo, atributos, listas e rodapé integrados

#### Scenario: Características em lista
- **WHEN** a ficha informa perícias, vantagens, desvantagens ou limitações
- **THEN** cada categoria aparece como item de lista não ordenada dentro do card

### Requirement: Navegação escalável
O site SHALL manter navegação utilizável com o aumento de capítulos e SHALL agrupar visualmente páginas por seção e categoria.

#### Scenario: Seção com muitas fichas
- **WHEN** a seção Regras contém operações, compêndios de NPCs e fichas de inimigos
- **THEN** o visitante consegue localizar cada documento por título e categoria sem percorrer conteúdo integral

#### Scenario: Posição atual
- **WHEN** o visitante está em uma ficha
- **THEN** a navegação indica página atual, seção e acesso anterior/próximo

### Requirement: Responsividade e acessibilidade preservadas
O novo visual MUST preservar HTML semântico, foco visível, contraste legível, redução de movimento, ampliação de texto e ausência de rolagem horizontal estrutural.

#### Scenario: Preferência por movimento reduzido
- **WHEN** o sistema informa `prefers-reduced-motion: reduce`
- **THEN** transições e animações não essenciais são removidas

#### Scenario: Tela estreita
- **WHEN** a viewport possui largura de dispositivo móvel
- **THEN** cards e fichas se reorganizam em uma coluna, enquanto o menu começa oculto e abre como painel lateral sobreposto que pode ser fechado

#### Scenario: Hierarquia editorial
- **WHEN** um capítulo contém títulos de níveis 1 a 4, texto, listas, citações e tabelas
- **THEN** cada nível e elemento possui tratamento visual distinto e consistente com sua função hierárquica

#### Scenario: CSS indisponível
- **WHEN** a folha de estilo não carrega
- **THEN** a ordem semântica do HTML ainda permite ler e navegar pelo módulo

### Requirement: Ausência de dependências de rastreamento
O tema MUST NOT carregar analytics, trackers, fontes remotas, scripts de terceiros ou recursos externos necessários à renderização.

#### Scenario: Build do site
- **WHEN** o site é gerado em modo estrito
- **THEN** seus layouts, fontes e assets visuais são resolvidos exclusivamente a partir de arquivos locais aprovados

#### Scenario: Fontes personalizadas
- **WHEN** a folha de estilo é carregada
- **THEN** o site usa famílias tipográficas personalizadas hospedadas localmente, com fallback de sistema e licenças incluídas
