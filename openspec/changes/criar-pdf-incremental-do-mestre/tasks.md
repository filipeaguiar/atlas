## 1. Fundação e contrato do manifesto

- [x] 1.1 Auditar fontes atualmente elegíveis, links locais, handouts existentes e disponibilidade do Chrome
- [x] 1.2 Definir e documentar schema do `publicacao/manifest.yml` para um único livro do Mestre
- [x] 1.3 Adicionar e bloquear dependência Python de renderização Markdown
- [x] 1.4 Criar template HTML e CSS inicial para impressão A4

## 2. Validação e materialização

- [x] 2.1 Implementar carregamento do manifesto, validação de campos e saneamento de versão e nome-base
- [x] 2.2 Implementar lista positiva, ordem estável e detecção de origens duplicadas
- [x] 2.3 Implementar confinamento às raízes permitidas e bloqueio das áreas internas, referências, stubs e derivados
- [x] 2.4 Implementar validação de front matter, estado canônico, publicabilidade, IDs e títulos
- [x] 2.5 Implementar validação específica de handouts e metadados de entrega
- [x] 2.6 Implementar varredura de links e recursos locais com comportamentos incremental e estrito
- [x] 2.7 Materializar fontes, sumário e documento combinado em `publicacao/conteudo/`
- [x] 2.8 Registrar hashes e digest determinístico do conjunto de entradas

## 3. Renderização do livro

- [x] 3.1 Converter Markdown materializado em HTML com tabelas, listas, notas e código
- [x] 3.2 Gerar capa, identificação de versão e sumário navegável
- [x] 3.3 Aplicar hierarquia visual, quebras de capítulo, tabelas, imagens e numeração de páginas
- [x] 3.4 Renderizar orientação do Mestre e página entregável de handouts no mesmo módulo
- [x] 3.5 Localizar Chrome por `CHROME_BIN` ou caminhos conhecidos e produzir PDF headless
- [x] 3.6 Validar código de saída e existência não vazia do HTML e PDF

## 4. Relatório e interface

- [x] 4.1 Gerar `build/relatorio-publicacao.json` com modo, versão, Chrome, fontes, hashes, avisos e artefatos
- [x] 4.2 Implementar CLI padrão incremental e opção `--strict`
- [x] 4.3 Garantir limpeza segura de saídas antigas antes de cada build
- [x] 4.4 Documentar manifesto, fluxo incremental, release estrita e ausência de edição pública

## 5. Primeira versão incremental

- [x] 5.1 Selecionar no manifesto inicial somente fontes individualmente revisadas e elegíveis
- [x] 5.2 Organizar seções iniciais de cenário, campanha, regras e handouts quando disponíveis
- [x] 5.3 Gerar `herdeiros-da-vanguarda-0.1.0-dev.1.pdf` e revisar capa, sumário e paginação
- [x] 5.4 Confirmar que links indisponíveis aparecem no relatório incremental sem ocultar pendências

## 6. Testes e entrega

- [x] 6.1 Testar seleção positiva, ordem, duplicatas, caminhos externos e raízes proibidas
- [x] 6.2 Testar metadados, estados, publicabilidade e recusa de referências completas
- [x] 6.3 Testar handouts integrados e ausência de qualquer PDF público ou exportação automática
- [x] 6.4 Testar diferenças entre modo incremental e estrito
- [x] 6.5 Testar materialização, digest, HTML, invocação do Chrome e relatório
- [x] 6.6 Executar testes, validação OpenSpec e build real incremental
- [x] 6.7 Revisar o diff e criar commit próprio sem incluir fontes externas ou conteúdo não aprovado
