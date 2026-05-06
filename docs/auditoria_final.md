# Auditoria Técnica — Aurora Finance Intelligence
**Data:** 05 de Maio de 2026 | **Auditora:** Vitoria Freitas

> Esta auditoria substitui a versão anterior. Todos os bugs abaixo foram **corrigidos diretamente nos arquivos** durante esta sessão.

---

## BUGS CORRIGIDOS NESTA SESSÃO

### 🔴 BUG 1 — Colunas erradas no DAX (`medidas_dax.md`) — CRÍTICO
DAX referenciava colunas do Kaggle (inglês), mas o CSV processado usa português.
Medidas afetadas: Clientes Ativos, Clientes com Churn, Renda Média, Saldo Médio, Idade, Tenure, Produtos, Cartão, Membro Ativo, Churn por País.

| DAX usava (ERRADO) | Coluna real no CSV |
|---|---|
| `clientes_limpo[Exited]` | `clientes_limpo[churn_flag]` |
| `clientes_limpo[Balance]` | `clientes_limpo[saldo_atual]` |
| `clientes_limpo[EstimatedSalary]` | `clientes_limpo[renda_mensal]` |
| `clientes_limpo[Age]` | `clientes_limpo[idade]` |
| `clientes_limpo[Tenure]` | `clientes_limpo[tempo_relacionamento]` |
| `clientes_limpo[NumOfProducts]` | `clientes_limpo[produtos_ativos]` |
| `clientes_limpo[HasCrCard]` | `clientes_limpo[tem_cartao_credito]` |
| `clientes_limpo[IsActiveMember]` | `clientes_limpo[membro_ativo]` |
| `predicoes_churn[churn_flag]` | `predicoes_churn[predicao_churn]` |
| `metrica = "threshold"` | `metrica = "threshold_used"` |

**Status:** ✅ Corrigido em `powerbi/medidas_dax.md`

---

### 🔴 BUG 2 — "Médio" vs "Medio" no filtro DAX — CRÍTICO
CSV tem `"Medio"` (sem acento); DAX filtrava `"Médio"` (com acento).
Resultado: `Clientes Médio Risco` retornava 0 — 1.080 clientes sumiam do dashboard.
**Status:** ✅ Corrigido em `powerbi/medidas_dax.md`

---

### 🔴 BUG 3 — Case sensitivity em tipo de transação — CRÍTICO
CSV tem `"Debito"` / `"Credito"` (inicial maiúscula); DAX filtrava `"debito"` / `"credito"`.
Resultado: `Total Gastos` e `Total Créditos` retornavam 0; `Saldo Líquido` calculado incorretamente.
**Status:** ✅ Corrigido em `powerbi/medidas_dax.md`

---

### 🟡 BUG 4 — Estrutura de tabelas errada em `modelagem_dados.md` — MODERADO
Tabela `clientes_limpo` documentada com colunas do Kaggle. `predicoes_churn` com campo errado (`churn_flag` em vez de `predicao_churn`), acento errado em `"Médio"`, e colunas faltando.
**Status:** ✅ Corrigido em `powerbi/modelagem_dados.md`

---

### 🟡 GAP — Análise probabilística ausente no notebook — REQUISITO DO EDITAL
Edital exige: *"Uso de fundamentos de probabilidade para identificar produtos de maior destaque, justificando-os com análises estatísticas."*
Notebook `02_limpeza_eda.ipynb` não tinha nenhuma célula com p-valor ou teste de hipótese.

Adicionada seção completa com:
- P(Churn | Perfil de Risco) com risco relativo vs baseline
- P(Churn | Estado) com risco relativo por país
- P(Churn | Membro Ativo) com ratio de risco
- Teste Qui-Quadrado: χ² = 851.79 | p-valor ≈ 0.000 ✅ significativo
- Correlação de Pearson com p-valor para cada variável numérica

**Status:** ✅ Corrigido em `notebooks/02_limpeza_eda.ipynb`

---

## PANORAMA GERAL DO PROJETO (versão anterior desta auditoria)

Aurora Finance Intelligence esta consistente como projeto de hackathon de dados com ambicao de produto. O repositorio entrega:

- pipeline Python executavel por `python -m src.pipeline`
- suporte ao dataset publico `Churn Modelling` em `dados/raw/churn_modelling.csv`
- fallback sintetico quando o CSV publico nao existe
- camada sintetica de transacoes para SQL, EDA, Power BI e storytelling
- modelo de churn com `RandomForestClassifier`
- frontend React estatico em `app/`
- documentacao suficiente para GitHub e banca

No estado atual, o projeto esta tecnicamente forte. O principal ponto remanescente nao e de codigo: ainda falta material final de evidencia visual do Power BI no repositorio, se voce quiser levar isso como prova completa para a banca.

## 2. O que foi validado

- execucao do pipeline do zero com CSV publico
- execucao do pipeline do zero sem CSV publico
- execucao separada de `python -m src.predict_churn`
- build do frontend com `npm run build`
- existencia e schema dos CSVs processados
- existencia e estrutura dos JSONs do frontend
- coerencia entre dataset publico, schema interno e documentacao
- coerencia do `sql/schema.sql` com os CSVs finais
- coerencia e execucao das queries de `sql/queries_analiticas.sql` em SQLite
- `.gitignore` e prontidao basica para GitHub

## 3. Testes executados

### Pipeline com CSV publico

```powershell
python -m src.pipeline
```

### Pipeline sem CSV publico

```powershell
Move-Item dados\raw\churn_modelling.csv dados\raw\churn_modelling.tmp.csv
python -m src.pipeline
Move-Item dados\raw\churn_modelling.tmp.csv dados\raw\churn_modelling.csv
python -m src.pipeline
```

### Predicao separada

```powershell
python -m src.predict_churn
```

### Frontend

```powershell
cd app
npm run build
```

### Validacao estrutural

- validacao de schema com `pandas`
- validacao de JSONs do frontend
- carga do schema SQL em SQLite em memoria
- execucao das 8 queries analiticas

## 4. Resultado dos testes

### Pipeline com CSV publico

- status: `OK`
- origem detectada: `public_kaggle_churn_modelling`
- clientes: `10000`
- transacoes processadas: `267255`
- categorias: `10`
- metricas da ultima execucao:
  - `roc_auc = 0.9288`
  - `precision = 0.6600`
  - `recall = 0.8108`
  - `threshold_used = 0.40`

### Pipeline sem CSV publico

- status: `OK`
- origem detectada: `synthetic_fallback`
- clientes: `2800`
- transacoes processadas: `78484`
- metricas da ultima execucao de fallback:
  - `roc_auc = 0.7189`
  - `precision = 0.5556`
  - `recall = 0.1042`
  - `threshold_used = 0.50`

### Predicao separada

- status: `OK`
- `python -m src.predict_churn` atualiza `dados/outputs/predicoes_churn.csv`

### Frontend

- status: `OK`
- `npm run build` concluido sem erro de TypeScript, Vite ou imports

### CSVs e JSONs

- `dados/processed/clientes_limpo.csv`: `OK`
- `dados/processed/transacoes_limpo.csv`: `OK`
- `dados/processed/categorias_limpo.csv`: `OK`
- `dados/processed/base_modelagem.csv`: `OK`
- `dados/outputs/predicoes_churn.csv`: `OK`
- `dados/outputs/metricas_modelo.json`: `OK`
- `dados/outputs/feature_importance.csv`: `OK`
- `dados/outputs/threshold_analysis.csv`: `OK`
- `app/public/data/metrics.json`: `OK`
- `app/public/data/predictions.json`: `OK`
- `app/public/data/feature_importance.json`: `OK`
- `app/public/data/summary.json`: `OK`
- `app/public/data/threshold_analysis.json`: `OK`

### SQL

- `sql/schema.sql`: `OK`
- `sql/queries_analiticas.sql`: `OK`
- queries executadas com sucesso em SQLite: `8/8`

## 5. Problemas encontrados

### Problema 1. Ausencia de `threshold_analysis.json` no frontend

O checklist pedia esse arquivo, mas ele nao estava sendo exportado para `app/public/data/`.

### Problema 2. `sql/schema.sql` estava defasado

O schema nao refletia o schema atual dos CSVs finais. Faltavam colunas como:

- `customer_id_original`
- `tempo_relacionamento`
- `tem_cartao_credito`
- `origem_dado`
- varias colunas da `base_modelagem`

### Problema 3. Risco real de data leakage no modo publico

No modo `Churn Modelling`, a camada sintetica de transacoes estava usando `churn_flag` para moldar comportamento financeiro. Isso contaminava indiretamente os features com o target.

### Problema 4. App pouco resiliente a JSON ausente ou vazio

Se algum JSON do frontend estivesse faltando ou viesse vazio, o carregamento poderia quebrar ou ficar inconsistente.

### Problema 5. Roteiro de apresentacao desatualizado

O roteiro ainda soava como se toda a base fosse 100 por cento simulada, o que nao representa mais o estado final do projeto.

### Problema 6. `.gitignore` incompleto para a nova estrategia

O dataset publico local ainda nao estava explicitamente ignorado.

## 6. Correcoes aplicadas

- exportei `app/public/data/threshold_analysis.json`
- atualizei `sql/schema.sql` para refletir os CSVs reais do projeto
- atualizei `sql/queries_analiticas.sql` para nomes coerentes com o schema final
- corrigi o risco de leakage no modo publico:
  - a simulacao de transacoes continua existindo
  - mas, quando a origem e `Churn Modelling`, ela nao usa `Exited` para gerar comportamento sintetico
- deixei o app mais resiliente a JSON ausente ou vazio com fallbacks seguros
- alinhei a documentacao e o roteiro de apresentacao ao uso de base publica + camada sintetica
- atualizei `.gitignore` para ignorar `dados/raw/churn_modelling.csv` e arquivos temporarios
- revalidei pipeline, predicao separada, build do frontend e SQL

## 7. Riscos remanescentes

### Risco 1. Power BI ainda depende de evidencia manual

O guia esta bom, mas o repositorio ainda nao tem screenshots reais do painel. Isso impacta mais a percepcao da entrega do que o codigo em si.

### Risco 2. Fallback sintetico continua mais fraco em recall

No modo fallback, o modelo continua com recall baixo. Isso nao quebra o projeto, mas deve ser tratado como baseline de demonstracao, nao como melhor configuracao operacional.

### Risco 3. Nao ha suite automatizada de testes unitarios

O projeto esta validado por execucao real, mas ainda sem testes automatizados formais.

### Risco 4. `model.pkl` e outputs sao regeneraveis

Se o repositorio for compartilhado sem outputs, a reproducao continua possivel, mas a evidencia pronta para banca diminui.

## 8. Checklist final para Vitoria executar manualmente

- confirmar que `dados/raw/churn_modelling.csv` esta no lugar correto
- rodar `python -m src.pipeline`
- abrir `dados/outputs/metricas_modelo.json` e conferir as metricas finais
- abrir `app/public/data/summary.json` e confirmar:
  - `data_source_name = Churn Modelling`
  - `public_dataset_used = true`
  - `synthetic_transactions_used = true`
- rodar `python -m src.predict_churn`
- rodar `cd app` e `npm run build`
- abrir o app localmente para conferir a frase:
  - `Base publica Kaggle + camada sintetica de transacoes`
- montar o Power BI com base nos arquivos processados e outputs
- salvar screenshots finais em `powerbi/screenshots/`
- revisar rapidamente o pitch em `docs/roteiro_apresentacao.md`

## 9. Comandos finais recomendados

### Caminho principal com base publica

```powershell
python -m src.pipeline
python -m src.predict_churn
cd app
npm run build
```

### Teste de fallback

```powershell
Move-Item dados\raw\churn_modelling.csv dados\raw\churn_modelling.tmp.csv
python -m src.pipeline
Move-Item dados\raw\churn_modelling.tmp.csv dados\raw\churn_modelling.csv
python -m src.pipeline
```

### Recomendacao de versionamento

- `churn_modelling.csv`: **nao versionar**
- outputs CSV e JSON leves de evidencia: **pode versionar**
- `model.pkl`: **opcional**, versionar so se o tamanho estiver aceitavel
- `app/dist`: **nao versionar**
- screenshots do Power BI: **versionar**

## 10. Status final

**Pendente — aguardando screenshots manuais do Power BI Desktop**

O codigo, o pipeline, o frontend, os outputs e a documentacao tecnica estao prontos.

---

## 11. Camada Power BI — Status (atualizado em 05/05/2026)

**✅ PRONTO — Todos os guias e arquivos de configuracao gerados.**

A pasta `powerbi/` agora contem todos os artefatos necessarios para montar o dashboard:

| Arquivo | Status | Descricao |
|---------|--------|-----------|
| `powerbi/README.md` | ✅ Pronto | Guia completo de montagem passo a passo |
| `powerbi/medidas_dax.md` | ✅ Pronto | +20 medidas DAX organizadas por secao |
| `powerbi/modelagem_dados.md` | ✅ Pronto | Relacionamentos, cardinalidade e erros comuns |
| `powerbi/layout_dashboard.md` | ✅ Pronto | Layout detalhado das 5 paginas com ASCII art |
| `powerbi/tema_aurora.json` | ✅ Pronto | Tema dark fintech (azul marinho, ciano, violeta) |
| `powerbi/power_query.md` | ✅ Pronto | Codigo M e instrucoes de importacao e tipos |
| `powerbi/checklist_screenshots.md` | ✅ Pronto | Guia de quais prints tirar e onde salvar |
| `powerbi/roteiro_demo_powerbi.md` | ✅ Pronto | Roteiro de fala de 60 segundos para apresentacao |
| `powerbi/resumo_insights.md` | ✅ Pronto | Insights numericos reais gerados automaticamente |
| `powerbi/screenshots/` | ⏳ Aguardando | Pasta criada, prints dependem de acao manual no PBI Desktop |

**Numeros reais do projeto (gerados por Python a partir dos CSVs):**
- 10.000 clientes analisados
- Taxa de churn real: 20,37% (2.037 clientes)
- Volume financeiro total: R$ 441.581.018,45
- Ticket medio: R$ 1.652,28
- Clientes de alto risco: 1.456 (14,6%)
- Probabilidade media de churn: 28,45%
- ROC-AUC do modelo: 0,9288
- Feature mais importante: `idade` (0,161)

**O unico passo remanescente de toda a entrega Power BI e manual:**
1. Abrir o Power BI Desktop
2. Importar os CSVs conforme `powerbi/README.md`
3. Aplicar o tema `powerbi/tema_aurora.json`
4. Criar as 5 paginas conforme `powerbi/layout_dashboard.md`
5. Tirar 5 screenshots e salvar em `powerbi/screenshots/`

Quando os screenshots estiverem prontos, o projeto estara **completamente pronto** para apresentacao.
