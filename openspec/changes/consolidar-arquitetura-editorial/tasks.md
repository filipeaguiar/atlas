## 1. Preparação e baseline da migração

- [x] 1.1 Criar branch dedicada a partir de `main` atualizada e confirmar estado Git limpo exceto pelos artefatos desta mudança
- [x] 1.2 Registrar contagens, caminhos, status e hashes dos 94 marcadores, 23 stubs e dez marcadores de regras que serão renumerados
- [x] 1.3 Mapear todas as referências ativas aos dois manifestos e aos dez caminhos antigos de regras antes de alterar arquivos
- [x] 1.4 Criar mapa auditável das dez migrações de regras com caminho anterior, caminho atual e motivo editorial

## 2. Arquitetura e manifesto único

- [x] 2.1 Documentar em `AGENTS.md`, `README.md` e `ORGANIZACAO.md` a árvore definitiva, a autoridade de cada camada e o destino futuro das aventuras completas
- [x] 2.2 Documentar `SUMMARY.md` como sumário-alvo das fontes e `publicacao/conteudo/SUMMARY.md` como sumário gerado da release
- [x] 2.3 Mover `publicacao/manifesto.yml` para `historico/publicacao/` com nome histórico inequívoco e atualizar sua proveniência no inventário
- [x] 2.4 Atualizar `publicacao/README.md` e comandos operacionais para reconhecer apenas `publicacao/manifest.yml` como manifesto ativo
- [x] 2.5 Confirmar que nenhuma ferramenta ou documentação operacional continua tratando o manifesto histórico como entrada ativa

## 3. Inventário editorial verificável

- [x] 3.1 Evoluir `recuperacao/inventario.json` com versão de esquema e registros de caminho, classe, estado, status esperado, publicabilidade, existência e proveniência
- [x] 3.2 Registrar no inventário os caminhos anteriores e atuais das regras sem alterar seu estado de recuperação
- [x] 3.3 Atualizar `tools/check_recovery.py` para confrontar registros pendentes com arquivos físicos e front matter
- [x] 3.4 Fazer o verificador detectar marcadores físicos não inventariados, registros ausentes, stubs divergentes e contagens protegidas alteradas
- [x] 3.5 Manter as verificações de DEC-001 e separar avisos informativos de erros bloqueantes

## 4. Migração canônica das regras

- [x] 4.1 Mover os cinco capítulos gerais pendentes para `01-convencoes`, `02-pontuacao-escala-e-progressao`, `03-testes-equipe-e-pa`, `04-objetivos-xp-e-marcos` e `06-configuracoes-modulares-e-encontros`
- [x] 4.2 Mover as fichas pendentes dos tenentes e alunos para a sequência editorial `07` a `11`
- [x] 4.3 Confirmar que `regras/05-operacoes-do-atlas.md` permaneceu intacto e que todos os dez marcadores movidos conservaram conteúdo, status e publicabilidade
- [x] 4.4 Atualizar `regras/README.md`, `SUMMARY.md`, metadados editoriais e referências internas para os caminhos canônicos
- [x] 4.5 Buscar referências residuais e garantir que caminhos antigos apareçam somente em histórico ou no mapa explícito de migração

## 5. Validação de arquitetura e links

- [x] 5.1 Criar verificador de links Markdown locais para fontes modulares, adaptações editoriais e documentação operacional, com exclusões explícitas para histórico e saídas geradas
- [x] 5.2 Validar coerência entre manifesto, inventário e front matter, incluindo existência da fonte, publicabilidade e status
- [x] 5.3 Validar destinos duplicados, raízes proibidas e ausência de caminhos editoriais antigos em referências ativas
- [x] 5.4 Garantir que os verificadores retornem código diferente de zero para erros e apresentem origem e destino de cada divergência
- [x] 5.5 Integrar os novos comandos de validação à documentação operacional sem incluir notas de pipeline no produto

## 6. Validação final

- [x] 6.1 Executar validações sintáticas de YAML e JSON e a validação estrita do OpenSpec
- [x] 6.2 Executar os verificadores de recuperação, arquitetura e links e corrigir todas as falhas ativas
- [x] 6.3 Validar o manifesto e rematerializar os três documentos atualmente aprovados
- [x] 6.4 Confirmar 94 marcadores, 23 stubs, nenhum conteúdo interno materializado e nenhum link ativo quebrado
- [x] 6.5 Revisar o diff para comprovar que as regras foram renomeadas sem reescrita narrativa e que nenhum fato novo foi canonizado
- [x] 6.6 Remover novamente saídas geradas, registrar a consolidação em commit próprio e enviar a branch ao repositório privado
