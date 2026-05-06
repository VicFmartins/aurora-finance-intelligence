# Medidas DAX - Aurora Finance Intelligence

> Como usar: no Power BI Desktop, va em **Modelagem > Nova medida** e cole cada formula abaixo.
> Padrao adotado: nomes de medidas em minusculo, sem acento e com `_` separando as palavras.

## Observacoes importantes

- Os CSVs processados usam colunas em portugues, como `churn_flag`, `renda_mensal`, `saldo_atual` e `tempo_relacionamento`.
- A coluna `transacoes_limpo[tipo]` usa os valores `Debito`, `Credito`, `Pix` e `Transferencia`.
- A coluna `predicoes_churn[risco]` usa `Alto`, `Medio` e `Baixo`. O valor `Medio` fica sem acento.
- A tabela `metricas_modelo` deve ser importada do JSON como duas colunas: `metrica` e `valor`.

## 1. Visao geral

### total_clientes
```dax
total_clientes =
COUNTROWS(clientes_limpo)
```

### total_transacoes
```dax
total_transacoes =
COUNTROWS(transacoes_limpo)
```

### clientes_sem_churn
```dax
clientes_sem_churn =
CALCULATE(
    COUNTROWS(clientes_limpo),
    clientes_limpo[churn_flag] = 0
)
```

### clientes_com_churn
```dax
clientes_com_churn =
CALCULATE(
    COUNTROWS(clientes_limpo),
    clientes_limpo[churn_flag] = 1
)
```

### media_renda_mensal
```dax
media_renda_mensal =
AVERAGE(clientes_limpo[renda_mensal])
```

### media_saldo_atual
```dax
media_saldo_atual =
AVERAGE(clientes_limpo[saldo_atual])
```

### media_idade
```dax
media_idade =
AVERAGE(clientes_limpo[idade])
```

### media_tempo_relacionamento
```dax
media_tempo_relacionamento =
AVERAGE(clientes_limpo[tempo_relacionamento])
```

## 2. Financeiro

### volume_financeiro
```dax
volume_financeiro =
SUM(transacoes_limpo[valor])
```

### total_debito
```dax
total_debito =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "Debito"
)
```

### total_credito
```dax
total_credito =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "Credito"
)
```

### saldo_liquido
```dax
saldo_liquido =
[total_credito] - [total_debito]
```

### ticket_medio
```dax
ticket_medio =
DIVIDE(
    [volume_financeiro],
    [total_transacoes],
    0
)
```

### ticket_medio_por_cliente
```dax
ticket_medio_por_cliente =
DIVIDE(
    [volume_financeiro],
    [total_clientes],
    0
)
```

### media_saldo_clientes
```dax
media_saldo_clientes =
AVERAGE(clientes_limpo[saldo_atual])
```

### media_produtos_por_cliente
```dax
media_produtos_por_cliente =
AVERAGE(clientes_limpo[produtos_ativos])
```

### percentual_clientes_com_cartao
```dax
percentual_clientes_com_cartao =
DIVIDE(
    CALCULATE(
        COUNTROWS(clientes_limpo),
        clientes_limpo[tem_cartao_credito] = 1
    ),
    [total_clientes],
    0
)
```

### percentual_membros_ativos
```dax
percentual_membros_ativos =
DIVIDE(
    CALCULATE(
        COUNTROWS(clientes_limpo),
        clientes_limpo[membro_ativo] = 1
    ),
    [total_clientes],
    0
)
```

### meta_saldo
```dax
meta_saldo =
0
```

> Ajuste `meta_saldo` se a banca pedir uma meta operacional. Para a demo, manter zero deixa claro que o indicador mede saldo liquido observado.

### variacao_saldo
```dax
variacao_saldo =
[saldo_liquido] - [meta_saldo]
```

## 3. Churn e risco

### taxa_churn
```dax
taxa_churn =
DIVIDE(
    [clientes_com_churn],
    [total_clientes],
    0
)
```

### churn_por_pais
```dax
churn_por_pais =
DIVIDE(
    CALCULATE(
        COUNTROWS(clientes_limpo),
        clientes_limpo[churn_flag] = 1
    ),
    COUNTROWS(clientes_limpo),
    0
)
```

### probabilidade_media_churn
```dax
probabilidade_media_churn =
AVERAGE(predicoes_churn[prob_churn])
```

### clientes_churn_previsto
```dax
clientes_churn_previsto =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[predicao_churn] = 1
)
```

### taxa_churn_previsto
```dax
taxa_churn_previsto =
DIVIDE(
    [clientes_churn_previsto],
    [total_clientes],
    0
)
```

### clientes_alto_risco
```dax
clientes_alto_risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Alto"
)
```

### clientes_medio_risco
```dax
clientes_medio_risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Medio"
)
```

### clientes_baixo_risco
```dax
clientes_baixo_risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Baixo"
)
```

### percentual_clientes_alto_risco
```dax
percentual_clientes_alto_risco =
DIVIDE(
    [clientes_alto_risco],
    [total_clientes],
    0
)
```

## 4. Modelo ML

### roc_auc
```dax
roc_auc =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "roc_auc"
)
```

### precision_modelo
```dax
precision_modelo =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "precision"
)
```

### recall_modelo
```dax
recall_modelo =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "recall"
)
```

### f1_score_modelo
```dax
f1_score_modelo =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "f1_score"
)
```

### accuracy_modelo
```dax
accuracy_modelo =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "accuracy"
)
```

### baseline_churn_rate
```dax
baseline_churn_rate =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "baseline_churn_rate"
)
```

### threshold_usado
```dax
threshold_usado =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "threshold_used"
)
```

### top_feature_importancia
```dax
top_feature_importancia =
MAXX(
    TOPN(
        1,
        feature_importance,
        feature_importance[importance],
        DESC
    ),
    feature_importance[feature]
)
```

### resumo_modelo
```dax
resumo_modelo =
"AUC: " & FORMAT([roc_auc], "0.000") &
" | F1: " & FORMAT([f1_score_modelo], "0.000") &
" | Recall: " & FORMAT([recall_modelo], "0.000")
```

## 5. Consumo e comportamento

### top_categoria_por_gasto
```dax
top_categoria_por_gasto =
MAXX(
    TOPN(
        1,
        SUMMARIZE(
            transacoes_limpo,
            categorias_limpo[nome_categoria],
            "gasto_categoria", SUM(transacoes_limpo[valor])
        ),
        [gasto_categoria],
        DESC
    ),
    categorias_limpo[nome_categoria]
)
```

### gasto_medio_por_categoria
```dax
gasto_medio_por_categoria =
AVERAGEX(
    VALUES(categorias_limpo[nome_categoria]),
    CALCULATE(SUM(transacoes_limpo[valor]))
)
```

### transacoes_por_cliente
```dax
transacoes_por_cliente =
DIVIDE(
    [total_transacoes],
    [total_clientes],
    0
)
```

### volume_por_canal
```dax
volume_por_canal =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    ALLEXCEPT(transacoes_limpo, transacoes_limpo[canal])
)
```

### crescimento_mom
```dax
crescimento_mom =
VAR volume_atual = [volume_financeiro]
VAR volume_mes_anterior =
    CALCULATE(
        [volume_financeiro],
        PREVIOUSMONTH(transacoes_limpo[data])
    )
RETURN
DIVIDE(
    volume_atual - volume_mes_anterior,
    volume_mes_anterior,
    0
)
```

### volume_ytd
```dax
volume_ytd =
CALCULATE(
    [volume_financeiro],
    DATESYTD(transacoes_limpo[data])
)
```

## 6. Medidas de apoio para cards

### status_churn
```dax
status_churn =
SWITCH(
    TRUE(),
    [taxa_churn] > 0.25, "ALTO",
    [taxa_churn] > 0.15, "MEDIO",
    "BAIXO"
)
```

### status_modelo
```dax
status_modelo =
SWITCH(
    TRUE(),
    [roc_auc] >= 0.85, "EXCELENTE",
    [roc_auc] >= 0.75, "BOM",
    "ABAIXO DO ESPERADO"
)
```

## Formatos sugeridos

| Medida | Formato no Power BI |
| --- | --- |
| `taxa_churn`, `probabilidade_media_churn`, `precision_modelo`, `recall_modelo`, `baseline_churn_rate` | Porcentagem |
| `roc_auc`, `f1_score_modelo`, `accuracy_modelo`, `threshold_usado` | Numero decimal |
| `volume_financeiro`, `saldo_liquido`, `ticket_medio`, `media_renda_mensal` | Moeda |
| `total_clientes`, `total_transacoes`, `clientes_alto_risco` | Numero inteiro |

