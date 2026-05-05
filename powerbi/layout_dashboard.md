# Layout do Dashboard — Aurora Finance Intelligence
## 5 Páginas com Posicionamento Detalhado

> **Tamanho de página recomendado:** 1280 × 720 px (16:9) ou usar o padrão "Widescreen"
> **Tema:** Aurora Finance Intelligence (importar `tema_aurora.json` antes de montar)

---

## Página 1 — Visão Executiva

**Objetivo:** Dar à diretoria uma visão completa do negócio em 30 segundos.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🏷️ AURORA FINANCE INTELLIGENCE — Visão Executiva          [Filtros →] │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────┤
│  TOTAL   │  TAXA DE │  VOLUME  │  ALTO    │  PROB. MÉDIA                │
│ CLIENTES │  CHURN   │ FINANC.  │  RISCO   │    CHURN                    │
│  10.000  │  20,37%  │ R$441,6M │  1.456   │   28,45%                    │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────┤
│                                                                           │
│  📈 EVOLUÇÃO MENSAL DO VOLUME (mai/24 – abr/25)             [linha]      │
│  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                     │
│  R$28,3M ──/\────/\──────/\────/\──────/\────/\──  ~R$27-28M/mês        │
│                                                                           │
├────────────────────────────────┬──────────────────────────────────────────┤
│  🌍 CLIENTES POR PAÍS          │  🎯 DISTRIBUIÇÃO DE RISCO CHURN         │
│  [barras horizontais]          │  [rosca / donut]                        │
│  França    ████████ 5.014      │                                         │
│  Alemanha  ████ 2.509          │    Baixo 74,6% ██████                   │
│  Espanha   ████ 2.477          │    Alto  14,6% ██                       │
│                                │    Médio 10,8% █                        │
├────────────────────────────────┴──────────────────────────────────────────┤
│  🏆 TOP CATEGORIAS POR VOLUME [barras horizontais]                        │
│  Investimentos       R$75,3M  ██████████████████                          │
│  Serviços Financeiros R$73,1M ██████████████████                          │
│  Saúde               R$43,3M  ████████████                                │
│  Educação            R$43,1M  ████████████                                │
│  Transporte          R$43,0M  ████████████                                │
└───────────────────────────────────────────────────────────────────────────┘
```

### Visuais e configurações:

**Cabeçalho:**
- Caixa de texto com título: `AURORA FINANCE INTELLIGENCE` (fonte 18px, cor ciano #00D4FF)
- Subtítulo: `Visão Executiva` (fonte 12px, cinza)
- Slicers no canto direito: Estado, Perfil de Risco

**Cards KPI (linha superior):**
| Card | Medida | Formato |
|------|--------|---------|
| Total Clientes | `[Total Clientes]` | `#,##0` |
| Taxa de Churn | `[Taxa Churn]` | `0.00%` |
| Volume Financeiro | `[Volume Financeiro]` | `R$ #,##0,,M` |
| Clientes Alto Risco | `[Clientes Alto Risco]` | `#,##0` |
| Prob. Média Churn | `[Probabilidade Média Churn]` | `0.00%` |

**Gráfico de linhas (Evolução Mensal):**
- Eixo X: `transacoes_limpo[ano_mes]`
- Valores: `[Volume Financeiro]`
- Linha de tendência: ativar
- Marcadores: ativar

**Gráfico de barras (Clientes por País):**
- Eixo Y: `clientes_limpo[estado]`
- Valores: `[Total Clientes]`
- Barras horizontais, ordenar por valor decrescente

**Gráfico de rosca (Distribuição de Risco):**
- Legenda: `predicoes_churn[risco]`
- Valores: `[Total Clientes]`
- Cores: Alto = `#EF4444`, Médio = `#F59E0B`, Baixo = `#10B981`

**Gráfico de barras (Top Categorias):**
- Eixo Y: `categorias_limpo[nome_categoria]`
- Valores: `[Volume Financeiro]`
- Ordenar por valor decrescente
- Mostrar top 5 ou 8

---

## Página 2 — Consumo e Comportamento Financeiro

**Objetivo:** Detalhar como os clientes gastam, por canal e categoria.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  💳 Consumo e Comportamento Financeiro         [Data] [Tipo] [Canal]    │
├──────────────────────────────────┬──────────────────────────────────────┤
│  💰 GASTOS POR CATEGORIA         │  📱 TICKET MÉDIO POR CANAL           │
│  [barras verticais]              │  [barras verticais]                  │
│                                  │                                      │
│  Invest. ██████ R$75,3M          │  App Mobile   R$1.652 ██             │
│  Serv.Fin ██████ R$73,1M         │  Internet Bkg R$1.633 ██             │
│  Saúde   ████  R$43,3M           │  Cartão       R$1.663 ██             │
│  Educação ████ R$43,1M           │  PIX          R$1.659 ██             │
│  Transp.  ████ R$43,0M           │  Agência      R$1.659 ██             │
├──────────────────────────────────┴──────────────────────────────────────┤
│  📅 EVOLUÇÃO MENSAL POR TIPO DE TRANSAÇÃO [área empilhada]              │
│                                                                          │
│  Crédito ████  Débito ████  Pix ████  Transferência ████                │
│  mai/24 ── jun/24 ── jul/24 ── ... ── mar/25 ── abr/25                  │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│  🔢 MATRIZ: PERFIL DE RISCO × CATEGORIA (Volume em R$)                  │
│  [matriz/tabela]                                                         │
│                         Conservador  Moderado  Arrojado  Total           │
│  Alimentação            R$XX,XM      R$XX,XM   R$XX,XM   R$42,9M        │
│  Investimentos          R$XX,XM      R$XX,XM   R$XX,XM   R$75,3M        │
│  Serviços Financeiros   R$XX,XM      R$XX,XM   R$XX,XM   R$73,1M        │
│  ...                                                                      │
└───────────────────────────────────────────────────────────────────────────┘
```

### Visuais e configurações:

**Slicers no topo:**
- `transacoes_limpo[data]` → tipo: Intervalo de datas
- `transacoes_limpo[tipo]` → tipo: Lista com seleção múltipla
- `transacoes_limpo[canal]` → tipo: Lista com seleção múltipla

**Gastos por Categoria (barras verticais):**
- Eixo X: `categorias_limpo[nome_categoria]`
- Valores: `[Volume Financeiro]`
- Ordenar por valor decrescente

**Ticket Médio por Canal (barras verticais):**
- Eixo X: `transacoes_limpo[canal]`
- Valores: `[Ticket Médio]`

**Evolução por Tipo (área empilhada):**
- Eixo X: `transacoes_limpo[ano_mes]`
- Valores: `[Volume Financeiro]`
- Legenda: `transacoes_limpo[tipo]`
- Tipo de gráfico: Área empilhada ou Barras empilhadas

**Matriz Perfil × Categoria:**
- Linhas: `categorias_limpo[nome_categoria]`
- Colunas: `clientes_limpo[perfil_risco]`
- Valores: `[Volume Financeiro]`
- Formatar valores como moeda abreviada (R$ X,XM)

---

## Página 3 — Churn e Retenção

**Objetivo:** Identificar e priorizar clientes em risco de saída.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🔴 Churn e Retenção          [Estado ▼] [Perfil ▼] [Risco ▼]          │
├──────────────────────────────────┬──────────────────────────────────────┤
│  📊 CLIENTES POR FAIXA DE RISCO │  🎯 PROBABILIDADE MÉDIA DE CHURN     │
│  [barras verticais]              │  [card grande]                       │
│                                  │                                      │
│  Baixo  ████████████ 7.464       │         28,45%                       │
│  Alto   ████ 1.456               │    Probabilidade Média               │
│  Médio  ███ 1.080                │                                      │
│                                  │  [card] 1.456 → Alto Risco          │
│                                  │  [card] 1.080 → Médio Risco         │
│                                  │  [card] 7.464 → Baixo Risco         │
├──────────────────────────────────┴──────────────────────────────────────┤
│  📋 TOP 20 CLIENTES EM RISCO [tabela com rolagem]                        │
│                                                                          │
│  Nome          Estado    Perfil       Prob.Churn  Risco  Recomendação   │
│  Bradley       Alemanha  Conservador  98,97%      Alto   Plano retencao  │
│  Foster        Alemanha  Conservador  97,81%      Alto   Plano retencao  │
│  Dike          Alemanha  Conservador  97,56%      Alto   Plano retencao  │
│  Manna         Alemanha  Conservador  97,49%      Alto   Plano retencao  │
│  ...           ...       ...          ...         ...    ...             │
│                                                                          │
│  [Formatação condicional: prob_churn > 0.8 = fundo vermelho]            │
└───────────────────────────────────────────────────────────────────────────┘
```

### Visuais e configurações:

**Slicers (no topo ou lateral):**
- `clientes_limpo[estado]` → Lista
- `clientes_limpo[perfil_risco]` → Lista
- `predicoes_churn[risco]` → Lista (Alto / Médio / Baixo)

**Barras de Risco:**
- Eixo X: `predicoes_churn[risco]`
- Valores: `[Total Clientes]`
- Cores por categoria: Alto=#EF4444, Médio=#F59E0B, Baixo=#10B981

**Cards de Risco:**
- `[Clientes Alto Risco]`, `[Clientes Médio Risco]`, `[Clientes Baixo Risco]`
- `[Probabilidade Média Churn]` (card principal, destaque)

**Tabela Top 20 Clientes em Risco:**
- Filtro visual: `predicoes_churn[risco]` = "Alto"
- Colunas: `nome`, `estado`, `perfil_risco`, `prob_churn`, `risco`, `recomendacao`
- Ordenar por `prob_churn` decrescente
- Formatação condicional em `prob_churn`: escala de cor vermelho (alto) → amarelo (médio)
- Top N: usar filtro visual para mostrar apenas Top 20 por `prob_churn`

---

## Página 4 — Modelo ML

**Objetivo:** Demonstrar a qualidade e transparência do modelo de Machine Learning.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  🤖 Modelo ML — Avaliação e Transparência                               │
├──────────┬──────────┬──────────┬──────────┬──────────────────────────────┤
│  ROC-AUC │ PRECISION│  RECALL  │ F1 SCORE │  THRESHOLD                  │
│  0,929   │  0,660   │  0,811   │  0,728   │    0,40                     │
│ Excelente│ Razoável │   Alto   │   Bom    │  Otimizado p/ recall        │
├──────────┴──────────┴──────────┴──────────┴──────────────────────────────┤
│  🏆 FEATURE IMPORTANCE (Top 10)         │  📊 ANÁLISE DE THRESHOLDS     │
│  [barras horizontais]                   │  [tabela]                     │
│                                         │                               │
│  idade              0,161 ██████████    │  Thresh  Prec  Recall  F1     │
│  produtos_ativos    0,098 ██████        │  0,30   0,52  0,897  0,655    │
│  perfil_Conserv.   0,091 █████         │  0,40   0,66  0,811  0,728  ← │
│  score_credito     0,081 █████         │  0,50   0,76  0,668  0,712    │
│  saldo_atual       0,041 ██            │                               │
│  perfil_Moderado   0,041 ██            │                               │
│  perfil_Arrojado   0,036 ██            │                               │
│  razao_saldo_renda 0,036 ██            │                               │
│  membro_ativo      0,025 █             │                               │
│  estado_Alemanha   0,022 █             │                               │
├─────────────────────────────────────────┴───────────────────────────────┤
│  📈 TRADE-OFF: PRECISION vs RECALL por THRESHOLD [gráfico de linhas]    │
│                                                                          │
│  1,0 ─                                                                   │
│  0,8 ─  Recall ──────────●──────────●                                   │
│  0,6 ─  Precision ────────────────●─────────●                          │
│  0,4 ─                                                                   │
│       threshold: 0,30        0,40        0,50                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### Visuais e configurações:

**Cards de Métricas:**
- Criar medidas DAX para ROC-AUC, Precision, Recall, F1, Threshold (ver `medidas_dax.md`)
- Adicionar rótulo de contexto abaixo de cada card (caixa de texto pequena)

**Feature Importance (barras horizontais):**
- Eixo Y: `feature_importance[feature]`
- Valores: `feature_importance[importance]`
- Ordenar por `importance` decrescente
- Mostrar top 10 (filtro visual: Top N por `importance`)
- Cor: gradiente ciano

**Tabela Threshold Analysis:**
- Colunas: `threshold`, `precision`, `recall`, `f1_score`, `alert_rate`, `retention_score`
- Formatação condicional: destacar linha do threshold 0,40
- Formatar como porcentagem (0.00%)

**Gráfico Precision vs Recall (linhas):**
- Eixo X: `threshold_analysis[threshold]`
- Linha 1: `threshold_analysis[precision]` (cor: laranja)
- Linha 2: `threshold_analysis[recall]` (cor: ciano)
- Linha 3 (opcional): `threshold_analysis[f1_score]` (cor: violeta)
- Marcadores ativados
- Linha de referência vertical no threshold 0,40

---

## Página 5 — Storytelling Executivo

**Objetivo:** Contar a história completa do projeto para um público executivo não técnico.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📋 Aurora Finance Intelligence — Storytelling Executivo                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🔴 PROBLEMA                    💡 SOLUÇÃO                              │
│  ┌──────────────────────┐       ┌──────────────────────┐               │
│  │ 20,37% dos clientes  │       │ Pipeline ML preditivo │               │
│  │ saem sem aviso.      │  →    │ com ROC-AUC de 0,929  │               │
│  │ Custo de aquisição   │       │ que rankeia clientes  │               │
│  │ 5x maior que reter.  │       │ por risco de saída.   │               │
│  └──────────────────────┘       └──────────────────────┘               │
│                                                                          │
│  🏗️ ARQUITETURA                                                         │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  Kaggle CSV → Python Pipeline → ML (XGBoost) → Power BI      │       │
│  │  + Transações Sintéticas → Feature Engineering → Dashboard   │       │
│  └──────────────────────────────────────────────────────────────┘       │
│                                                                          │
│  📊 PRINCIPAIS INSIGHTS              💼 IMPACTO DE NEGÓCIO              │
│  ┌──────────────────────┐            ┌──────────────────────┐           │
│  │ • Idade é o fator #1 │            │ • 1.456 clientes de  │           │
│  │ • Alemanha tem maior │            │   alto risco          │           │
│  │   taxa de churn      │            │   identificados       │           │
│  │ • Conservadores são  │            │ • Recall 81%: captura │           │
│  │   os de maior risco  │            │   4 em cada 5        │           │
│  │ • Investimentos e    │            │   churners           │           │
│  │   Serviços Financ.   │            │ • R$441,6M em        │           │
│  │   dominam o volume   │            │   transações mapeadas │           │
│  └──────────────────────┘            └──────────────────────┘           │
│                                                                          │
│  🚀 PRÓXIMOS PASSOS                                                      │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │  1. Integrar dados reais do CRM                              │       │
│  │  2. Automatizar pipeline mensal                              │       │
│  │  3. Deploy em produção (AWS Free Tier)                       │       │
│  │  4. A/B test de campanhas de retenção                        │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Visuais e configurações:

**Blocos de texto (6 blocos principais):**
Usar **Inserir → Caixa de Texto** para cada bloco. Sugestão de cores:
- Título do bloco: ciano (`#00D4FF`), negrito, 14px
- Corpo: branco suave (`#E6EDF3`), 11px
- Fundo do bloco: azul escuro (`#1C2128`), bordas arredondadas via formatação

**Imagens dos gráficos:**
- Inserir → Imagem → selecionar os PNGs de `reports/figuras/`
  - `evolucao_mensal.png`
  - `top_categorias.png`
  - `ticket_por_churn.png`
  - `histograma_renda.png`

**Diagrama de Arquitetura:**
- Usar caixas de texto + setas (formas do Power BI: Inserir → Formas)
- Ou inserir uma imagem do diagrama de arquitetura

**Ícones de status:**
- Usar emojis diretamente nas caixas de texto (✅, 🔴, 💡, 📊)

---

## Dicas Gerais de Layout

1. **Fundo:** Defina cor de fundo da página como `#0D1117` (preto-azul escuro) em **Formatar Página**
2. **Bordas dos visuais:** Use `#30363D` com espessura 1px
3. **Tipografia:** Use Segoe UI em todos os títulos de visual
4. **Espaçamento:** Deixe pelo menos 8px entre visuais
5. **Grid:** Use a grade do Power BI (Exibição → Mostrar Linhas de Grade) para alinhar
6. **Zoom:** Monte em 100% e verifique em 75% para visão geral
7. **Modo de foco:** Use Ctrl+M para verificar cada visual individualmente

---

*Layout Dashboard — Aurora Finance Intelligence*
