# Arquitetura da Solucao

## Visao geral

A Aurora Finance Intelligence combina um dataset publico de churn bancario com uma camada sintetica de transacoes para ganhar profundidade analitica sem perder simplicidade operacional.

## Camada de origem

O projeto trabalha em dois modos:

1. **modo publico**  
   Usa `dados/raw/churn_modelling.csv` como origem principal de clientes e churn.

2. **modo fallback sintetico**  
   Se o arquivo nao existir, gera a base de clientes sinteticamente.

Essa decisao acontece dentro do proprio pipeline, sem mudar o comando `python -m src.pipeline`.

## Camada sintetica de transacoes

Mesmo usando o `Churn Modelling`, a Aurora continua gerando transacoes sinteticas porque o dataset publico nao possui:

- categorias de consumo
- historico temporal
- canais de transacao
- detalhamento financeiro por evento

Essa camada gera:

- `Alimentacao`
- `Moradia`
- `Transporte`
- `Saude`
- `Educacao`
- `Lazer`
- `Assinaturas`
- `Investimentos`
- `Servicos Financeiros`
- `Outros`

## Fluxo principal

```text
dados/raw/churn_modelling.csv (opcional)
    -> padronizacao Aurora
    -> camada sintetica de transacoes
    -> limpeza e tratamento
    -> base_modelagem
    -> Random Forest + threshold analysis
    -> CSVs, JSONs e model.pkl
    -> Power BI e app React estatico
```

## Decisoes importantes

- `Exited` e tratado como target de churn
- `EstimatedSalary` e convertido de anual para mensal
- `Geography` e usada como localizacao
- `Surname` e usado como nome do cliente no schema Aurora
- `CustomerId` e preservado em `customer_id_original`

## Por que essa arquitetura e boa para banca

- mostra uso de dado publico real
- mantem fallback sintetico para reproducao
- preserva SQL, EDA, ML e BI no mesmo projeto
- evita backend cloud obrigatorio
- continua AWS-ready com custo baixo
