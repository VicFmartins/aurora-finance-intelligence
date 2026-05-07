# Auditoria Final - Aurora Finance Intelligence

**Data:** 06 de maio de 2026
**Projeto:** Aurora Finance Intelligence
**Status final:** pronto para banca, GitHub e apresentação.

## 1. Panorama Geral

A Aurora Finance Intelligence está estruturada como um projeto completo de hackathon de dados. A entrega combina pipeline Python, SQL, notebooks didáticos, Machine Learning, Power BI, documentação técnica e um app React estático como diferencial de produto.

O projeto usa o dataset público `Churn Modelling` do Kaggle quando `dados/raw/churn_modelling.csv` existe. Caso o arquivo não esteja disponível, o pipeline mantém fallback sintético e continua executando com `python -m src.pipeline`.

## 2. Evidências Técnicas Validadas

- Pipeline Python em `src/`.
- Dados processados em `dados/processed/`.
- Outputs finais em `dados/outputs/`.
- Modelo salvo em `modelo/model.pkl`.
- SQL em `sql/schema.sql` e `sql/queries_analiticas.sql`.
- Power BI em `powerbi/aurora_finance_intelligence.pbix`.
- Screenshots finais em `powerbi/screenshots/`.
- App React em `app/`.
- JSONs estáticos para o frontend em `app/public/data/`.
- Documentação complementar em `docs/`.

## 3. Notebooks Didáticos Adicionados

Foram adicionados notebooks em `notebooks/` para evidenciar o processo passo a passo esperado no hackathon. Eles deixam claro que a Aurora não é apenas uma interface visual: o projeto demonstra carregamento, limpeza, EDA, SQL, modelagem e storytelling analítico de forma acompanhável pela banca.

| Notebook | Evidência do processo |
|---|---|
| `01_carregamento_e_limpeza.ipynb` | Carregamento do `Churn Modelling`, diagnóstico inicial, mapeamento para o schema Aurora e explicação da camada sintética de transações. |
| `02_analise_exploratoria.ipynb` | Estatísticas descritivas, taxa de churn, distribuições, análises por estado/perfil e gráficos com interpretação de negócio. |
| `03_sql_insights.ipynb` | SQLite em memória com consultas para nulos, volume por estado, categorias, saldo mensal, churn por perfil e clientes prioritários. |
| `04_modelo_churn.ipynb` | Comparação entre Logistic Regression, Decision Tree e Random Forest, com precision, recall, F1, ROC-AUC, matriz de confusão e feature importance. |
| `05_storytelling_resultados.ipynb` | Leitura dos outputs finais, conexão com Power BI e roteiro curto de apresentação. |

## 4. Dataset Público

O dataset `Churn Modelling` é usado como base principal de clientes e churn quando o CSV está presente.

Mapeamentos importantes:

- `Exited` -> `churn_flag`.
- `EstimatedSalary` -> `renda_mensal`, convertido de anual para mensal.
- `Geography` -> localização.
- `CustomerId` -> `customer_id_original`.
- `Surname` -> nome/sobrenome no schema Aurora.
- `origem_dado` -> `public_kaggle_churn_modelling`.

Como o dataset público não possui histórico transacional por categoria, a Aurora cria uma camada sintética e reprodutível de transações financeiras para viabilizar EDA, SQL, Power BI, Machine Learning e storytelling.

## 5. Machine Learning

O modelo oficial em produção local continua em:

- `src/train_model.py`
- `src/predict_churn.py`
- `modelo/model.pkl`

O pipeline usa `RandomForestClassifier` com `class_weight="balanced"` e threshold ajustável. As métricas são exportadas em `dados/outputs/metricas_modelo.json`, incluindo:

- `accuracy`
- `precision`
- `recall`
- `f1_score`
- `roc_auc`
- `baseline_churn_rate`
- `threshold_used`

Também existe análise de thresholds em `dados/outputs/threshold_analysis.csv`.

## 6. Power BI

A camada Power BI está documentada e possui evidência visual real.

Arquivos principais:

- `powerbi/aurora_finance_intelligence.pbix`
- `powerbi/README.md`
- `powerbi/medidas_dax.md`
- `powerbi/layout_dashboard.md`
- `powerbi/tema_aurora.json`
- `powerbi/screenshots/00_pagina_inicial.png`
- `powerbi/screenshots/01_visao_executiva.png`
- `powerbi/screenshots/02_consumo_comportamento.png`
- `powerbi/screenshots/03_churn_retencao.png`
- `powerbi/screenshots/04_modelo_ml.png`
- `powerbi/screenshots/05_storytelling_executivo.png`

Status: pronto.

## 7. Frontend

O app React é um bônus de produto e apresentação. Ele consome JSONs estáticos gerados pelo pipeline e roda sem backend obrigatório.

Funcionalidades validadas:

- Landing Page.
- Dashboard Executivo.
- Clientes em Risco.
- ML Insights.
- Arquitetura.
- Power BI Guide.
- Análise Expressa com upload local de CSV.

A Análise Expressa roda no navegador, não envia arquivos para servidor e usa score heurístico apenas demonstrativo. O modelo oficial continua sendo o pipeline Python.

## 8. Riscos Remanescentes

- O CSV Kaggle não deve ser baixado automaticamente por exigir autenticação.
- Transações são sintéticas e devem ser explicadas como enriquecimento analítico.
- O score express do frontend é demonstrativo e não substitui o modelo oficial.
- Métricas podem mudar se o pipeline for reexecutado com outra seed ou base.
- O `.pbix` pode ser pesado para alguns repositórios, mas neste projeto funciona como evidência técnica.

## 9. Comandos Finais Recomendados

```powershell
python -m src.pipeline
jupyter lab notebooks
cd app
npm run build
```

## 10. Status Final

Pronto. O projeto está alinhado com os requisitos técnicos do hackathon e agora possui notebooks didáticos para demonstrar o processo de formação, além do pipeline, SQL, Power BI, Machine Learning, documentação e frontend premium.
