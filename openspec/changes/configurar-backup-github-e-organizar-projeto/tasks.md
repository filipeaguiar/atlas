## 1. Verificações prévias

- [x] 1.1 Verificar `gh auth status`, registrar o proprietário autenticado e confirmar acesso de criação de repositórios
- [x] 1.2 Consultar se o repositório `atlas` já existe no proprietário e interromper sem alterações em caso de colisão
- [x] 1.3 Inspecionar a árvore por tokens, chaves privadas, credenciais e arquivos locais sensíveis antes de adicionar arquivos ao Git
- [x] 1.4 Inventariar fontes preserváveis, marcadores, stubs, arquivos estruturais, caches e saídas geradas, registrando as contagens de baseline
- [x] 1.5 Confirmar que `publicacao/conteudo/` e `build/` são reproduzíveis a partir das fontes e ferramentas rastreadas antes de classificá-los como ignoráveis

## 2. Política de rastreamento e governança

- [x] 2.1 Criar uma política Git conservadora que ignore caches Python e saídas comprovadamente geradas, sem ignorar marcadores, legado, inventários, stubs, OpenSpec ou arquivos `.keep`
- [x] 2.2 Registrar a classificação das camadas da árvore e os limites de limpeza em documentação operacional
- [x] 2.3 Documentar a restauração de arquivos e da árvore a partir da tag `recovery-baseline-v1`
- [x] 2.4 Validar que nenhum arquivo preservável ficou ignorado ou ausente da seleção do baseline

## 3. Baseline Git local

- [x] 3.1 Renomear a branch inicial de `master` para `main`
- [x] 3.2 Adicionar os arquivos preserváveis e revisar integralmente a seleção antes do commit
- [x] 3.3 Criar o commit inicial de recuperação e confirmar que não há mudanças preserváveis não registradas
- [ ] 3.4 Criar a tag anotada `recovery-baseline-v1` apontando para o commit inicial

## 4. Backup privado no GitHub

- [ ] 4.1 Criar o repositório `atlas` com visibilidade privada no proprietário autenticado e configurar `origin` sem sobrescrever remoto existente
- [ ] 4.2 Enviar a branch `main` e a tag `recovery-baseline-v1` ao GitHub
- [ ] 4.3 Confirmar pelo GitHub CLI que a visibilidade é privada e que os SHAs remotos da branch e da tag correspondem ao baseline local
- [ ] 4.4 Registrar o endereço do remoto e a confirmação verificável do backup sem armazenar credenciais

## 5. Organização controlada

- [ ] 5.1 Criar uma branch dedicada à organização somente depois da confirmação do backup remoto
- [ ] 5.2 Remover por lista positiva apenas `tools/__pycache__/`, `publicacao/conteudo/` e `build/`, preservando qualquer conteúdo que a validação tenha identificado como único
- [ ] 5.3 Confirmar que os 94 marcadores, os 23 stubs, `publicacao/fontes-legado-97/`, arquivos `.keep`, OpenSpec e estruturas de continuidade permanecem preservados
- [ ] 5.4 Revisar o diff e bloquear qualquer remoção não prevista antes de registrar o commit de organização

## 6. Validação e publicação da branch

- [ ] 6.1 Executar o verificador de recuperação e registrar eventuais limitações que ele não detecta automaticamente
- [ ] 6.2 Validar o manifesto operacional e rematerializar os três documentos atualmente aprovados
- [ ] 6.3 Confirmar que nenhuma fonte de `desenvolvimento/`, `historico/`, `recuperacao/` ou `publicacao/stubs/` entrou em `publicacao/conteudo/`
- [ ] 6.4 Revisar estado Git, contagens protegidas e referências essenciais após a organização
- [ ] 6.5 Criar um commit separado para a organização e enviar sua branch ao remoto privado sem incorporá-la automaticamente a `main`
