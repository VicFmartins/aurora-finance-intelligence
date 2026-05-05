# Resumo de Insights — Aurora Finance Intelligence
*Gerado automaticamente em 05/05/2026 01:10 a partir dos dados reais do projeto*

---

## 1. Visão Geral da Base

| Indicador | Valor |
|-----------|-------|
| **Total de clientes** | 10,000 |
| **Total de transações** | 267,255 |
| **Período das transações** | Jan/2024 a Apr/2025 |
| **Média de idade** | 38.9 anos |
| **Média de tempo de relacionamento** | 5.0 anos |

**Distribuição por país/estado:**
- França: 5,014 clientes (50.1%)
- Alemanha: 2,509 clientes (25.1%)
- Espanha: 2,477 clientes (24.8%)

**Distribuição por perfil de risco:**
- Conservador: 4,676 clientes (46.8%)
- Moderado: 3,654 clientes (36.5%)
- Arrojado: 1,670 clientes (16.7%)

---

## 2. Churn Real

| Indicador | Valor |
|-----------|-------|
| **Taxa de churn real (target Kaggle)** | **20.37%** |
| **Clientes que saíram (Exited=1)** | 2,037 |
| **Clientes ativos** | 7,963 |

**Taxa de churn por país:**
- Alemanha: 32.44%
- Espanha: 16.67%
- Franca: 16.15%

---

## 3. Volume Financeiro (Transações Sintéticas)

| Indicador | Valor |
|-----------|-------|
| **Volume financeiro total** | R$ 441,581,018.45 |
| **Ticket médio por transação** | R$ 1,652.28 |
| **Volume de créditos** | R$ 250,784,446.31 (56.8% do total) |
| **Volume de débitos** | R$ 89,359,592.14 (20.2% do total) |
| **Volume via Pix** | R$ 59,761,833.09 (13.5% do total) |
| **Média de renda mensal dos clientes** | R$ 8,371.51 |
| **Média de saldo atual dos clientes** | R$ 76,485.89 |

---

## 4. Top Categorias de Consumo

| Categoria | Volume Total | % do Total |
|-----------|-------------|-----------|
| **Investimentos** | R$ 75,291,990.84 | 17.1% |
| **Servicos Financeiros** | R$ 73,089,611.76 | 16.6% |
| **Saude** | R$ 43,297,714.88 | 9.8% |
| **Educacao** | R$ 43,055,012.84 | 9.8% |
| **Transporte** | R$ 42,978,287.38 | 9.7% |

> Investimentos e Serviços Financeiros dominam por terem tickets médios mais altos (~R$ 2.700–3.000).
> As categorias Essenciais (Alimentação, Moradia, Transporte, Saúde) têm volume similar, mas ticket menor (~R$ 1.340).

---

## 5. Predição de Churn (Modelo ML)

| Indicador | Valor |
|-----------|-------|
| **Clientes de ALTO risco** | **1,456 (14.6% da base)** |
| **Clientes de MÉDIO risco** | 1,080 (10.8% da base) |
| **Clientes de BAIXO risco** | 7,464 (74.6% da base) |
| **Probabilidade média de churn** | 28.45% |
| **Cliente com maior prob. de churn** | prob_churn = 98.97% |

**Threshold de classificação utilizado:** 0.40

---

## 6. Principais Features do Modelo

| # | Feature | Importância |
|---|---------|-------------|
| 1 | `numericas__idade` | 0.1605 |
| 2 | `numericas__produtos_ativos` | 0.0982 |
| 3 | `categoricas__perfil_risco_Conservador` | 0.0912 |
| 4 | `numericas__score_credito` | 0.0814 |
| 5 | `numericas__saldo_atual` | 0.0414 |
| 6 | `categoricas__perfil_risco_Moderado` | 0.0413 |
| 7 | `categoricas__perfil_risco_Arrojado` | 0.0356 |
| 8 | `numericas__razao_saldo_renda` | 0.0355 |
| 9 | `numericas__membro_ativo` | 0.0247 |
| 10 | `categoricas__estado_Alemanha` | 0.0220 |

**Interpretação dos top 3:**
1. **`idade`** (0.161): O fator mais determinante. Clientes mais velhos tendem a sair mais.
2. **`produtos_ativos`** (0.098): Menos produtos = maior risco de churn.
3. **`perfil_risco_Conservador`** (0.091): Perfil conservador está correlacionado ao churn.

---

## 7. Métricas do Modelo

| Métrica | Valor | Interpretação |
|---------|-------|---------------|
| **ROC-AUC** | **0.9288** | 🟢 Excelente (>0,90) |
| **Accuracy** | 0.8765 | 🟢 87,65% de acertos gerais |
| **Precision** | 0.6600 | 🟡 66% dos alertas são verdadeiros |
| **Recall** | 0.8108 | 🟢 Captura 81% dos churners reais |
| **F1 Score** | 0.7277 | 🟢 Bom equilíbrio Precision/Recall |
| **Threshold usado** | 0.40 | Otimizado para maximizar recall |
| **Taxa baseline (churn real)** | 20.37% | Taxa de referência sem modelo |

**Comparação de thresholds:**

| Threshold | Precision | Recall | F1 Score | Alert Rate |
|-----------|-----------|--------|----------|------------|
| 0.30 | 0.515 | 0.897 | 0.655 | 35.4% |
| 0.40 | 0.660 | 0.811 | 0.728 | 25.0% | ← **recomendado**
| 0.50 | 0.762 | 0.668 | 0.712 | 17.8% |

---

## 8. Recomendação Executiva

> **O modelo Aurora recomenda priorizar os 1,456 clientes de alto risco** (14.6% da base).
>
> Com Recall de **81%**, o modelo captura **4 em cada 5 clientes** que efetivamente iriam sair.
> A cada R$ 1 investido em retenção de clientes identificados, o retorno esperado é significativamente superior ao custo de reaquisiçãoo de clientes perdidos.
>
> **Próximo passo imediato:** Usar a coluna `recomendacao` de `predicoes_churn.csv` como script de abordagem para o time de CRM, priorizando os clientes com `prob_churn > 0.70`.

---

## 9. Fonte dos Dados

| Componente | Fonte |
|------------|-------|
| Base de clientes e churn | **Kaggle — Churn Modelling** (dataset público, 10.000 registros) |
| Transações financeiras | **Camada sintética** gerada pelo pipeline Aurora (`src/simulate_transactions.py`) |
| Modelo ML | **XGBoost** treinado via `src/train_model.py` |
| Predições | Geradas por `src/predict_churn.py` |

---

*Aurora Finance Intelligence — Resumo de Insights | Gerado em 05/05/2026 01:10*
