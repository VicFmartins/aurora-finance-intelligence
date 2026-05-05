# Dataset publico da Aurora

## Dataset usado

- nome: `Churn Modelling`
- plataforma: `Kaggle`
- arquivo esperado: `dados/raw/churn_modelling.csv`

## Importante

O projeto **nao faz download automatico do Kaggle**, porque isso exigiria autenticacao.

## Comportamento do pipeline

Se `dados/raw/churn_modelling.csv` existir:

- a Aurora carrega o dataset publico
- usa essa base como origem principal dos clientes e do churn
- marca `origem_dado = public_kaggle_churn_modelling`

Se o arquivo nao existir:

- a Aurora usa o fallback sintetico
- marca `origem_dado = synthetic_fallback`
- o comando `python -m src.pipeline` continua funcionando normalmente

## Colunas usadas do Churn Modelling

- `RowNumber`
- `CustomerId`
- `Surname`
- `CreditScore`
- `Geography`
- `Gender`
- `Age`
- `Tenure`
- `Balance`
- `NumOfProducts`
- `HasCrCard`
- `IsActiveMember`
- `EstimatedSalary`
- `Exited`

## Mapeamento para o schema Aurora

| Dataset publico | Aurora |
| --- | --- |
| `CustomerId` | `customer_id_original` e base para rastreabilidade |
| `Surname` | `nome` |
| `Age` | `idade` |
| `Gender` | `genero` |
| `Geography` | `estado` |
| `Geography` | `cidade` quando nao existe cidade real |
| `EstimatedSalary` | `renda_mensal` |
| `Balance` | `saldo_atual` |
| `CreditScore` | `score_credito` |
| `Tenure` | `tempo_relacionamento` |
| `NumOfProducts` | `produtos_ativos` |
| `HasCrCard` | `tem_cartao_credito` |
| `IsActiveMember` | `membro_ativo` |
| `Exited` | `churn_flag` |

## Regras importantes

- `cliente_id` vira string estavel como `C000001`, `C000002`
- `CustomerId` e preservado em `customer_id_original`
- `Surname` e usado como nome do cliente
- `EstimatedSalary` e tratado como salario anual e dividido por 12
- `Geography` e usada como localizacao
- `Exited` e o target de churn
- `data_cadastro` e criada de forma sintetica e reprodutivel com base em `tempo_relacionamento`

## Por que a Aurora ainda gera transacoes

O dataset `Churn Modelling` nao traz historico transacional por categoria. Por isso a Aurora gera uma camada sintetica reprodutivel com:

- categorias financeiras
- transacoes por cliente
- historico temporal
- canais
- valores coerentes com renda, saldo, perfil de risco, membro ativo e churn

Essa abordagem combina dado publico com enriquecimento sintetico para atender Python, SQL, Power BI, ML e storytelling.

No modo publico, a simulacao de transacoes nao usa `Exited` para construir o comportamento financeiro sintetico. Isso foi adotado para reduzir risco de data leakage.
