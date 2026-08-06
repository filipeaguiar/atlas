# Curadoria de imagens geradas para 3DeT Victory

> Material interno. Nenhuma imagem desta pasta é canônica, publicável ou associada automaticamente a um NPC, inimigo ou capítulo.

## Origem

As imagens foram importadas individualmente dos arquivos `~/Downloads/imagens-3det-victory-parte-*.zip`. Os arquivos ZIP originais permaneceram intactos em `Downloads` e não foram copiados para o projeto.

- 9 pacotes encontrados: partes 02 a 10;
- a parte 01 não estava disponível;
- 7 pacotes íntegros;
- partes 04 e 08 truncadas, sem diretório central;
- 127 PNGs importados e validados por assinatura, chunks e CRC;
- 2 PNGs incompletos rejeitados;
- 7 duplicatas binárias exatas identificadas no inventário.

As imagens recuperadas das partes truncadas foram extraídas de cópias temporárias reparadas. A origem parcial e os arquivos rejeitados constam em `inventario.json`.

### Importação manual complementar

O lote `manual-01` registra imagens recebidas em `~/Imagens` após a curadoria inicial:

- 4 binários inéditos importados: Caio Ventura — Impacto, Malu Serrano — Rasura, Titã e Vetora;
- 3 cópias exatas já existentes restauradas: Colosso, Lia Vasconcelos — Atalho e Prisma;
- 131 registros totais após a importação.

A aprovação e a identidade foram registradas por solicitação explícita. As imagens continuam como material interno de curadoria e não se tornam automaticamente canônicas ou publicáveis.

## Estrutura

- `lotes/parte-XX/`: PNGs válidos, com nomes normalizados e IDs estáveis dentro do lote;
- `contatos/parte-XX.jpg`: folhas de contato para revisão rápida;
- `inventario.json`: proveniência, hashes, dimensões, duplicatas e problemas de origem;
- `curadoria.csv`: planilha editável de decisões.

Os diretórios binários `lotes/` e `contatos/` são ignorados pelo Git enquanto aguardam curadoria. Inventário, decisões e documentação podem ser versionados.

## Curadoria interativa no terminal

Em um terminal com suporte ao **Kitty graphics protocol**, execute:

```bash
uv run python tools/curate_images.py
```

### Uso dentro do Herdr

O Herdr desabilita gráficos por padrão. Acrescente a `~/.config/herdr/config.toml`:

```toml
[experimental]
kitty_graphics = true
```

Recarregue a configuração:

```bash
herdr server reload-config
```

O script detecta o Herdr e interrompe com instruções se essa opção continuar desativada.

Controles:

- `s`: marca a imagem como `aprovar` e avança;
- `l`: marca a imagem como `lixo` e avança; ela deixa de aparecer em todos os scripts, inclusive com `--all`;
- `espaço`: mantém a decisão atual e avança;
- `q`: encerra;
- `Ctrl+C`: encerra preservando todas as decisões já gravadas.

Por padrão, somente imagens pendentes são exibidas. Opções úteis:

```bash
# Revisar apenas um lote
uv run python tools/curate_images.py --batch 03

# Retomar em um ID
uv run python tools/curate_images.py --start parte-03-008

# Mostrar também imagens já decididas
uv run python tools/curate_images.py --all
```

Cada aprovação é gravada imediatamente em `curadoria.csv` e `inventario.json`.

## Identificação das imagens aprovadas

Depois da seleção visual, associe personagens somente às imagens aprovadas:

```bash
uv run python tools/identify_images.py
```

Digite parte do nome, use `↑`, `↓` ou `Tab` para escolher entre as sugestões e pressione `Enter` para salvar e avançar. Pressione `Enter` com o campo vazio para pular a imagem. Se o texto digitado não estiver na lista e nenhuma sugestão tiver sido selecionada, `Enter` adiciona o novo personagem a `personagens.txt` e usa esse nome. `Esc` encerra preservando as associações anteriores. A busca ignora diferenças entre maiúsculas, minúsculas e acentos.

Por padrão, o script mostra apenas aprovações sem identidade e elimina duplicatas binárias da fila. Ao identificar uma imagem, a mesma identidade é aplicada às suas cópias exatas.

Opções úteis:

```bash
# Retomar em uma imagem específica
uv run python tools/identify_images.py --start parte-06-008

# Revisar inclusive imagens já identificadas
uv run python tools/identify_images.py --all
```

As opções de autocomplete ficam em `personagens.txt`. Esse arquivo é uma lista interna editável e sua presença não associa automaticamente nenhum personagem a uma imagem.

## Fluxo de curadoria

1. Abra a folha de contato do lote ou use o script interativo.
2. Localize a imagem pelo ID de três dígitos.
3. Consulte a linha correspondente em `curadoria.csv`.
4. Preencha `identity` com o NPC, inimigo, grupo ou uso proposto.
5. Defina `decision` como:
   - `pendente`;
   - `aprovar`;
   - `rejeitar`;
   - `revisar`;
   - `duplicata`;
   - `lixo` — exclusão definitiva das filas interativas.
6. Registre em `notes` inconsistências visuais, texto embutido, artefatos, problemas de continuidade ou ajustes necessários.
7. Promova cada imagem aprovada individualmente para uma pasta de recursos da fonte correspondente, como `cenario/recursos/`, `campanha/aventuras/recursos/` ou `regras/recursos/`.
8. Ao promover, preserve o hash e registre a proveniência do ID de curadoria.

O nome original do arquivo funciona apenas como pista de triagem. Ele não confirma identidade, cânone, adequação ou direito de publicação.
