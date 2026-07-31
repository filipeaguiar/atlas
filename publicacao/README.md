# Publicação

A publicação usa uma única arquitetura operacional:

- `manifest.yml`: lista positiva atual, com fontes e destinos explícitos.

O manifesto recuperado da camada editorial de 97 documentos está preservado em `historico/publicacao/manifesto-publicacao-recuperado.yml` e não controla nenhuma ferramenta atual.

`fontes-legado-97/` contém apenas marcadores dos caminhos confirmados pelo relatório histórico. Esses marcadores têm `publicar: false` e não são materializados.

`stubs/` contém as 23 aventuras em desenvolvimento. A sincronização é feita por `tools/materialize_publication.py --sync-stubs`.

`conteudo/` é saída gerada e pode ser recriada. Seu `SUMMARY.md` lista somente os documentos ativos da release; o `SUMMARY.md` da raiz descreve a arquitetura-alvo das fontes.
