# Publicação

Esta reconstrução preserva duas arquiteturas:

- `manifesto.yml`: manifesto histórico da camada editorial de 97 documentos;
- `manifest.yml`: manifesto operacional atual, com fontes e destinos explícitos.

`fontes-legado-97/` contém apenas marcadores dos caminhos confirmados pelo relatório histórico. Esses marcadores têm `publicar: false` e não são materializados.

`stubs/` contém as 23 aventuras em desenvolvimento. A sincronização é feita por `tools/materialize_publication.py --sync-stubs`.

`conteudo/` é saída gerada e pode ser recriada.
