## ADDED Requirements

### Requirement: Seleção positiva compartilhada
O gerador do site Hugo SHALL publicar somente documentos declarados em `publicacao/manifest.yml`, na ordem definida pelo manifesto, e aceitos pelas mesmas validações editoriais do pipeline do livro do Mestre.

#### Scenario: Documento manifestado e canônico
- **WHEN** um documento canônico, publicável e localizado em raiz permitida consta no manifesto
- **THEN** o site contém uma página para esse documento na seção e posição declaradas

#### Scenario: Documento presente mas não manifestado
- **WHEN** um arquivo existe em uma raiz editorial, mas não consta no manifesto
- **THEN** o site não contém o arquivo nem conteúdo derivado dele

#### Scenario: Fonte proibida declarada
- **WHEN** o manifesto ou um documento tenta alcançar conteúdo em área proibida
- **THEN** o build falha antes de produzir um site publicável

### Requirement: Site dirigido ao Mestre
O site SHALL se apresentar como módulo de campanha para o Mestre e SHALL preservar o conteúdo integral aprovado, sem criar automaticamente perfil público, livro do jogador ou filtragem de segredos.

#### Scenario: Conteúdo reservado no manifesto
- **WHEN** um capítulo do Mestre com segredos está aprovado e declarado no manifesto
- **THEN** o capítulo é publicado integralmente com indicação de que o site se destina ao Mestre

### Requirement: Navegação editorial
O site SHALL oferecer página inicial, navegação ordenada por seções e capítulos, links para capítulo anterior e seguinte e indicação da versão e do estado editorial do livro.

#### Scenario: Leitura sequencial
- **WHEN** o visitante abre um capítulo intermediário
- **THEN** a página oferece acesso ao capítulo anterior, ao próximo capítulo e à seção correspondente

#### Scenario: Seção sem documentos
- **WHEN** uma seção declarada não contém documentos
- **THEN** o site apresenta a seção como conteúdo em preparação sem inventar capítulos

### Requirement: Renderização responsiva e acessível
O site SHALL renderizar o Markdown aprovado em HTML semântico e navegável em telas largas e estreitas, com contraste legível, foco visível, hierarquia de títulos e texto alternativo preservado para imagens.

#### Scenario: Navegação em tela estreita
- **WHEN** o site é aberto em uma viewport móvel
- **THEN** conteúdo e navegação permanecem utilizáveis sem rolagem horizontal estrutural

#### Scenario: Navegação por teclado
- **WHEN** o visitante percorre links e controles usando teclado
- **THEN** o foco atual permanece visualmente identificável

### Requirement: Links e recursos publicados com segurança
O materializador SHALL copiar somente recursos locais alcançáveis a partir dos documentos manifestados, SHALL evitar colisões de nomes e SHALL reescrever links internos para funcionar sob uma base URL com subdiretório.

#### Scenario: Imagem referenciada por capítulo
- **WHEN** um capítulo manifestado referencia uma imagem válida em área permitida
- **THEN** a imagem é copiada para a árvore positiva do site e a página aponta para sua URL publicada

#### Scenario: Imagem apenas aprovada na curadoria
- **WHEN** uma imagem está aprovada na curadoria, mas não foi promovida e referenciada por uma fonte manifestada
- **THEN** a imagem não é incluída no site

#### Scenario: Link entre capítulos manifestados
- **WHEN** um capítulo contém link para outro capítulo também manifestado
- **THEN** o site gera um link funcional entre as respectivas páginas

### Requirement: Build local reproduzível
O projeto SHALL fornecer um comando documentado que valide, materialize e gere o site em diretório descartável usando uma versão suportada do Hugo Extended.

#### Scenario: Build estrito bem-sucedido
- **WHEN** manifesto, fontes, links, recursos e Hugo são válidos
- **THEN** o comando termina com sucesso e produz o site completo em `build/site/`

#### Scenario: Hugo ausente
- **WHEN** o executável Hugo não está disponível
- **THEN** o comando falha com mensagem que informa o requisito ausente
