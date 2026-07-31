---
titulo: "Sistema interno de continuidade"
tipo: desenvolvimento-interno
status: ativo
publicar: false
schema_version: "1.0.0"
---

# Sistema interno de continuidade

Esta pasta mantém o estado acumulado da campanha entre as 23 aventuras. Ela existe para impedir que mortes, sequestros, descobertas, relações, pistas e consequências desapareçam quando uma aventura é escrita por outra pessoa ou em outro momento.

Nada nesta árvore deve aparecer no livro, no PDF ou em handouts para jogadores.

## Estrutura

```text
desenvolvimento/continuidade/
├── README.md
├── schema.yml
├── estado-inicial.yml
├── transicoes/
├── snapshots/
└── briefings/
```

- `schema.yml`: contrato dos dados de continuidade.
- `estado-inicial.yml`: snapshot imediatamente anterior à Aventura 1.
- `transicoes/NN.yml`: somente as mudanças produzidas pela Aventura NN.
- `snapshots/NN.yml`: estado consolidado após aplicar as transições até NN.
- `briefings/NN.md`: contexto mínimo entregue ao autor da Aventura NN.

## Regra de autoridade

O estado não cria cânone. Ele registra o que já foi definido nas fontes ou o que ocorreu em jogo.

Ordem de autoridade:

1. fontes canônicas em `cenario/`, `campanha/`, `regras/` e `apendices/`;
2. decisões explícitas aprovadas e incorporadas às fontes;
3. resultados efetivamente ocorridos na mesa;
4. transições e snapshots derivados desses resultados;
5. briefings gerados.

Quando o estado divergir de uma fonte canônica, a divergência deve ser registrada em `conflitos_de_fonte`; não se corrige silenciosamente nenhum dos lados.

## Separação obrigatória de informação

Cada verdade importante deve distinguir:

- `fato_real`: o que é verdadeiro no mundo;
- `conhecimento_publico`: aquilo que a sociedade acredita;
- `conhecimento_por_entidade`: aquilo que um NPC ou grupo sabe;
- `crenca_incorreta`: aquilo que alguém acredita, mas não é verdade;
- `decisao_pendente`: variável ainda não canonizada.

Um NPC não passa a conhecer um fato apenas porque o fato aparece no arquivo de estado.


## Decisões aprovadas

Decisões editoriais aprovadas devem ser registradas em `decisoes_aprovadas` e, quando alterarem a estrutura da campanha, também em um registro dentro de `desenvolvimento/decisoes/`.

A posição estrutural de um marco não transforma automaticamente seu resultado em cena obrigatória. Por exemplo, a segunda operação de captura ocorre na Aventura 14, mas a captura física continua condicional às ações dos personagens. O snapshot registra o ramo efetivamente ocorrido na mesa.

## IDs estáveis

Use IDs em minúsculas, sem acentos e com hífens:

```yaml
id: tomas-valenca
id: segredo-tomas-e-multiplex
id: pista-transmissao-final-solar
```

Depois de publicado em uma transição, um ID não deve ser renomeado sem migração explícita.

## Fluxo por aventura

1. Consolidar o snapshot anterior.
2. Gerar o briefing da aventura.
3. Escrever e jogar a aventura.
4. Registrar apenas mudanças em `transicoes/NN.yml`.
5. Validar referências e enumerações.
6. Aplicar a transição para gerar `snapshots/NN.yml`.
7. Gerar `briefings/NN+1.md`.
8. Revisar o texto público para remover linguagem de pipeline.

## Estados e transições

O estado físico de uma entidade usa enumerações, não frases vagas:

```yaml
estado_fisico: vivo
condicao: saudavel
disponibilidade: disponivel
```

Um sequestro deve alterar, no mínimo:

```yaml
estado_fisico: vivo
condicao: desconhecida
disponibilidade: sequestrado
localizacao:
  status: desconhecida
```

Uma descoberta deve apontar quem aprendeu o quê:

```yaml
conhecimento_adicionado:
  - entidade_id: prisma
    fato_id: identidade-do-tenente-principal
    confianca: confirmada
```

Uma morte deve registrar fonte e consequências, sem apagar o histórico anterior:

```yaml
mudancas_de_entidade:
  - entidade_id: exemplo
    estado_fisico: morto
    causa_evento_id: adv-08-evento-03
```

## Resultados condicionais

Aventuras não produzem um único resultado obrigatório. Uma transição pode conter alternativas mutuamente exclusivas, identificadas por `condicao_id`:

```yaml
resultados_condicionais:
  - condicao_id: resgate-bem-sucedido
    aplicar_quando: "o NPC foi retirado antes do colapso"
    mudancas: []
  - condicao_id: retirada-segura
    aplicar_quando: "a equipe reconheceu a escalada e solicitou retirada"
    mudancas: []
```

O snapshot consolidado deve conter somente o ramo que ocorreu na mesa.

## Pistas

Toda pista essencial deve registrar redundância e payoff:

```yaml
pistas:
  - id: pista-exemplo
    verdade_relacionada: fato-exemplo
    fontes_alternativas:
      - arquivo-antigo
      - testemunha
      - sensor
    acessada_pelos_pcs: false
    payoff_previsto: adv-19
```

Nenhuma verdade estrutural pode depender de uma única rolagem, cena ou NPC.

## Pacote de Antagonista

Antes da seleção, mantenha:

```yaml
pacote_antagonista:
  selecionado: null
  status: decisao_pendente
```

Depois da seleção:

- carregar apenas o Pacote escolhido;
- preencher mecanismo, Vestígios, Frentes, Tenente Principal e pistas específicas;
- não importar elementos de outros Pacotes sem aprovação explícita;
- preencher vínculos material, ideológico e operacional após conhecer os PCs.

## Proteção editorial

- Todos os arquivos desta pasta usam `publicar: false` quando possuem metadados.
- `desenvolvimento/` não deve aparecer em `publicacao/fontes/SUMMARY.md`.
- O materializador deve operar por lista positiva, nunca copiar a raiz inteira.
- Termos como `snapshot`, `pipeline`, `handoff`, `estado interno` e `briefing de continuidade` devem ser barrados na publicação, salvo uso ficcional explicitamente revisado.

## Validação mínima

Após incorporar estes arquivos ao projeto:

```bash
python tools/check_links.py
python tools/build_book.py
```

Enquanto não existir o compilador de continuidade, validar sintaxe YAML com:

```bash
python - <<'PY'
from pathlib import Path
import yaml
for path in Path('desenvolvimento/continuidade').glob('*.yml'):
    yaml.safe_load(path.read_text(encoding='utf-8'))
    print('OK', path)
PY
```
