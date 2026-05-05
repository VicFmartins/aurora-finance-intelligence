# Checklist de Screenshots — Aurora Finance Intelligence

> Após montar cada página no Power BI Desktop, tire um screenshot e salve em `powerbi/screenshots/`.
> Os prints são evidência técnica do dashboard e devem ser incluídos no repositório.

---

## Como tirar o screenshot

**Opção 1 — Ferramenta de Recorte do Windows:**
1. Pressione `Win + Shift + S`
2. Selecione a área do dashboard (excluindo o painel de campos/formatação lateral)
3. Salve com o nome correto em `powerbi/screenshots/`

**Opção 2 — Exportar como imagem pelo Power BI:**
1. Abra a página desejada
2. Vá em **Arquivo → Exportar → Exportar para PDF** (ou Print Screen)
3. Alternativamente: botão direito no canvas → "Copiar" → colar no Paint → salvar como PNG

**Resolução recomendada:** 1920×1080 px mínimo  
**Formato:** PNG  
**Qualidade:** Alta (evitar compressão JPG)

---

## Screenshots obrigatórios

### 01 — Visão Executiva
**Arquivo:** `powerbi/screenshots/01_visao_executiva.png`

**O que deve aparecer:**
- [ ] 5 cards KPI visíveis (Total Clientes, Taxa Churn, Volume, Alto Risco, Prob. Churn)
- [ ] Valores corretos: 10.000 clientes, 20,37% churn, R$ 441,6M volume, 1.456 alto risco
- [ ] Gráfico de linhas com evolução mensal (maio/24 a abr/25)
- [ ] Gráfico de barras com distribuição por país (França, Alemanha, Espanha)
- [ ] Gráfico de rosca com distribuição de risco
- [ ] Top categorias por volume visível
- [ ] Tema Aurora (fundo escuro, texto claro, destaques em ciano)

**Antes de tirar o print:**
- [ ] Remover qualquer seleção ativa nos visuais
- [ ] Fechar painel de Formatação e Campos se estiver aberto
- [ ] Zoom em 100%
- [ ] Nenhum visual com mensagem de erro

---

### 02 — Consumo e Comportamento Financeiro
**Arquivo:** `powerbi/screenshots/02_consumo_comportamento.png`

**O que deve aparecer:**
- [ ] Gráfico de gastos por categoria (Investimentos e Serviços Financeiros no topo)
- [ ] Gráfico de ticket médio por canal
- [ ] Evolução mensal por tipo de transação (área ou barras empilhadas)
- [ ] Matriz perfil_risco × categoria com valores
- [ ] Slicers de período, tipo e canal visíveis

**Antes de tirar o print:**
- [ ] Slicers em estado "sem filtro" (todos selecionados) para mostrar visão completa
- [ ] Todos os visuais carregados sem loading
- [ ] Nomes das categorias legíveis

---

### 03 — Churn e Retenção
**Arquivo:** `powerbi/screenshots/03_churn_retencao.png`

**O que deve aparecer:**
- [ ] Barras de clientes por faixa de risco (Baixo: 7.464, Alto: 1.456, Médio: 1.080)
- [ ] Card de probabilidade média de churn (28,45%)
- [ ] Tabela com top 20 clientes em risco (nome, estado, prob_churn, risco, recomendação)
- [ ] Formatação condicional na coluna prob_churn (vermelho → amarelo)
- [ ] Slicers de estado, perfil e risco visíveis

**Antes de tirar o print:**
- [ ] Filtrar a tabela para mostrar apenas Alto Risco ou sem filtro para mostrar variedade
- [ ] Scroll da tabela posicionado no início (primeiros clientes da lista)
- [ ] Probabilidade mais alta visível (Bradley: 98,97%)

---

### 04 — Modelo ML
**Arquivo:** `powerbi/screenshots/04_modelo_ml.png`

**O que deve aparecer:**
- [ ] Cards: ROC-AUC (0,929), Precision (0,660), Recall (0,811), F1 (0,728), Threshold (0,40)
- [ ] Gráfico de Feature Importance com as 10 principais features
  - Topo: `idade` (0,161), `produtos_ativos` (0,098), `perfil_Conservador` (0,091)
- [ ] Tabela de Threshold Analysis com 3 linhas (0.30, 0.40, 0.50)
- [ ] Linha do threshold 0.40 destacada
- [ ] Gráfico de linhas Precision vs Recall vs F1 por threshold

**Antes de tirar o print:**
- [ ] Verificar se os valores dos cards batem com metricas_modelo.json
- [ ] Feature importance ordenada do maior para o menor
- [ ] Nomes das features legíveis (pode precisar de rolagem horizontal)

---

### 05 — Storytelling Executivo
**Arquivo:** `powerbi/screenshots/05_storytelling_executivo.png`

**O que deve aparecer:**
- [ ] Bloco "Problema" com dados de churn (20,37%)
- [ ] Bloco "Solução" com ROC-AUC 0,929
- [ ] Diagrama ou descrição de Arquitetura
- [ ] Bloco "Principais Insights"
- [ ] Bloco "Impacto de Negócio" com números reais
- [ ] Bloco "Próximos Passos"
- [ ] Pelo menos uma imagem de `reports/figuras/` inserida
- [ ] Layout organizado e legível

**Antes de tirar o print:**
- [ ] Nenhuma caixa de texto selecionada (bordas de edição visíveis arruínam o print)
- [ ] Clicar fora de qualquer visual para deselecionar
- [ ] Verificar se textos não estão cortados

---

## Checklist global antes de tirar os prints

- [ ] Tema Aurora aplicado em todas as páginas
- [ ] Título do relatório visível em cada página
- [ ] Nenhum visual com "Não é possível exibir este visual" ou dados em branco inesperados
- [ ] Slicers em estado neutro (nada filtrado) para os prints de documentação
- [ ] Power BI em modo de apresentação ou canvas limpo (sem painéis laterais)

---

## Após salvar os prints

1. Confirme que todos os 5 arquivos existem em `powerbi/screenshots/`
2. Abra cada arquivo e verifique a legibilidade
3. Adicione ao Git: `git add powerbi/screenshots/` → `git commit -m "feat: screenshots dashboard Power BI"`
4. Atualize `docs/auditoria_final.md` marcando os screenshots como concluídos

---

*Checklist Screenshots — Aurora Finance Intelligence*
