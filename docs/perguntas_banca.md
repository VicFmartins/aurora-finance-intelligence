# Perguntas da Banca

## Qual dataset publico voces usaram?

Usamos o `Churn Modelling`, do Kaggle, salvo localmente em `dados/raw/churn_modelling.csv`.

## O projeto baixa o Kaggle automaticamente?

Nao. O projeto nao faz download automatico porque o Kaggle exige autenticacao. Por isso a Aurora espera o arquivo localmente.

## O que acontece se o arquivo nao existir?

O pipeline usa o fallback sintetico e continua rodando normalmente.

## Qual e o target de churn?

O target publico e `Exited`, que vira `churn_flag` no schema Aurora.

## O que foi feito com EstimatedSalary?

`EstimatedSalary` foi tratado como salario anual e convertido para `renda_mensal` com divisao por 12.

## O que foi feito com Geography?

`Geography` foi usada como localizacao principal. No schema Aurora, ela alimenta `estado` e tambem `cidade` quando nao existe uma cidade real no dataset.

## O que foi feito com Surname?

`Surname` foi usado como nome ou sobrenome do cliente dentro do schema Aurora.

## Por que ainda existem transacoes sinteticas?

Porque o `Churn Modelling` nao possui historico transacional por categoria. Sem essa camada seria mais dificil demonstrar SQL, comportamento financeiro, Power BI e storytelling.

## Isso enfraquece o projeto?

Nao. Pelo contrario: a Aurora deixa explicito o que vem do dado publico e o que e enriquecimento sintetico. Isso torna a narrativa mais honesta e mais util para o caso de negocio.

## Existe risco de data leakage?

Havia um risco potencial se a camada sintetica usasse diretamente o target `Exited` para moldar transacoes no modo publico. Isso foi evitado: no modo `Churn Modelling`, as transacoes sao geradas a partir de perfil, renda, saldo, produtos e atividade, sem usar o target como motor de simulacao.

## Por que Random Forest?

Porque oferece boa performance inicial, lida bem com relacoes nao lineares e entrega uma baseline forte sem overengineering.

## Por que ajustar threshold?

Porque churn e um problema de retencao. Nao basta olhar a saida padrao do modelo; e importante equilibrar sensibilidade operacional e qualidade dos alertas.

## Como defender precision, recall e ROC-AUC?

- `precision` mostra a qualidade dos alertas
- `recall` mostra a capacidade de capturar clientes que poderiam sair
- `roc_auc` mostra a capacidade do modelo de ranquear risco

Em churn, falso negativo importa porque deixar um cliente de alto risco passar despercebido pode custar relacionamento e receita.

## Isso decide automaticamente quem recebera acao?

Nao. O MVP usa ranking de risco e priorizacao. A decisao final continua humana.
