# Organização e segurança da árvore

Este documento registra a política operacional para preservar e organizar a reconstrução de **Instituto Atlas e a Tragédia de Belamar**. Ele não integra o módulo publicado.

## Camadas

| Camada | Caminhos | Tratamento |
|---|---|---|
| Fontes canônicas | `cenario/`, `campanha/`, `regras/`, `apendices/` | fonte editável quando o arquivo possui conteúdo canônico integral |
| Recuperação pendente | arquivos com `status: recuperacao-pendente` | marcador não canônico e não publicável; preservar até decisão individual |
| Adaptação editorial | `publicacao/fontes/` | publicável somente quando aprovada e declarada no manifesto operacional |
| Planejamento interno | `desenvolvimento/` | preservar no Git; nunca materializar no produto |
| Stubs | `publicacao/stubs/` | preservar no Git; nunca publicar enquanto forem stubs |
| Histórico e auditoria | `historico/`, `recuperacao/`, `publicacao/fontes-legado-97/` | somente consulta; preservar até encerramento explícito da recuperação |
| Saídas geradas | `publicacao/conteudo/`, `build/` | descartar somente quando reproduzíveis |
| Assets | `assets/` | preservar fontes e estruturas, inclusive arquivos `.keep` |
| Especificações | `openspec/` | preservar propostas, especificações, designs e tarefas |

A hierarquia editorial normativa continua definida em `AGENTS.md`.

## Inventário protegido do baseline

Levantamento anterior à criação da política Git:

- marcadores `recuperacao-pendente`: **94**;
- stubs de aventuras: **23**;
- arquivos em `publicacao/fontes-legado-97/`: **97**;
- arquivos `.keep`: **6**;
- caches Python identificados: **2**;
- arquivos materializados em `publicacao/conteudo/`: **5**;
- arquivos em `build/`: **2**, incluindo `build/releases/.keep`.

Os cinco arquivos materializados e `build/relatorio-materializacao.md` foram regenerados por `tools/materialize_publication.py` com checksums idênticos aos anteriores. Por isso podem permanecer fora do Git. `build/releases/.keep` é estrutural e permanece rastreado.

## Limites da limpeza

Toda limpeza usa lista positiva. Nesta etapa, os únicos alvos descartáveis aprovados são:

- `tools/__pycache__/`;
- `publicacao/conteudo/`;
- arquivos gerados dentro de `build/`, preservando `build/releases/.keep`.

É proibido executar remoção global a partir da raiz, incluindo comandos como:

```text
find . -type d -empty -delete
find . ... -delete
```

Nenhuma limpeza genérica pode alcançar `.git/`, `openspec/`, `assets/`, fontes, marcadores, inventários, stubs ou `desenvolvimento/continuidade/`.

## Baseline e remoto

- branch protegida por procedimento: `main`;
- tag anotada de recuperação: `recovery-baseline-v1`;
- remoto confirmado: `git@github.com:filipeaguiar/atlas.git`;
- página: `https://github.com/filipeaguiar/atlas`;
- visibilidade confirmada pelo GitHub CLI: `PRIVATE`;
- commit de baseline: `2be4931136ecf572a9182896bd02b160993d172a`;
- `origin/main` e `recovery-baseline-v1` confirmados no mesmo commit.

O backup remoto foi verificado antes da limpeza. Nenhuma credencial foi armazenada neste documento.

## Restauração

Para restaurar um arquivo sem alterar a tag:

```bash
git restore --source recovery-baseline-v1 -- caminho/do/arquivo
```

Para comparar a organização com o baseline:

```bash
git diff recovery-baseline-v1...HEAD
```

Para criar uma árvore de inspeção sem substituir o trabalho atual:

```bash
git worktree add ../Atlas-baseline recovery-baseline-v1
```

Se uma organização já tiver sido registrada em commit, prefira revertê-la em novo commit. Não mova nem reescreva `recovery-baseline-v1`.

## Validações mínimas

```bash
python tools/check_recovery.py
python tools/materialize_publication.py --check
python tools/materialize_publication.py
```

O verificador de recuperação atual lê a quantidade de marcadores do inventário, mas não confirma individualmente a existência dos 94 caminhos. A contagem física deve ser verificada separadamente durante reorganizações.

## Limitações preexistentes registradas

A auditoria de referências encontrou cinco links quebrados em `regras/README.md`, causados pela divergência já conhecida entre a numeração modular recuperada e a numeração editorial:

- `01-convencoes-do-cenario.md`;
- `02-pontuacao-escala-e-progressao.md`;
- `03-testes-equipe-e-pa.md`;
- `04-objetivos-xp-e-marcos.md`;
- `06-configuracoes-modulares-e-encontros.md`.

A correção depende da consolidação da arquitetura das regras e não será resolvida silenciosamente nesta limpeza. A referência operacional do `README.md` ao inventário foi corrigida para o arquivo existente `recuperacao/inventario.json`.
