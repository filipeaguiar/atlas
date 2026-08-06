## 1. Fundação do site Hugo

- [x] 1.1 Criar a estrutura autoral em `publicacao/hugo/` sem conteúdo editorial duplicado
- [x] 1.2 Adicionar configuração-base do Hugo com idioma pt-BR, URLs relativas seguras e versão mínima suportada
- [x] 1.3 Criar layouts para página inicial, seção, capítulo, cabeçalho, rodapé e navegação sequencial
- [x] 1.4 Criar CSS responsivo com contraste, foco visível e navegação adaptável a telas estreitas

## 2. Materialização positiva

- [x] 2.1 Implementar `tools/generate_site.py` reutilizando `prepare_publication()` em modo estrito
- [x] 2.2 Gerar em `build/hugo/content/` as seções e páginas na ordem e com os metadados do manifesto
- [x] 2.3 Reescrever links entre documentos manifestados para rotas estáveis do Hugo
- [x] 2.4 Copiar para `build/hugo/static/recursos/` somente recursos locais alcançáveis e nomeados por hash
- [x] 2.5 Gerar dados de livro, versão, estado editorial e navegação sem incluir front matter interno desnecessário
- [x] 2.6 Executar Hugo Extended com `--baseURL` configurável e produzir exclusivamente `build/site/`
- [x] 2.7 Falhar com diagnóstico claro quando Hugo, manifesto, fonte, link ou recurso forem inválidos

## 3. Segurança editorial e testes

- [x] 3.1 Testar que apenas documentos manifestados aparecem no source tree e no site
- [x] 3.2 Testar recusa de fontes e recursos em todas as áreas proibidas
- [x] 3.3 Testar links internos e assets sob uma base URL com subdiretório de projeto
- [x] 3.4 Testar seções vazias, aviso de desenvolvimento e navegação anterior/próxima
- [x] 3.5 Adicionar auditoria negativa do artefato para caminhos, conteúdo de áreas excluídas e qualquer arquivo PDF
- [x] 3.6 Validar HTML essencial, responsividade estrutural e ausência de rolagem horizontal causada pelo layout
- [x] 3.7 Executar toda a suíte de testes e um build local estrito com Hugo 0.164.0

## 4. Documentação e comandos locais

- [x] 4.1 Documentar instalação do Hugo Extended e comando de geração local
- [x] 4.2 Documentar que o site é integralmente dirigido ao Mestre e publicamente acessível no Pages
- [x] 4.3 Documentar que aprovação de imagem na curadoria não equivale a publicação no site
- [x] 4.4 Atualizar `.gitignore` para manter `build/hugo/` e `build/site/` como saídas descartáveis

## 5. GitHub Actions e Pages

- [x] 5.1 Criar `.github/workflows/pages.yml` com gatilhos em `main` e `workflow_dispatch`
- [x] 5.2 Fixar Hugo Extended 0.164.0 e executar testes e build estrito no job sem permissão de escrita
- [x] 5.3 Obter a base URL de `actions/configure-pages` e usá-la no build Hugo
- [x] 5.4 Enviar somente `build/site/` com `actions/upload-pages-artifact`
- [x] 5.5 Implantar em job separado com `actions/deploy-pages`, ambiente e permissões mínimas
- [x] 5.6 Configurar concorrência do Pages e garantir que falhas de validação bloqueiem o deploy

## 6. Repositório remoto e primeira implantação

- [x] 6.1 Registrar a autorização explícita para substituir a `main` divergente de `filipeaguiar/atlas` e confirmar a visibilidade antes do Pages
- [x] 6.2 Configurar `filipeaguiar/atlas` como `origin` e buscar o estado remoto sem mesclá-lo às fontes locais
- [ ] 6.3 Após validação e commit, substituir a branch remota com `--force-with-lease` vinculado ao hash remoto observado
- [ ] 6.4 Configurar Pages para origem GitHub Actions e verificar compatibilidade da visibilidade com o plano da conta
- [ ] 6.5 Acionar e acompanhar o primeiro workflow com `gh`, corrigindo falhas do build sem relaxar as regras editoriais
- [ ] 6.6 Revisar o site implantado, seus assets, navegação, URL de subdiretório e ausência de áreas internas
