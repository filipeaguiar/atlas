## 1. Segurança e catálogo

- [x] 1.1 Ignorar livros locais e índice derivado no Git
- [x] 1.2 Criar catálogo explícito com identificador, título, edição e caminho das referências
- [x] 1.3 Documentar que referências são externas, locais e não publicáveis

## 2. Indexação

- [x] 2.1 Implementar validação de catálogo e confinamento à raiz do projeto
- [x] 2.2 Implementar fragmentação Chonkie para OCR com IDs, hashes, offsets e páginas aproximadas
- [x] 2.3 Implementar banco SQLite FTS5 isolado e reconstrução atômica
- [x] 2.4 Criar CLI de indexação com resumo por livro

## 3. Busca

- [x] 3.1 Implementar consulta FTS5 com ranking BM25
- [x] 3.2 Limitar quantidade de resultados e tamanho de snippets
- [x] 3.3 Exibir título, edição, página aproximada, offsets e aviso de autoridade externa

## 4. Validação

- [x] 4.1 Testar catálogo, caminhos externos, links simbólicos e livros ausentes
- [x] 4.2 Testar determinismo, páginas aproximadas e isolamento do índice editorial
- [x] 4.3 Testar busca, ranking, limites e ausência de resultados
- [x] 4.4 Executar testes, validação OpenSpec e busca real nas referências locais
