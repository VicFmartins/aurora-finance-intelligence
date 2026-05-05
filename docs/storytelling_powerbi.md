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

- `clientes.cliente_id` com `transacoes.cliente_id`
- `categorias.categoria_id` com `transacoes.categoria_id`
- `clientes.cliente_id` com `predicoes_churn.cliente_id`

## Paginas do dashboard

1. `Visao Executiva`
2. `Comportamento Financeiro`
3. `Consumo e Categorias`
4. `Churn e Retencao`
5. `Modelo ML`

## Medidas DAX

```DAX
Total Clientes =
DISTINCTCOUNT(clientes[cliente_id])

Total Transações =
COUNTROWS(transacoes)

Total Gastos =
CALCULATE(
    SUM(transacoes[valor]),
    transacoes[tipo] <> "Credito"
)

Ticket Médio =
DIVIDE([Total Gastos], [Total Transações])

Taxa Churn =
AVERAGE(clientes[churn_flag])

Clientes Alto Risco =
CALCULATE(
    DISTINCTCOUNT(predicoes_churn[cliente_id]),
    predicoes_churn[risco] = "Alto"
)

Probabilidade Média Churn =
AVERAGE(predicoes_churn[prob_churn])

Volume Financeiro =
SUM(transacoes[valor])

Saldo Líquido =
SUMX(
    transacoes,
    IF(transacoes[tipo] = "Credito", transacoes[valor], -transacoes[valor])
)
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
