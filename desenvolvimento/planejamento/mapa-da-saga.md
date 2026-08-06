# Mapa editorial da saga

> **Planejamento interno:** este grafo não integra o livro e não estabelece cânone por si só. As arestas mostram sucessão editorial, Marcos ou dependências; não impõem uma sequência de cenas nem um único resultado válido.

Documentos relacionados: [Arco I](../../campanha/arcos/arco-1/README.md), [Arco II](../../campanha/arcos/arco-2/README.md) e [Arco III](../../campanha/arcos/arco-3/README.md).

## Legenda

- **Fato fixo:** função já aprovada pela campanha.
- **Consequência condicional:** recebe o estado realmente produzido pelos jogadores.
- **Variável do Pacote:** depende do antagonista escolhido e não possui resposta padrão.
- **Lacuna editorial:** posição existente cuja função individual ainda precisa de aprovação.

```mermaid
flowchart TD
  classDef fixed fill:#174f73,color:#fff,stroke:#0b3048,stroke-width:2px
  classDef conditional fill:#fff3d6,color:#4a3410,stroke:#d59a24,stroke-width:2px
  classDef package fill:#eee6ff,color:#39225f,stroke:#7651a8,stroke-width:2px,stroke-dasharray:5 3
  classDef open fill:#f3f5f7,color:#52606d,stroke:#93a1ad,stroke-width:1px,stroke-dasharray:3 3
  classDef milestone fill:#e6f4ea,color:#173e25,stroke:#3b7a57,stroke-width:3px

  subgraph ARC1["Arco I — Rumo à Licença"]
    direction TB
    A01["Aventura 1<br/>Exame de Admissão"]:::fixed
    A02["Aventura 2<br/>Função a aprovar"]:::open
    A03["Aventura 3<br/>Função a aprovar"]:::open
    A04["Aventura 4<br/>Função a aprovar"]:::open
    A05["Aventura 5<br/>Função a aprovar"]:::open
    A06["Aventura 6<br/>Avaliação final do arco"]:::fixed
    A01 --> A02 --> A03 --> A04 --> A05 --> A06
  end

  M1(["Marco<br/>Licença provisória"]):::milestone
  A06 --> M1

  subgraph ARC2["Arco II — Chamados de Belamar"]
    direction TB
    A07["Aventura 7<br/>Função a aprovar"]:::open
    A08["Aventura 8<br/>Função a aprovar"]:::open
    A09["Aventura 9<br/>Função a aprovar"]:::open
    A10["Aventura 10<br/>Função a aprovar"]:::open
    A11["Aventura 11<br/>Função a aprovar"]:::open
    A12["Aventura 12<br/>Função a aprovar"]:::open
    A13["Aventura 13<br/>Função a aprovar"]:::open
    A14["Aventura 14<br/>Segunda operação de captura<br/>captura física condicional"]:::conditional
    A15["Aventura 15<br/>Consequências do estado real da 14"]:::conditional
    A16["Aventura 16<br/>Conclusão institucional do arco"]:::fixed
    A07 --> A08 --> A09 --> A10 --> A11 --> A12 --> A13 --> A14 --> A15 --> A16
  end

  M1 --> A07
  FIRST{"Primeira operação contra a Vanguarda<br/>posição entre 7 e 13 a aprovar"}:::open
  A07 -. dependência anterior à segunda operação .-> FIRST
  FIRST -.-> A14
  PKG{"Pacote de Antagonista<br/>sinais • Frentes • forças • contrajogo"}:::package
  PKG -. variáveis selecionadas .-> A07
  PKG -. variáveis selecionadas .-> A14
  M2(["Marco<br/>Licença definitiva estudantil"]):::milestone
  A16 --> M2

  subgraph ARC3["Arco III — O Retorno"]
    direction TB
    A17["Aventura 17<br/>Função a aprovar"]:::open
    A18["Aventura 18<br/>Função a aprovar"]:::open
    A19["Aventura 19<br/>Função a aprovar"]:::open
    A20["Aventura 20<br/>Função a aprovar"]:::open
    A21["Aventura 21<br/>Função a aprovar"]:::open
    A22["Aventura 22<br/>Função a aprovar"]:::open
    A23["Aventura 23<br/>Encerramento do Clarão artificial<br/>autoria sobre o legado"]:::fixed
    A17 --> A18 --> A19 --> A20 --> A21 --> A22 --> A23
  end

  M2 --> A17
  PKG -. mecanismo e vulnerabilidade .-> A17
  PKG -. clímax configurado .-> A23
  M3(["Marco final<br/>Nova geração decide o legado"]):::milestone
  A23 --> M3
```

## Estado de atualização

O Exame de Admissão é o primeiro piloto. Uma posição só deixa a classe de lacuna quando sua função recebe aprovação explícita. Escolher um Pacote não transforma resultados condicionais em resultados obrigatórios.
