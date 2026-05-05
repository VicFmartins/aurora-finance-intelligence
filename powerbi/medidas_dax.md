# Medidas DAX — Aurora Finance Intelligence

> **Como usar:** No Power BI Desktop, vá em **Modelagem → Nova Medida** e cole cada fórmula abaixo.
> Todas as medidas devem ser criadas em uma tabela chamada `_Medidas` (crie uma tabela vazia via **Inserir Dados** com apenas uma coluna chamada `Placeholder` e delete a coluna depois).

---

## 1. Visão Geral

### Total Clientes
```dax
Total Clientes =
COUNTROWS(clientes_limpo)
```

### Total Transações
```dax
Total Transações =
COUNTROWS(transacoes_limpo)
```

### Clientes Ativos (sem churn)
```dax
Clientes Ativos =
CALCULATE(
    COUNTROWS(clientes_limpo),
    clientes_limpo[Exited] = 0
)
```

### Clientes com Churn
```dax
Clientes com Churn =
CALCULATE(
    COUNTROWS(clientes_limpo),
    clientes_limpo[Exited] = 1
)
```

### Média de Renda Mensal
```dax
Média de Renda Mensal =
AVERAGE(clientes_limpo[EstimatedSalary])
```

### Média de Saldo Atual
```dax
Média de Saldo Atual =
AVERAGE(clientes_limpo[Balance])
```

### Média de Idade
```dax
Média de Idade =
AVERAGE(clientes_limpo[Age])
```

### Média de Tenure (Anos de Relacionamento)
```dax
Média Tenure =
AVERAGE(clientes_limpo[Tenure])
```

---

## 2. Financeiro

### Volume Financeiro Total
```dax
Volume Financeiro =
SUM(transacoes_limpo[valor])
```

### Total Gastos (Débitos)
```dax
Total Gastos =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "debito"
)
```

### Total Créditos
```dax
Total Créditos =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    transacoes_limpo[tipo] = "credito"
)
```

### Saldo Líquido
```dax
Saldo Líquido =
[Total Créditos] - [Total Gastos]
```

### Ticket Médio por Transação
```dax
Ticket Médio =
DIVIDE(
    [Volume Financeiro],
    [Total Transações],
    0
)
```

### Ticket Médio por Cliente
```dax
Ticket Médio por Cliente =
DIVIDE(
    [Volume Financeiro],
    [Total Clientes],
    0
)
```

### Média de Saldo dos Clientes
```dax
Média Saldo Clientes =
AVERAGE(clientes_limpo[Balance])
```

### Produtos por Cliente (Média)
```dax
Média Produtos por Cliente =
AVERAGE(clientes_limpo[NumOfProducts])
```

### % Clientes com Cartão de Crédito
```dax
% Clientes com Cartão =
DIVIDE(
    CALCULATE(COUNTROWS(clientes_limpo), clientes_limpo[HasCrCard] = 1),
    [Total Clientes],
    0
)
```

### % Clientes Membros Ativos
```dax
% Membros Ativos =
DIVIDE(
    CALCULATE(COUNTROWS(clientes_limpo), clientes_limpo[IsActiveMember] = 1),
    [Total Clientes],
    0
)
```

---

## 3. Churn

### Taxa de Churn
```dax
Taxa Churn =
DIVIDE(
    [Clientes com Churn],
    [Total Clientes],
    0
)
```

### Taxa de Churn % (Formatada)
```dax
Taxa Churn % =
FORMAT([Taxa Churn], "0.00%")
```

### Churn por Geografia
```dax
Churn por País =
CALCULATE(
    DIVIDE(
        COUNTROWS(FILTER(clientes_limpo, clientes_limpo[Exited] = 1)),
        COUNTROWS(clientes_limpo),
        0
    )
)
```

### Probabilidade Média de Churn
```dax
Probabilidade Média Churn =
AVERAGE(predicoes_churn[prob_churn])
```

### Probabilidade Média Churn % (Formatada)
```dax
Prob Média Churn % =
FORMAT([Probabilidade Média Churn], "0.00%")
```

### Clientes com Churn Previsto
```dax
Clientes Churn Previsto =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[churn_flag] = 1
)
```

### Taxa Churn Previsto
```dax
Taxa Churn Previsto =
DIVIDE(
    [Clientes Churn Previsto],
    [Total Clientes],
    0
)
```

---

## 4. Risco

### Clientes Alto Risco
```dax
Clientes Alto Risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Alto"
)
```

### Clientes Médio Risco
```dax
Clientes Médio Risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Médio"
)
```

### Clientes Baixo Risco
```dax
Clientes Baixo Risco =
CALCULATE(
    COUNTROWS(predicoes_churn),
    predicoes_churn[risco] = "Baixo"
)
```

### % Clientes Alto Risco
```dax
% Clientes Alto Risco =
DIVIDE(
    [Clientes Alto Risco],
    [Total Clientes],
    0
)
```

### % Clientes Médio Risco
```dax
% Clientes Médio Risco =
DIVIDE(
    [Clientes Médio Risco],
    [Total Clientes],
    0
)
```

### % Clientes Baixo Risco
```dax
% Clientes Baixo Risco =
DIVIDE(
    [Clientes Baixo Risco],
    [Total Clientes],
    0
)
```

### Risco Formatado (Para Cards)
```dax
Alto Risco Formatado =
FORMAT([Clientes Alto Risco], "#,##0") & " clientes"
```

---

## 5. Modelo ML

### ROC-AUC
```dax
ROC-AUC =
MAXX(
    FILTER(metricas_modelo, metricas_modelo[metrica] = "roc_auc"),
    metricas_modelo[valor]
)
```

> **Alternativa:** Se `metricas_modelo` for importada como uma tabela simples de chave-valor:
```dax
ROC-AUC =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "roc_auc"
)
```

### Precision
```dax
Precision =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "precision"
)
```

### Recall
```dax
Recall =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "recall"
)
```

### F1 Score
```dax
F1 Score =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "f1_score"
)
```

### Accuracy
```dax
Accuracy =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "accuracy"
)
```

### Threshold Usado
```dax
Threshold Usado =
CALCULATE(
    MAX(metricas_modelo[valor]),
    metricas_modelo[metrica] = "threshold"
)
```

> **Nota sobre metricas_modelo:** O arquivo `metricas_modelo.json` deve ser importado via Power Query e transformado em tabela de duas colunas: `metrica` (texto) e `valor` (decimal). Veja `power_query.md` para instruções detalhadas.

### Feature Importance Máxima
```dax
Top Feature Importância =
MAXX(
    TOPN(1, feature_importance, feature_importance[importance], DESC),
    feature_importance[feature]
)
```

### Score Médio do Modelo (Resumo)
```dax
Score Resumo Modelo =
"AUC: " & FORMAT([ROC-AUC], "0.000") &
" | F1: " & FORMAT([F1 Score], "0.000") &
" | Recall: " & FORMAT([Recall], "0.000")
```

---

## 6. Consumo (Transações)

### Top Categoria por Gasto
```dax
Top Categoria por Gasto =
CALCULATE(
    MAXX(
        TOPN(1,
            SUMMARIZE(
                transacoes_limpo,
                categorias_limpo[nome_categoria],
                "GastoCategoria", SUM(transacoes_limpo[valor])
            ),
            [GastoCategoria], DESC
        ),
        categorias_limpo[nome_categoria]
    )
)
```

### Gasto Médio por Categoria
```dax
Gasto Médio por Categoria =
AVERAGEX(
    VALUES(categorias_limpo[nome_categoria]),
    CALCULATE(SUM(transacoes_limpo[valor]))
)
```

### Transações por Cliente (Média)
```dax
Transações por Cliente =
DIVIDE(
    [Total Transações],
    [Total Clientes],
    0
)
```

### Volume por Canal
```dax
Volume por Canal =
CALCULATE(
    SUM(transacoes_limpo[valor]),
    ALLEXCEPT(transacoes_limpo, transacoes_limpo[canal])
)
```

### Crescimento MoM (Mês a Mês)
```dax
Crescimento MoM =
VAR VolumeAtual = [Volume Financeiro]
VAR VolumeMesAnterior =
    CALCULATE(
        [Volume Financeiro],
        PREVIOUSMONTH(transacoes_limpo[data])
    )
RETURN
DIVIDE(
    VolumeAtual - VolumeMesAnterior,
    VolumeMesAnterior,
    0
)
```

### Evolução Acumulada (YTD)
```dax
Volume YTD =
CALCULATE(
    [Volume Financeiro],
    DATESYTD(transacoes_limpo[data])
)
```

---

## 7. Medidas Auxiliares (KPI Coloridos)

### Semáforo Churn (Texto)
```dax
Status Churn =
SWITCH(
    TRUE(),
    [Taxa Churn] > 0.25, "🔴 ALTO",
    [Taxa Churn] > 0.15, "🟡 MÉDIO",
    "🟢 BAIXO"
)
```

### Semáforo ROC-AUC
```dax
Status Modelo =
SWITCH(
    TRUE(),
    [ROC-AUC] >= 0.85, "🟢 EXCELENTE",
    [ROC-AUC] >= 0.75, "🟡 BOM",
    "🔴 ABAIXO DO ESPERADO"
)
```

### Variação Saldo vs Meta
```dax
Variação Saldo =
[Saldo Líquido] - 0  -- substitua 0 pela meta definida
```

---

## Dicas de Formatação

| Medida | Formato Sugerido |
|--------|-----------------|
| Taxa Churn | Porcentagem (0.00%) |
| ROC-AUC, Precision, Recall, F1 | Número Decimal (0.000) |
| Volume Financeiro, Saldo | Moeda (R$ #,##0.00) |
| Total Clientes, Transações | Inteiro (#,##0) |
| Probabilidade Churn | Porcentagem (0.0%) |
| Ticket Médio | Moeda (R$ #,##0.00) |

---

*Gerado automaticamente para o projeto Aurora Finance Intelligence*
