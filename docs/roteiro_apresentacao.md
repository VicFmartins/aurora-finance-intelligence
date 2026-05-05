# Roteiro de Apresentacao

## Pitch de 5 minutos

### 0:00 a 0:40 | Problema

"Empresas financeiras normalmente descobrem tarde demais que um cliente esta prestes a reduzir relacionamento ou sair. A Aurora nasceu para antecipar esse momento com dados."

### 0:40 a 1:20 | O que e a solucao

"A Aurora Finance Intelligence e uma solucao ponta a ponta que une Python, SQL, Machine Learning, Power BI e uma aplicacao web estatica premium para apoiar retencao."

### 1:20 a 2:10 | Dataset e pipeline

"Usamos como base publica o Churn Modelling do Kaggle. O campo Exited vira nosso target de churn, e o EstimatedSalary foi convertido de anual para renda mensal. Como o dataset nao traz historico transacional por categoria, enriquecemos a base com uma camada sintetica de transacoes reprodutiveis."

### 2:10 a 3:10 | Analise e modelo

"Depois da limpeza e da base de modelagem, treinamos um Random Forest com balanceamento de classe e avaliamos multiplos thresholds. Como churn e um problema de retencao, defendemos o modelo como ferramenta de ranking e priorizacao, nao decisao automatica."

### 3:10 a 4:10 | Produto e BI

"Os artefatos gerados alimentam tanto o Power BI quanto uma aplicacao React estatica com visual de produto real, sem backend obrigatorio e sem dependencia de infraestrutura paga."

### 4:10 a 5:00 | Fechamento

"A Aurora combina dado publico realista com enriquecimento sintetico para transformar sinais financeiros dispersos em acao concreta de retencao. E um projeto tecnicamente completo, visualmente consistente e pronto para evoluir."

## Sugestao de distribuicao por pessoa

- Pessoa 1: problema e visao geral
- Pessoa 2: dataset publico, pipeline e SQL
- Pessoa 3: EDA e insights
- Pessoa 4: modelo de churn
- Pessoa 5: app, Power BI e arquitetura AWS-ready

## Perguntas provaveis

Se a banca perguntar sobre:

- `dataset publico`: explicar que o CSV e local e nao ha download automatico do Kaggle
- `transacoes sinteticas`: defender que o dataset publico nao possui historico transacional por categoria
- `recall`: defender que falso negativo importa em churn
- `precision`: explicar que alerta ruim tambem custa operacao
- `ROC-AUC`: explicar que ele mede capacidade de ranquear risco
- `threshold`: mostrar que a equipe comparou cenarios e escolheu um ponto defensavel para retencao
