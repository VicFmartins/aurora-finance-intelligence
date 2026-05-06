# Modelagem de Dados — Aurora Finance Intelligence

## Visão Geral do Modelo

O modelo segue uma arquitetura **estrela (Star Schema)** com `clientes_limpo` como tabela central de fatos/dimensão e as demais tabelas conectadas a ela.

```
categorias_limpo ────────────────────────────────────────────
       │                                                     │
       │ [categoria_id]                              (via transacoes)
       ▼                                                     │
transacoes_limpo ◄──── [cliente_id] ──── clientes_limpo ────┤
                                               │             │
                                               │ [cliente_id]│
                                               ▼             │
                                      predicoes_churn ◄──────┘
                                               │
                                               │ (standalone)
                                      feature_importance
                                      threshold_analysis
                                      metricas_modelo
```

---

## Tabelas e Relacionamentos

### Relacionamento 1: Clientes ↔ Transações
| Campo | Tabela | Tipo |
|-------|--------|------|
| `cliente_id` | `clientes_limpo` | Chave primária (1) |
| `cliente_id` | `transacoes_limpo` | Chave estrangeira (N) |

- **Cardinalidade:** Um para Muitos (1:N)
- **Direção do filtro:** Simples → de `clientes_limpo` para `transacoes_limpo`
- **Ativo:** Sim
- **Interpretação:** Um cliente pode ter muitas transações

**Como criar no Power BI:**
1. Vá em **Modelagem → Gerenciar Relacionamentos → Novo**
2. Tabela 1: `clientes_limpo` → Coluna: `cliente_id`
3. Tabela 2: `transacoes_limpo` → Coluna: `cliente_id`
4. Cardinalidade: `Um para Muitos (1:*)`
5. Direção do filtro cruzado: `Simples`

---

### Relacionamento 2: Categorias ↔ Transações
| Campo | Tabela | Tipo |
|-------|--------|------|
| `categoria_id` | `categorias_limpo` | Chave primária (1) |
| `categoria_id` | `transacoes_limpo` | Chave estrangeira (N) |

- **Cardinalidade:** Um para Muitos (1:N)
- **Direção do filtro:** Simples → de `categorias_limpo` para `transacoes_limpo`
- **Ativo:** Sim
- **Interpretação:** Uma categoria engloba muitas transações

**Como criar no Power BI:**
1. Tabela 1: `categorias_limpo` → Coluna: `categoria_id`
2. Tabela 2: `transacoes_limpo` → Coluna: `categoria_id`
3. Cardinalidade: `Um para Muitos (1:*)`
4. Direção do filtro cruzado: `Simples`

---

### Relacionamento 3: Clientes ↔ Predições de Churn
| Campo | Tabela | Tipo |
|-------|--------|------|
| `cliente_id` | `clientes_limpo` | Chave primária (1) |
| `cliente_id` | `predicoes_churn` | Chave estrangeira (1) |

- **Cardinalidade:** Um para Um (1:1)
- **Direção do filtro:** Ambos (bidirecional)
- **Ativo:** Sim
- **Interpretação:** Cada cliente tem exatamente uma predição de churn

**Como criar no Power BI:**
1. Tabela 1: `clientes_limpo` → Coluna: `cliente_id`
2. Tabela 2: `predicoes_churn` → Coluna: `cliente_id`
3. Cardinalidade: `Um para Um (1:1)`
4. Direção do filtro cruzado: `Ambos`

---

### Tabelas Independentes (sem relacionamento)

| Tabela | Motivo | Como usar |
|--------|--------|-----------|
| `feature_importance` | Contém features do modelo ML, sem ligação com clientes individuais | Usar isolada em visuais da Página 4 |
| `threshold_analysis` | Análise de thresholds por ponto de corte, nível agregado | Usar isolada em visuais da Página 4 |
| `metricas_modelo` | Métricas globais do modelo (AUC, F1, etc.) | Usar via medidas DAX |

---

## Estrutura Esperada de Cada Tabela

### clientes_limpo
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `cliente_id` | Texto | Identificador único do cliente |
| `customer_id_original` | Número Inteiro | ID original do Kaggle |
| `nome` | Texto | Nome do cliente |
| `idade` | Número Inteiro | Idade |
| `genero` | Texto | Gênero |
| `cidade` | Texto | Cidade |
| `estado` | Texto | País/região (França, Alemanha, Espanha) |
| `renda_mensal` | Número Decimal | Renda estimada (R$) |
| `saldo_atual` | Número Decimal | Saldo atual (R$) |
| `score_credito` | Número Inteiro | Score de crédito |
| `tempo_relacionamento` | Número Inteiro | Anos como cliente |
| `produtos_ativos` | Número Inteiro | Qtd de produtos |
| `tem_cartao_credito` | Número Inteiro | Possui cartão (0/1) |
| `membro_ativo` | Número Inteiro | Membro ativo (0/1) |
| `perfil_risco` | Texto | Conservador, Moderado, Arrojado |
| `data_cadastro` | Data | Data de cadastro |
| `churn_flag` | Número Inteiro | Churn real (0/1) |
| `origem_dado` | Texto | Fonte do dado |

### transacoes_limpo
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `transacao_id` | Texto | ID da transação |
| `cliente_id` | Texto | FK para clientes_limpo |
| `categoria_id` | Texto | FK para categorias_limpo |
| `data` | Data | Data da transação |
| `valor` | Número Decimal | Valor em R$ |
| `tipo` | Texto | "Debito", "Credito", "Pix", "Transferencia" |
| `canal` | Texto | "App Mobile", "Internet Banking", "PIX", "Cartao", "Agencia" |
| `descricao` | Texto | Descrição da transação |
| `ano_mes` | Texto | Formato "YYYY-MM" |
| `flag_outlier` | Número Inteiro | 1 se outlier detectado |

### categorias_limpo
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `categoria_id` | Texto | ID da categoria |
| `nome_categoria` | Texto | Nome legível |
| `tipo_macro` | Texto | Agrupamento macro |
| `descricao` | Texto | Descrição da categoria |

### predicoes_churn
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `cliente_id` | Texto | FK para clientes_limpo |
| `prob_churn` | Número Decimal | Probabilidade 0-1 |
| `predicao_churn` | Número Inteiro | 1 = churn previsto pelo modelo |
| `churn_real` | Número Inteiro | 1 = churn real (label original) |
| `risco` | Texto | "Alto", "Medio", "Baixo" ⚠️ sem acento em "Medio" |
| `recomendacao` | Texto | Ação de retenção sugerida |

### feature_importance
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `feature` | Texto | Nome da feature |
| `importance` | Número Decimal | Score de importância |

### threshold_analysis
| Coluna | Tipo PBI | Descrição |
|--------|----------|-----------|
| `threshold` | Número Decimal | Ponto de corte |
| `precision` | Número Decimal | Precisão naquele threshold |
| `recall` | Número Decimal | Recall naquele threshold |
| `f1_score` | Número Decimal | F1 naquele threshold |

---

## Erros Comuns e Soluções

### ❌ Erro: "Ambiguidade de relacionamento"
**Causa:** Relacionamento bidirecional entre clientes e predições causando loops.
**Solução:** Se houver warnings, mude a direção do filtro de clientes ↔ predicoes_churn para `Simples`.

### ❌ Erro: "Não é possível determinar um único valor"
**Causa:** Medida DAX tentando retornar múltiplos valores em contexto de filtro errado.
**Solução:** Verifique se o relacionamento está ativo e se está usando CALCULATE corretamente.

### ❌ Erro: "cliente_id não encontrado / Sem correspondências"
**Causa:** `cliente_id` em uma tabela está como número e em outra como texto.
**Solução:** No Power Query, converta AMBAS as colunas `cliente_id` para `Texto` antes de criar o relacionamento.

### ❌ Erro: "Relacionamento inativo"
**Causa:** Power BI detectou mais de um caminho entre duas tabelas.
**Solução:** Use `USERELATIONSHIP()` nas medidas DAX quando precisar ativar um relacionamento inativo pontualmente.

### ❌ Erro: "Dados em branco no visual"
**Causa:** Filtro de contexto não propagou por falta de relacionamento ou tipo de dado diferente.
**Solução:** Confirme que os tipos de dados estão idênticos nos campos de junção (ambos Texto).

---

## Checklist de Modelagem

- [ ] `cliente_id` é **Texto** em todas as tabelas
- [ ] `data` é do tipo **Data** em `transacoes_limpo`
- [ ] `valor` é **Número Decimal** em `transacoes_limpo`
- [ ] `prob_churn` é **Número Decimal** em `predicoes_churn`
- [ ] `churn_flag` é **Número Inteiro** em `predicoes_churn`
- [ ] `risco` é **Texto** em `predicoes_churn`
- [ ] Relacionamento clientes ↔ transações criado (1:N)
- [ ] Relacionamento categorias ↔ transações criado (1:N)
- [ ] Relacionamento clientes ↔ predicoes_churn criado (1:1)
- [ ] Nenhum relacionamento com ambiguidade de loop
- [ ] Tabelas feature_importance e threshold_analysis isoladas
- [ ] metricas_modelo importada como tabela chave-valor

---

*Modelagem de Dados — Aurora Finance Intelligence*
