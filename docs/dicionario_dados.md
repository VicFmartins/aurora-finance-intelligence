# Dicionario de Dados

## clientes

| Campo | Tipo | Descricao |
| --- | --- | --- |
| cliente_id | string | Identificador interno padronizado no formato `C000001` |
| customer_id_original | string | `CustomerId` original do Kaggle, quando existir |
| nome | string | Sobrenome do cliente vindo de `Surname` ou nome sintetico |
| idade | inteiro | Idade em anos |
| genero | string | `Feminino`, `Masculino` ou `Nao informado` |
| cidade | string | Cidade derivada da geografia publica ou cidade sintetica |
| estado | string | Localizacao principal, como `Franca`, `Espanha` ou `Alemanha` |
| renda_mensal | float | Salario estimado mensal, derivado de `EstimatedSalary / 12` quando publico |
| saldo_atual | float | Saldo atual do cliente |
| score_credito | inteiro | Score de credito |
| tempo_relacionamento | inteiro | Tempo de relacionamento derivado de `Tenure` |
| produtos_ativos | inteiro | Numero de produtos ativos |
| tem_cartao_credito | inteiro | 1 para cliente com cartao de credito, 0 caso contrario |
| membro_ativo | inteiro | 1 para cliente ativo, 0 para inativo |
| perfil_risco | string | `Conservador`, `Moderado` ou `Arrojado` |
| data_cadastro | data | Data sintetica e reprodutivel baseada em relacionamento |
| churn_flag | inteiro | 1 para churn, 0 para ativo |
| origem_dado | string | `public_kaggle_churn_modelling` ou `synthetic_fallback` |

## categorias

Categorias geradas pela camada sintetica:

- `Alimentacao`
- `Moradia`
- `Transporte`
- `Saude`
- `Educacao`
- `Lazer`
- `Assinaturas`
- `Investimentos`
- `Servicos Financeiros`
- `Outros`

## transacoes

| Campo | Tipo | Descricao |
| --- | --- | --- |
| transacao_id | string | Chave unica da transacao |
| cliente_id | string | Referencia ao cliente |
| data | data | Data da transacao |
| tipo | string | `Credito`, `Debito`, `Transferencia` ou `Pix` |
| categoria_id | inteiro | Categoria associada |
| valor | float | Valor monetario |
| descricao | string | Descricao sintetica da transacao |
| canal | string | Canal de uso, como app, internet banking, cartao, PIX ou agencia |
| ano_mes | string | Competencia derivada da data |
| flag_outlier | inteiro | Marcacao de outlier por IQR |

## base_modelagem

Campos analiticos relevantes:

- `tempo_relacionamento`
- `qtd_transacoes`
- `valor_total`
- `ticket_medio`
- `dias_desde_ultima_transacao`
- `pressao_financeira`
- `razao_saldo_renda`
- `intensidade_credito`
- `pct_essencial`
- `pct_lazer`
- `pct_investimento`
- `pct_canal_digital`
- `origem_dado`

## predicoes_churn

| Campo | Tipo | Descricao |
| --- | --- | --- |
| cliente_id | string | Identificador interno do cliente |
| customer_id_original | string | Identificador original do Kaggle, se existir |
| nome | string | Nome exibido no ranking |
| estado | string | Localizacao principal do cliente |
| perfil_risco | string | Perfil de risco |
| origem_dado | string | Origem da base de clientes |
| prob_churn | float | Probabilidade prevista pelo modelo |
| predicao_churn | inteiro | Classe final conforme threshold recomendado |
| risco | string | `Baixo`, `Medio` ou `Alto` |
| recomendacao | string | Acao sugerida para retencao |
