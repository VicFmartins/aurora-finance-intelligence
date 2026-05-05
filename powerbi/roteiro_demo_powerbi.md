# Roteiro de Demonstração — Power BI
## Aurora Finance Intelligence | 60 segundos

---

## Roteiro de Fala (1 minuto exato)

> **Dica de apresentação:** Abra o Power BI em modo de apresentação (F11) antes de começar.
> Fale com calma, pause brevemente ao clicar em cada página.

---

### [0–10s] Abertura — Contexto do problema

*[Página 1 — Visão Executiva]*

> "A Aurora Finance Intelligence resolve um problema real: **20% dos clientes bancários saem sem aviso**.
> Aqui na Visão Executiva temos em 30 segundos: 10 mil clientes analisados, R$ 441 milhões em transações mapeadas, e 1.456 clientes já identificados como alto risco de churn."

---

### [10–25s] Comportamento e dados financeiros

*[Clicar na Página 2 — Consumo e Comportamento]*

> "Enriquecemos a base pública do Kaggle com uma camada sintética de transações financeiras.
> Isso nos permite ver **onde os clientes gastam** — Investimentos e Serviços Financeiros dominam — e como o comportamento varia por canal e perfil de risco."

---

### [25–40s] Churn e priorização

*[Clicar na Página 3 — Churn e Retenção]*

> "Aqui está o coração do projeto: a **lista de priorização de retenção**.
> Cada cliente tem uma probabilidade de churn calculada pelo modelo — o cliente Bradley, por exemplo, tem 98,97% de chance de sair.
> A equipe de CRM recebe essa lista ordenada com recomendação de ação."

---

### [40–55s] Qualidade do modelo ML

*[Clicar na Página 4 — Modelo ML]*

> "O modelo tem **ROC-AUC de 0,929** — excelente para um problema de churn bancário.
> Recall de 81% significa que capturamos 4 em cada 5 clientes que iriam sair.
> A feature mais importante é a **idade**, seguida de produtos ativos e perfil de risco."

---

### [55–60s] Fechamento

*[Clicar na Página 5 — Storytelling Executivo ou voltar à Página 1]*

> "Em resumo: pipeline reproduzível, dados públicos auditáveis, modelo transparente e dashboard pronto para decisão.
> **A Aurora transforma sinais financeiros em priorização de retenção.**"

---

## Variações para contextos diferentes

### Versão ultra-curta (30 segundos — para elevator pitch)

> "Desenvolvemos um sistema de predição de churn bancário com ROC-AUC de 0,929.
> A base é pública — Kaggle Churn Modelling — enriquecida com transações sintéticas.
> O resultado: 1.456 clientes de alto risco identificados, com probabilidade individual de saída e recomendação de retenção, tudo visualizado neste dashboard Power BI."

---

### Versão técnica (para banca / avaliadores)

> "O pipeline parte do dataset público Churn Modelling do Kaggle, com 10 mil clientes.
> Adicionamos feature engineering sobre transações sintéticas — pct_canal_digital, razao_gasto_renda, pressao_financeira entre outras.
> O modelo XGBoost foi calibrado com threshold 0,40 para maximizar recall, resultando em F1 de 0,728 e AUC de 0,929.
> As predições alimentam diretamente este dashboard Power BI, com modelagem em estrela, medidas DAX e tema personalizado Aurora Finance Intelligence."

---

## Checklist pré-apresentação

- [ ] Power BI Desktop aberto no arquivo `.pbix`
- [ ] Todas as 5 páginas carregadas sem erros
- [ ] Tema Aurora aplicado e visual está correto
- [ ] Página 1 selecionada como ponto de partida
- [ ] Modo de apresentação ativado (F11)
- [ ] Tela em 1920×1080 px ou maior
- [ ] Slicers sem filtros ativos (estado neutro)
- [ ] Segundo monitor configurado se for apresentação presencial

---

*Roteiro Demo Power BI — Aurora Finance Intelligence*
