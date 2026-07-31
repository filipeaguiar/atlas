## Why

A arquitetura editorial está consolidada, mas nove capítulos fundamentais de cenário ainda são apenas marcadores e o produto materializa somente uma introdução e dois documentos de regras. A próxima etapa deve reconstruir uma base de cenário utilizável e publicável a partir de fatos já aprovados, sem fingir que texto novo foi recuperado e sem resolver silenciosamente questões ainda abertas.

## What Changes

- Criar uma matriz interna de proveniência que classifique cada afirmação usada como fato fixo, explicação pública, limite deliberadamente aberto ou elaboração editorial sem novo fato.
- Reconstruir como texto novo aprovado os seguintes capítulos: visão geral, Extraordinários, sociedade heroica, Belamar e Atlas, programa de campo, Central de Operações, Vanguarda, memória pública da Tragédia e Instituto Atlas como hub jogável.
- Usar como base factual somente fontes integrais e aprovadas atualmente disponíveis, especialmente a introdução editorial canônica e as regras completas de Operações do Atlas.
- Usar documentos de desenvolvimento e continuidade apenas para localizar lacunas e conflitos; eles não poderão fundamentar afirmações publicadas.
- Preservar como abertas a origem do Clarão, a história global dos poderes, a estrutura da AHI, detalhes não aprovados de regulamentação e toda variável dependente de Pacote de Antagonista.
- Manter fora deste escopo Tomás em detalhe, corpo docente, alunos recorrentes, antagonistas, tenentes, segredos da campanha e aventuras.
- Diferenciar claramente a memória pública da Tragédia dos segredos reservados ao Mestre; a identidade de Tomás como Multiplex não será revelada nos capítulos públicos de cenário desta etapa.
- Substituir os nove marcadores somente após revisão de proveniência, registrando `origem: reescrita-aprovada` em vez de apresentar o texto como recuperação integral.
- Atualizar inventário, manifesto, sumário da release e validadores para refletir a redução auditável de 94 para 85 marcadores pendentes e a inclusão dos novos capítulos aprovados.
- Rematerializar a publicação ampliada, ainda sem gerar o PDF final.

## Capabilities

### New Capabilities

- `cenario-fundamental-publicavel`: Define o conteúdo, os limites de informação e os critérios editoriais dos nove capítulos fundamentais de cenário.
- `reescrita-canonica-controlada`: Define proveniência, revisão, transição de marcadores e proteção contra canonização silenciosa durante a reescrita de conteúdo ausente.

### Modified Capabilities

Nenhuma.

## Impact

- Nove arquivos em `cenario/`: `01` a `05`, `07`, `09` a `11`.
- `publicacao/manifest.yml`, cuja seção de cenário passará a incluir somente capítulos completos e aprovados.
- `recuperacao/inventario.json` e verificadores, com transição explícita de nove registros e nova contagem esperada de marcadores.
- `SUMMARY.md` permanece como arquitetura-alvo; `publicacao/conteudo/SUMMARY.md` passa a refletir a release ampliada.
- Nova documentação interna de proveniência em `desenvolvimento/`, sempre não publicável.
- Nenhum Pacote de Antagonista será escolhido, nenhuma questão aberta será resolvida e nenhum conteúdo de aventura será produzido.
