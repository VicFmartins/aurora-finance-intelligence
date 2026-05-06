# Storytelling Power BI

## Objetivo

Transformar os artefatos da Aurora em um dashboard executivo claro, usando o dataset publico `Churn Modelling` enriquecido com a camada sintetica de transacoes.

## Base da narrativa

Na apresentacao, deixe claro:

- o churn vem do dataset `Churn Modelling` do Kaggle
- o campo `Exited` e o target
- `EstimatedSalary` foi convertido para renda mensal
- as transacoes foram simuladas porque o dataset publico nao possui historico por categoria

## Arquivos para importar

- `dados/processed/clientes_limpo.csv`
- `dados/processed/transacoes_limpo.csv`
- `dados/processed/categorias_limpo.csv`
- `dados/processed/base_modelagem.csv`
- `dados/outputs/predicoes_churn.csv`
- `dados/outputs/feature_importance.csv`
- `dados/outputs/threshold_analysis.csv` se existir

## Relacionamentos

- `clientes_limpo.cliente_id` com `transacoes_limpo.cliente_id`
- `categorias_limpo.categoria_id` com `transacoes_limpo.categoria_id`
- `clientes_limpo.cliente_id` com `predicoes_churn.cliente_id`

## Paginas do dashboard

1. `Visao Executiva`
2. `Comportamento Financeiro`
3. `Consumo e Categorias`
4. `Churn e Retencao`
5. `Modelo ML`

## Medidas DAX

```DAX
total_clientes =
COUNTROWS(clientes_limpo)

total_transacoes =
COUNTROWS(transacoes_limpo)

clientes_com_churn =
CALCULATE(
    COUNTROWS(clientes_limpo),
    clientes_limpo[churn_flag] = 1
)

volume_financeiro =
SUM(transacoes_limpo[valor])

total_debito =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "Debito"
)

total_credito =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "Credito"
)

ticket_medio =
DIVIDE([volume_financeiro], [total_transacoes], 0)

taxa_churn =
DIVIDE([clientes_com_churn], [total_clientes], 0)

clientes_alto_risco =
CALCULATE(
    DISTINCTCOUNT(predicoes_churn[cliente_id]),
    predicoes_churn[risco] = "Alto"
)

probabilidade_media_churn =
AVERAGE(predicoes_churn[prob_churn])

saldo_liquido =
[total_credito] - [total_debito]
```

## Mensagem que deve aparecer no painel

Use discretamente no dashboard:

`Base publica Kaggle + camada sintetica de transacoes`

## Prints para o GitHub

Salvar em `powerbi/screenshots/`:

1. `01_visao_executiva.png`
2. `02_comportamento_financeiro.png`
3. `03_consumo_categorias.png`
4. `04_churn_retencao.png`
5. `05_modelo_ml.png`

## Como explicar em 5 minutos

1. o pipeline usa o `Churn Modelling` como base real de churn
2. `Exited` e o target
3. enriquecemos a base com transacoes sinteticas para analise financeira
4. o Power BI organiza isso em paginas executivas
5. o modelo ranqueia risco e orienta retencao, nao automatiza a decisao final
