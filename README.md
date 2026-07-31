# Instituto Atlas e a Tragédia de Belamar — árvore operacional recuperada

Esta pasta foi reconstruída em 31 de julho de 2026 a partir de:

- arquivos preservados na Biblioteca do Projeto;
- relatórios de materialização e sumários do projeto;
- o pacote interno de planejamento e continuidade gerado nesta conversa.

## Estado da recuperação

Esta não é uma cópia byte a byte do sistema de arquivos temporário do chat anterior. A Biblioteca permite recuperar o conteúdo integral de alguns arquivos, mas não montar automaticamente toda a pasta original.

Os arquivos com conteúdo integral recuperado permanecem em seus caminhos normais. Arquivos cujo conteúdo não pôde ser transferido integralmente foram representados por marcadores com `status: recuperacao-pendente` e `publicar: false`.

Consulte [RECUPERACAO.md](RECUPERACAO.md) e `recuperacao/inventario.json` antes de substituir qualquer marcador. A política de rastreamento, limpeza e restauração está em [ORGANIZACAO.md](ORGANIZACAO.md).

## Fontes de verdade

Quando o conteúdo integral estiver presente, a hierarquia editorial é:

1. `cenario/`, `campanha/`, `regras/` e `apendices/`;
2. `publicacao/fontes/`, apenas quando identificado como adaptação editorial aprovada;
3. `publicacao/conteudo/`, sempre gerado;
4. `build/`, sempre gerado;
5. `historico/`, somente consulta.

A pasta `desenvolvimento/` é interna e nunca entra na publicação.

## Arquitetura editorial

- `publicacao/manifest.yml` é o único manifesto operacional e seleciona cada origem e destino por lista positiva.
- `SUMMARY.md` representa a arquitetura-alvo das fontes e pode apontar para marcadores ainda não publicáveis.
- `publicacao/conteudo/SUMMARY.md` é gerado e representa somente os documentos da release atual.
- `publicacao/stubs/` guarda esqueletos internos; aventuras completas e aprovadas terão fonte em `campanha/aventuras/`.
- Manifestos e relatórios antigos permanecem em `historico/` e nunca controlam o build atual.

## Comandos

```bash
python tools/check_recovery.py
python tools/check_architecture.py
python tools/materialize_publication.py --sync-stubs --check
python tools/materialize_publication.py --check
python tools/materialize_publication.py
```
