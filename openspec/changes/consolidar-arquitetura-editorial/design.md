## Context

A reconstrução preserva duas arquiteturas sobrepostas. `publicacao/manifest.yml` é usado pelo materializador atual e declara fontes e destinos explícitos; `publicacao/manifesto.yml` descreve uma publicação histórica baseada em uma pasta editorial incompleta. `SUMMARY.md` representa a árvore modular pretendida, enquanto o materializador gera outro sumário contendo apenas os três documentos atualmente aprovados.

A seção de regras expõe a divergência mais visível: `regras/README.md` já aponta para a numeração editorial desejada, mas os marcadores modulares permanecem em caminhos antigos. Há cinco links quebrados, duas posições `05-*` e uma sequência de fichas incompatível com a ordem pública histórica. O inventário registra 94 caminhos pendentes, mas o verificador apenas conta a lista JSON e não prova que cada arquivo físico existe e continua pendente.

A mudança deve organizar contratos e caminhos sem transformar marcadores em conteúdo, sem recuperar capítulos e sem incluir planejamento interno na publicação.

## Goals / Non-Goals

**Goals:**

- definir uma fonte de verdade para cada camada editorial;
- manter um único manifesto operacional;
- distinguir sumário-alvo da árvore e sumário real de cada release;
- normalizar os caminhos das regras com migração auditável;
- tornar o inventário de recuperação verificável contra o sistema de arquivos;
- detectar links quebrados e divergências entre inventário, manifesto e metadados;
- preparar caminhos estáveis para cenário, campanha, aventuras, regras e apêndices.

**Non-Goals:**

- preencher qualquer marcador `recuperacao-pendente`;
- declarar hipóteses ou questões abertas como cânone;
- escrever aventuras ou fichas;
- escolher um Pacote de Antagonista;
- implementar composição ou geração de PDF;
- remover histórico ou o baseline Git.

## Decisions

### 1. Manter uma única lista positiva de publicação

`publicacao/manifest.yml` será o único manifesto operacional. Todo materializador, verificador e comando documentado deverá usá-lo por padrão. O arquivo recuperado `publicacao/manifesto.yml` será movido para `historico/publicacao/` com nome que explicite sua natureza histórica e seu caminho novo será registrado no inventário.

Alternativa considerada: fundir os dois formatos. Rejeitada porque o manifesto histórico contém referências inexistentes e não expressa origem e destino por documento.

### 2. Atribuir funções diferentes aos dois sumários

`SUMMARY.md` continuará sendo o **sumário-alvo das fontes modulares**: ele pode listar caminhos pendentes para mostrar a arquitetura que ainda precisa ser restaurada. Isso não torna esses arquivos canônicos ou publicáveis.

`publicacao/conteudo/SUMMARY.md` continuará sendo o **sumário real da release**, gerado exclusivamente a partir dos documentos ativos no manifesto. Ele nunca será editado manualmente.

A documentação deverá nomear explicitamente as duas funções. O materializador não usará `SUMMARY.md` para selecionar arquivos.

Alternativa considerada: usar um único sumário para planejamento e release. Rejeitada porque faria capítulos ausentes parecerem publicados ou esconderia a arquitetura-alvo.

### 3. Normalizar a numeração canônica das regras

Os marcadores serão movidos, sem alteração narrativa, para a sequência já indicada por `regras/README.md` e pela camada editorial histórica:

| Caminho anterior | Caminho canônico-alvo |
|---|---|
| `regras/05-separacao-cenario-e-regras.md` | `regras/01-convencoes-do-cenario.md` |
| `regras/03-pontuacao-e-escala.md` | `regras/02-pontuacao-escala-e-progressao.md` |
| `regras/01-testes-equipe-e-pa.md` | `regras/03-testes-equipe-e-pa.md` |
| `regras/02-objetivos-xp-e-marcos.md` | `regras/04-objetivos-xp-e-marcos.md` |
| `regras/04-antagonistas-e-encontros.md` | `regras/06-configuracoes-modulares-e-encontros.md` |
| `regras/06-fichas-tenentes-tecnologicos.md` | `regras/07-fichas-tenentes-tecnologicos.md` |
| `regras/07-fichas-tenentes-misticos.md` | `regras/08-fichas-tenentes-misticos.md` |
| `regras/08-fichas-tenentes-super-humanos.md` | `regras/09-fichas-tenentes-super-humanos.md` |
| `regras/09-fichas-tenentes-cosmicos.md` | `regras/10-fichas-tenentes-cosmicos.md` |
| `regras/10-ancoras-mecanicas-alunos-recorrentes.md` | `regras/11-ancoras-mecanicas-alunos-recorrentes.md` |

`regras/05-operacoes-do-atlas.md` permanece no lugar. O conteúdo dos marcadores não será completado ou reinterpretado. `SUMMARY.md`, inventário, metadados de fontes editoriais e referências internas serão atualizados de forma atômica. Os caminhos antigos permanecerão documentados somente no mapa de migração e no histórico.

Alternativa considerada: alterar apenas os links para os nomes antigos. Rejeitada porque perpetuaria duas numerações, duas posições 05 e novo retrabalho durante a publicação.

### 4. Definir o destino das aventuras completas

`publicacao/stubs/` permanece área interna e não publicável. Aventuras completas e aprovadas serão fontes em `campanha/aventuras/`, organizadas por número estável de 01 a 23, e só entrarão na release quando listadas no manifesto. Esta mudança apenas documenta e prepara o contrato; não move os stubs.

### 5. Evoluir o inventário para registros verificáveis

`recuperacao/inventario.json` receberá versão de esquema e registros editoriais capazes de representar, no mínimo:

- caminho atual;
- caminho anterior, quando migrado;
- classe do documento;
- estado de recuperação;
- status esperado no front matter;
- publicabilidade;
- existência física esperada;
- origem ou evidência;
- destino editorial, quando aplicável.

O inventário continuará distinguindo arquivos integrais, reconstruídos e pendentes. A migração de caminho não será registrada como recuperação de conteúdo.

### 6. Separar verificações especializadas

`tools/check_recovery.py` validará inventário, existência física, status, contagens protegidas, stubs e decisões estruturais da recuperação.

Um verificador de arquitetura e links validará:

- links Markdown locais nas fontes e documentos operacionais;
- fontes e destinos do manifesto;
- destinos duplicados;
- fronteiras proibidas;
- coerência entre caminhos ativos, sumário-alvo e inventário;
- ausência de caminhos editoriais antigos fora de histórico e migração.

Os verificadores retornarão código diferente de zero diante de erro e separarão erro de aviso. Saídas geradas e histórico serão excluídos de verificações que não se apliquem a eles.

### 7. Preservar autoridade e não inferir cânone

Mover, indexar ou validar um marcador não altera `status: recuperacao-pendente` nem `publicar: false`. Apenas conteúdo integral recuperado ou texto novo aprovado em mudança própria poderá mudar esse estado.

## Risks / Trade-offs

- **[Renomeações rompem referências ocultas]** → mapear referências antes da migração, atualizar atomicamente e executar busca residual pelos caminhos antigos.
- **[Inventário se torna uma segunda fonte editorial]** → limitar o inventário a estado, proveniência e caminhos; fatos narrativos continuam nas fontes canônicas.
- **[Sumário-alvo parece produto disponível]** → documentar sua função e fazer o manifesto permanecer como única seleção de release.
- **[Validador acusa histórico intencional]** → excluir explicitamente histórico e campos de migração das regras de caminho ativo.
- **[Marcador renomeado parece recuperado]** → preservar front matter e registrar `caminho_anterior` sem alterar o estado de recuperação.
- **[Escopo cresce para reescrita]** → bloquear alterações narrativas e conferir que os marcadores movidos mantêm conteúdo equivalente.

## Migration Plan

1. Capturar contagens, hashes e referências atuais dos marcadores afetados.
2. Definir e documentar a arquitetura consolidada.
3. Evoluir o inventário e os verificadores antes das renomeações.
4. Mover o manifesto histórico e atualizar sua proveniência.
5. Executar as dez migrações de regras com preservação de conteúdo.
6. Atualizar `SUMMARY.md`, `regras/README.md`, metadados, documentação e referências internas.
7. Executar validação de recuperação, arquitetura, links, OpenSpec e materialização.
8. Confirmar 94 marcadores, 23 stubs e três documentos atualmente materializáveis.
9. Registrar a mudança em branch própria e revisar o diff por renomeações, não reescritas narrativas.

**Rollback:** restaurar os caminhos e documentos pelo commit anterior ou pela tag `recovery-baseline-v1`. O mapa de migração permitirá reverter cada renomeação sem inferência.

## Open Questions

Nenhuma decisão editorial de conteúdo é necessária para esta mudança. A seleção de antagonista, o conteúdo dos capítulos e a forma final do PDF permanecem para mudanças posteriores.
