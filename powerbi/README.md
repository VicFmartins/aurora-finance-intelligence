# Power BI — Aurora Finance Intelligence
## Guia Completo de Montagem do Dashboard

> **Tempo estimado para montar do zero:** 2–3 horas  
> **Requisito:** Power BI Desktop (versão mai/2024 ou superior)

---

## 1. Arquivos que devem ser importados

Todos os arquivos estão em `dados/processed/` e `dados/outputs/`:

| Arquivo | Pasta | Tabela no PBI |
|---------|-------|----------------|
| `clientes_limpo.csv` | `dados/processed/` | `clientes_limpo` |
| `transacoes_limpo.csv` | `dados/processed/` | `transacoes_limpo` |
| `categorias_limpo.csv` | `dados/processed/` | `categorias_limpo` |
| `base_modelagem.csv` | `dados/processed/` | `base_modelagem` *(opcional — análise avançada)* |
| `predicoes_churn.csv` | `dados/outputs/` | `predicoes_churn` |
| `feature_importance.csv` | `dados/outputs/` | `feature_importance` |
| `threshold_analysis.csv` | `dados/outputs/` | `threshold_analysis` |
| `metricas_modelo.json` | `dados/outputs/` | `metricas_modelo` |

> **Nota sobre metricas_modelo.json:** Importar como JSON → transformar em tabela de pares chave-valor. Veja `power_query.md`.

---

## 2. Como importar os CSVs

1. Abra o Power BI Desktop
2. **Página Inicial → Obter Dados → Texto/CSV**
3. Navegue até `dados/processed/` e selecione `clientes_limpo.csv`
4. Na prévia, clique em **Transformar Dados** (não "Carregar" diretamente)
5. Aplique as transformações de tipo descritas em `power_query.md`
6. Clique em **Fechar e Aplicar**
7. Repita para cada arquivo da tabela acima

---

## 3. Aplicar o Tema Visual

1. Vá em **Exibição → Temas → Procurar Temas**
2. Selecione o arquivo `powerbi/tema_aurora.json`
3. O tema "Aurora Finance Intelligence" será aplicado a todas as páginas

---

## 4. Relacionamentos entre tabelas

Após importar, vá em **Exibição → Modelo** e crie:

| De | Para | Cardinalidade | Filtro |
|----|------|--------------|--------|
| `clientes_limpo[cliente_id]` | `transacoes_limpo[cliente_id]` | 1 : N | Simples → |
| `categorias_limpo[categoria_id]` | `transacoes_limpo[categoria_id]` | 1 : N | Simples → |
| `clientes_limpo[cliente_id]` | `predicoes_churn[cliente_id]` | 1 : 1 | Ambos ↔ |

> **IMPORTANTE:** `cliente_id` e `categoria_id` devem ser do tipo **Texto** nas duas pontas do relacionamento. Corrija no Power Query antes de criar o relacionamento se necessário.

Detalhes completos em `modelagem_dados.md`.

---

## 5. Tipos de dados esperados

| Tabela | Coluna | Tipo no Power BI |
|--------|--------|------------------|
| `clientes_limpo` | `cliente_id` | Texto |
| `clientes_limpo` | `churn_flag` | Número Inteiro |
| `clientes_limpo` | `renda_mensal` | Número Decimal |
| `clientes_limpo` | `saldo_atual` | Número Decimal |
| `clientes_limpo` | `data_cadastro` | Data |
| `transacoes_limpo` | `cliente_id` | Texto |
| `transacoes_limpo` | `categoria_id` | Texto |
| `transacoes_limpo` | `data` | Data |
| `transacoes_limpo` | `valor` | Número Decimal |
| `predicoes_churn` | `cliente_id` | Texto |
| `predicoes_churn` | `prob_churn` | Número Decimal |
| `predicoes_churn` | `predicao_churn` | Número Inteiro |
| `predicoes_churn` | `risco` | Texto |
| `feature_importance` | `importance` | Número Decimal |
| `threshold_analysis` | `threshold` | Número Decimal |
| `threshold_analysis` | `precision` | Número Decimal |
| `threshold_analysis` | `recall` | Número Decimal |
| `threshold_analysis` | `f1_score` | Número Decimal |

---

## 6. Criar tabela de medidas DAX

1. Vá em **Modelagem → Inserir Dados**
2. Crie uma tabela chamada `_Medidas` com uma coluna `Placeholder` = `1`
3. Após carregar, crie todas as medidas nessa tabela (ver `medidas_dax.md`)
4. Delete a coluna `Placeholder`

---

## 7. Páginas do Dashboard

| # | Nome da Página |
|---|----------------|
| 1 | Visão Executiva |
| 2 | Consumo e Comportamento Financeiro |
| 3 | Churn e Retenção |
| 4 | Modelo ML |
| 5 | Storytelling Executivo |

---

## 8. Visuais por página (resumo)

**Página 1 — Visão Executiva**
- 5 Cards KPI: Total Clientes (10.000), Taxa Churn (20,37%), Volume Financeiro (R$ 441,6M), Clientes Alto Risco (1.456), Prob. Média Churn (28,45%)
- Gráfico de linhas: Evolução mensal (`ano_mes` × `Volume Financeiro`)
- Gráfico de barras: Volume por estado (`estado`)
- Gráfico de rosca: Distribuição de risco Churn (Alto / Médio / Baixo)
- Gráfico de barras horizontal: Top categorias por volume

**Página 2 — Consumo e Comportamento Financeiro**
- Barras: Gastos por categoria (`nome_categoria` × `Volume Financeiro`)
- Barras: Ticket médio por canal (`canal` × `Ticket Médio`)
- Área empilhada: Crédito vs Débito vs Pix vs Transferência por mês
- Matriz: `perfil_risco` × `nome_categoria` com `Volume Financeiro`

**Página 3 — Churn e Retenção**
- Barras: Clientes por faixa de risco (Alto / Médio / Baixo)
- Tabela: Top 20 clientes por `prob_churn` (nome, estado, perfil, prob, recomendação)
- Card: Probabilidade Média Churn (28,45%)
- Segmentadores: `estado`, `perfil_risco`, `risco`

**Página 4 — Modelo ML**
- Cards: ROC-AUC (0,929), Precision (0,660), Recall (0,811), F1 Score (0,728), Threshold (0,40)
- Barras horizontal: Feature Importance top 10 (`feature` × `importance`)
- Tabela: Threshold Analysis (threshold × precision × recall × f1 × alert_rate)
- Linhas: Trade-off Precision vs Recall por threshold

**Página 5 — Storytelling Executivo**
- Caixas de texto: Problema, Solução, Arquitetura, Insights, Impacto, Próximos Passos
- Imagens de `reports/figuras/` inseridas como imagem estática

---

## 9. Principais medidas DAX

```dax
total_clientes = COUNTROWS(clientes_limpo)
taxa_churn = DIVIDE([clientes_com_churn], [total_clientes], 0)
volume_financeiro = SUM(transacoes_limpo[valor])
ticket_medio = DIVIDE([volume_financeiro], [total_transacoes], 0)
clientes_alto_risco = CALCULATE(COUNTROWS(predicoes_churn), predicoes_churn[risco] = "Alto")
probabilidade_media_churn = AVERAGE(predicoes_churn[prob_churn])
roc_auc = CALCULATE(MAX(metricas_modelo[valor]), metricas_modelo[metrica] = "roc_auc")
```

Ver todas as medidas em `medidas_dax.md`.

---

## 10. Filtros e segmentadores recomendados

| Segmentador | Campo | Páginas |
|-------------|-------|---------|
| Estado/País | `clientes_limpo[estado]` | 1, 2, 3 |
| Perfil de Risco | `clientes_limpo[perfil_risco]` | 1, 2, 3 |
| Faixa de Risco Churn | `predicoes_churn[risco]` | 3 |
| Período | `transacoes_limpo[data]` | 2 |
| Tipo de Transação | `transacoes_limpo[tipo]` | 2 |
| Canal | `transacoes_limpo[canal]` | 2 |

> Para sincronizar segmentadores entre páginas: **Exibição → Sincronizar Segmentações de Dados**

---

## 11. Como salvar screenshots

Após montar cada página, pressione `Win + Shift + S` e salve em `powerbi/screenshots/`:

```
powerbi/screenshots/01_visao_executiva.png
powerbi/screenshots/02_consumo_comportamento.png
powerbi/screenshots/03_churn_retencao.png
powerbi/screenshots/04_modelo_ml.png
powerbi/screenshots/05_storytelling_executivo.png
```

Veja checklist detalhado em `checklist_screenshots.md`.

---

## 12. Screenshots finais incluidos

Os prints finais do painel ja estao salvos como evidencia visual da camada de BI:

| Pagina | Screenshot |
|--------|------------|
| Visao Executiva | `powerbi/screenshots/01_visao_executiva.png` |
| Consumo e Comportamento Financeiro | `powerbi/screenshots/02_consumo_comportamento.png` |
| Churn e Retencao | `powerbi/screenshots/03_churn_retencao.png` |
| Modelo ML | `powerbi/screenshots/04_modelo_ml.png` |
| Storytelling Executivo | `powerbi/screenshots/05_storytelling_executivo.png` |

Esses arquivos podem ser usados no README do GitHub, na apresentacao e como comprovacao de que o Power BI foi construido sobre os outputs do pipeline.

---

## 13. Checklist final

- [ ] Tema Aurora aplicado (`tema_aurora.json`)
- [ ] 8 fontes importadas (7 CSV + 1 JSON)
- [ ] 3 relacionamentos criados corretamente no modelo
- [ ] Tabela `_Medidas` com todas as medidas DAX
- [ ] 5 páginas criadas e nomeadas
- [ ] Segmentadores sincronizados entre páginas
- [ ] Títulos preenchidos em cada visual
- [ ] Cards KPI validados com os números reais
- [ ] 5 screenshots tirados e salvos em `powerbi/screenshots/`
- [ ] Arquivo salvo como `powerbi/aurora_finance_intelligence.pbix`

---

## Upload Express no frontend

A aba `Analise Expressa` do app React permite upload local de CSV e gera uma leitura rapida de risco diretamente no navegador. Essa camada e complementar:

- nao substitui o Power BI oficial
- nao altera os CSVs gerados pelo pipeline
- nao envia planilhas para servidor
- ajuda a demonstrar a Aurora com uma base do avaliador ou uma base de teste

Para a entrega de BI, continue usando os arquivos listados neste guia e o modelo Power BI salvo em `powerbi/aurora_finance_intelligence.pbix`.

---

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| `medidas_dax.md` | Todas as fórmulas DAX |
| `modelagem_dados.md` | Relacionamentos e cardinalidade |
| `layout_dashboard.md` | Layout detalhado das 5 páginas |
| `tema_aurora.json` | Tema visual dark fintech |
| `power_query.md` | Transformações Power Query / M |
| `checklist_screenshots.md` | Guia de screenshots |
| `roteiro_demo_powerbi.md` | Roteiro de fala de 1 minuto |
| `resumo_insights.md` | Insights numéricos reais |

---

*Aurora Finance Intelligence — Camada Power BI*
