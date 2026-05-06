# Power Query — Aurora Finance Intelligence
## Instruções de Importação e Transformação de Dados

> **Onde aplicar:** Power BI Desktop → Transformar Dados (Power Query Editor)

---

## 1. Importar CSVs

### Passo a passo para cada CSV:

1. **Página Inicial → Obter Dados → Texto/CSV**
2. Selecione o arquivo desejado
3. Verifique o delimitador (deve ser `,` vírgula)
4. Verifique a codificação (use **UTF-8** se houver caracteres especiais)
5. Clique em **Transformar Dados** — não clique em "Carregar" diretamente
6. No Editor do Power Query, aplique as transformações abaixo
7. Ao terminar todos, clique em **Fechar e Aplicar**

---

## 2. Transformações por tabela

### 2.1 `clientes_limpo` (dados/processed/clientes_limpo.csv)

No Power Query, selecione a coluna e aplique o tipo correto via **Transformar → Tipo de Dados**:

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `cliente_id` | Texto | Clique com direito → Alterar Tipo → Texto |
| `customer_id_original` | Número Inteiro | |
| `nome` | Texto | |
| `idade` | Número Inteiro | |
| `genero` | Texto | |
| `cidade` | Texto | |
| `estado` | Texto | |
| `renda_mensal` | Número Decimal | Usar "Usando Localidade" → Inglês (EUA) |
| `saldo_atual` | Número Decimal | Usar "Usando Localidade" → Inglês (EUA) |
| `score_credito` | Número Inteiro | |
| `tempo_relacionamento` | Número Inteiro | |
| `produtos_ativos` | Número Inteiro | |
| `tem_cartao_credito` | Número Inteiro | |
| `membro_ativo` | Número Inteiro | |
| `perfil_risco` | Texto | |
| `data_cadastro` | Data | |
| `churn_flag` | Número Inteiro | |
| `origem_dado` | Texto | |

**Código M equivalente** (colar no Editor Avançado):
```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"cliente_id", type text},
    {"customer_id_original", Int64.Type},
    {"nome", type text},
    {"idade", Int64.Type},
    {"genero", type text},
    {"cidade", type text},
    {"estado", type text},
    {"renda_mensal", type number},
    {"saldo_atual", type number},
    {"score_credito", Int64.Type},
    {"tempo_relacionamento", Int64.Type},
    {"produtos_ativos", Int64.Type},
    {"tem_cartao_credito", Int64.Type},
    {"membro_ativo", Int64.Type},
    {"perfil_risco", type text},
    {"data_cadastro", type date},
    {"churn_flag", Int64.Type},
    {"origem_dado", type text}
})
```

---

### 2.2 `transacoes_limpo` (dados/processed/transacoes_limpo.csv)

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `transacao_id` | Texto | |
| `cliente_id` | **Texto** | ⚠️ CRÍTICO: deve ser Texto para relacionamento |
| `data` | **Data** | Formato YYYY-MM-DD → tipo Data |
| `tipo` | Texto | Valores: Debito, Credito, Pix, Transferencia |
| `categoria_id` | **Texto** | ⚠️ CRÍTICO: deve ser Texto para relacionamento |
| `valor` | **Número Decimal** | |
| `descricao` | Texto | |
| `canal` | Texto | |
| `ano_mes` | Texto | Manter como texto (ex: "2024-05") |
| `flag_outlier` | Número Inteiro | |

**Código M equivalente:**
```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"transacao_id", type text},
    {"cliente_id", type text},
    {"data", type date},
    {"tipo", type text},
    {"categoria_id", type text},
    {"valor", type number},
    {"descricao", type text},
    {"canal", type text},
    {"ano_mes", type text},
    {"flag_outlier", Int64.Type}
})
```

> **Atenção:** Se `data` não converter corretamente, use: **Transformar → Coluna de Data → Usando Localidade → Inglês (EUA)** para formato YYYY-MM-DD.

---

### 2.3 `categorias_limpo` (dados/processed/categorias_limpo.csv)

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `categoria_id` | **Texto** | ⚠️ CRÍTICO: deve ser Texto para relacionamento |
| `nome_categoria` | Texto | |
| `tipo_macro` | Texto | |
| `descricao` | Texto | |

```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"categoria_id", type text},
    {"nome_categoria", type text},
    {"tipo_macro", type text},
    {"descricao", type text}
})
```

---

### 2.4 `predicoes_churn` (dados/outputs/predicoes_churn.csv)

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `cliente_id` | **Texto** | ⚠️ CRÍTICO |
| `customer_id_original` | Número Inteiro | |
| `nome` | Texto | |
| `estado` | Texto | |
| `perfil_risco` | Texto | |
| `origem_dado` | Texto | |
| `renda_mensal` | Número Decimal | |
| `saldo_atual` | Número Decimal | |
| `churn_real` | Número Inteiro | |
| `prob_churn` | **Número Decimal** | Valores entre 0 e 1 |
| `predicao_churn` | **Número Inteiro** | 0 ou 1 |
| `risco` | **Texto** | "Alto", "Medio", "Baixo" |
| `recomendacao` | Texto | |

```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"cliente_id", type text},
    {"customer_id_original", Int64.Type},
    {"nome", type text},
    {"estado", type text},
    {"perfil_risco", type text},
    {"origem_dado", type text},
    {"renda_mensal", type number},
    {"saldo_atual", type number},
    {"churn_real", Int64.Type},
    {"prob_churn", type number},
    {"predicao_churn", Int64.Type},
    {"risco", type text},
    {"recomendacao", type text}
})
```

---

### 2.5 `feature_importance` (dados/outputs/feature_importance.csv)

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `feature` | Texto | Nome da feature do modelo |
| `importance` | **Número Decimal** | Score de importância |

```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"feature", type text},
    {"importance", type number}
})
```

---

### 2.6 `threshold_analysis` (dados/outputs/threshold_analysis.csv)

| Coluna | Tipo Power Query | Observação |
|--------|-----------------|------------|
| `threshold` | **Número Decimal** | Valores: 0.3, 0.4, 0.5 |
| `accuracy` | Número Decimal | |
| `precision` | **Número Decimal** | |
| `recall` | **Número Decimal** | |
| `f1_score` | **Número Decimal** | |
| `alert_rate` | Número Decimal | |
| `retention_score` | Número Decimal | |

```m
= Table.TransformColumnTypes(#"Etapa anterior", {
    {"threshold", type number},
    {"accuracy", type number},
    {"precision", type number},
    {"recall", type number},
    {"f1_score", type number},
    {"alert_rate", type number},
    {"retention_score", type number}
})
```

---

## 3. Importar metricas_modelo.json

O JSON tem estrutura de campos-chave. Precisamos transformá-lo em tabela de pares `metrica / valor`.

### Passo a passo:

1. **Obter Dados → JSON**
2. Selecione `dados/outputs/metricas_modelo.json`
3. No Power Query, o JSON aparecerá como um registro (`Record`)
4. Clique em **Para Tabela** (botão no canto superior esquerdo)
5. Isso cria duas colunas: `Name` e `Value`
6. Renomeie `Name` → `metrica` e `Value` → `valor`
7. Remova linhas onde `valor` não é numérico (ex: strings de explicação):
   - Selecione `valor` → Filtrar → desmarcar textos longos
8. Converta `valor` para **Número Decimal**
9. Renomeie a consulta para `metricas_modelo`

**Linhas que devem permanecer após filtro:**

| metrica | valor |
|---------|-------|
| accuracy | 0.8765 |
| precision | 0.66 |
| recall | 0.8108 |
| f1_score | 0.7277 |
| roc_auc | 0.9288 |
| baseline_churn_rate | 0.2037 |
| threshold_used | 0.4 |

**Código M para transformação completa:**
```m
let
    Fonte = Json.Document(File.Contents("CAMINHO\dados\outputs\metricas_modelo.json")),
    ParaTabela = Record.ToTable(Fonte),
    RenomearColunas = Table.RenameColumns(ParaTabela, {{"Name", "metrica"}, {"Value", "valor"}}),
    FiltrarNumericos = Table.SelectRows(RenomearColunas, each Value.Is([valor], type number)),
    ConverterTipo = Table.TransformColumnTypes(FiltrarNumericos, {{"valor", type number}})
in
    ConverterTipo
```

> **Substitua** `CAMINHO` pelo caminho absoluto da pasta do projeto no seu computador.

---

## 4. Verificações finais no Power Query

Antes de "Fechar e Aplicar", verifique:

- [ ] Nenhuma coluna com ícone de erro (⚠️) na barra de cabeçalho
- [ ] `cliente_id` é **ABC** (texto) em `clientes_limpo`, `transacoes_limpo` e `predicoes_churn`
- [ ] `categoria_id` é **ABC** (texto) em `categorias_limpo` e `transacoes_limpo`
- [ ] `data` em `transacoes_limpo` tem ícone de calendário (📅)
- [ ] `valor`, `prob_churn`, `importance` têm ícone de número decimal (1.2)
- [ ] `churn_flag`, `predicao_churn` têm ícone de número inteiro (123)
- [ ] Nenhuma tabela tem linhas com erro (verificar barra de status inferior)

---

## 5. Dicas de diagnóstico

**Problema:** `categoria_id` aparece como número e não conecta com categorias
**Solução:** Selecionar a coluna → Transformar → Tipo de Dados → Texto

**Problema:** Datas aparecem em formato americano (MM/DD/YYYY)
**Solução:** Selecionar coluna `data` → Alterar Tipo → Usando Localidade → selecionar "Inglês (EUA)" e tipo Data

**Problema:** Valores decimais com ponto (`.`) não carregam como número
**Solução:** Selecionar coluna → Alterar Tipo → Usando Localidade → Inglês (EUA)

**Problema:** JSON de métricas não filtra corretamente
**Solução:** Verificar se a coluna `valor` contém listas ou records aninhados; expandir se necessário antes de filtrar

---

*Power Query — Aurora Finance Intelligence*
