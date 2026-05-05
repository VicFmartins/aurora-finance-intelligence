-- 1. Validacao de nulos
SELECT
    COUNT(*) AS total_clientes,
    SUM(CASE WHEN renda_mensal IS NULL THEN 1 ELSE 0 END) AS nulos_renda,
    SUM(CASE WHEN saldo_atual IS NULL THEN 1 ELSE 0 END) AS nulos_saldo,
    SUM(CASE WHEN churn_flag IS NULL THEN 1 ELSE 0 END) AS nulos_churn,
    SUM(CASE WHEN score_credito IS NULL THEN 1 ELSE 0 END) AS nulos_score_credito
FROM clientes;

-- 2. Volume e ticket medio por estado
SELECT
    c.estado,
    COUNT(t.transacao_id) AS qtd_transacoes,
    ROUND(SUM(t.valor), 2) AS volume_total,
    ROUND(AVG(t.valor), 2) AS ticket_medio
FROM transacoes t
JOIN clientes c ON c.cliente_id = t.cliente_id
GROUP BY c.estado
ORDER BY volume_total DESC;

-- 3. Top categorias por gasto
SELECT
    cat.nome_categoria,
    ROUND(SUM(CASE WHEN t.tipo <> 'Credito' THEN t.valor ELSE 0 END), 2) AS total_gasto
FROM transacoes t
JOIN categorias cat ON cat.categoria_id = t.categoria_id
GROUP BY cat.nome_categoria
ORDER BY total_gasto DESC
LIMIT 10;

-- 4. Saldo liquido mensal por cliente
SELECT
    cliente_id,
    strftime('%Y-%m', data) AS ano_mes,
    ROUND(SUM(CASE WHEN tipo = 'Credito' THEN valor ELSE -valor END), 2) AS saldo_liquido
FROM transacoes
GROUP BY cliente_id, strftime('%Y-%m', data)
ORDER BY cliente_id, ano_mes;

-- 5. Score de risco por razao gasto/renda
WITH gasto_cliente AS (
    SELECT
        c.cliente_id,
        c.nome,
        c.estado,
        c.renda_mensal,
        SUM(CASE WHEN t.tipo <> 'Credito' THEN t.valor ELSE 0 END) AS total_gastos
    FROM clientes c
    JOIN transacoes t ON t.cliente_id = c.cliente_id
    GROUP BY c.cliente_id, c.nome, c.estado, c.renda_mensal
)
SELECT
    cliente_id,
    nome,
    estado,
    ROUND(total_gastos / NULLIF(renda_mensal, 0), 2) AS score_risco_gasto_renda
FROM gasto_cliente
ORDER BY score_risco_gasto_renda DESC
LIMIT 20;

-- 6. Churn por perfil de risco
SELECT
    perfil_risco,
    COUNT(*) AS qtd_clientes,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct
FROM clientes
GROUP BY perfil_risco
ORDER BY churn_rate_pct DESC;

-- 7. Top clientes para retencao
WITH comportamento AS (
    SELECT
        c.cliente_id,
        c.customer_id_original,
        c.nome,
        c.estado,
        c.perfil_risco,
        julianday('2025-05-01') - julianday(MAX(t.data)) AS dias_sem_movimento,
        SUM(CASE WHEN t.tipo <> 'Credito' THEN t.valor ELSE 0 END) AS total_saidas,
        c.renda_mensal,
        c.churn_flag
    FROM clientes c
    JOIN transacoes t ON t.cliente_id = c.cliente_id
    GROUP BY c.cliente_id, c.customer_id_original, c.nome, c.estado, c.perfil_risco, c.renda_mensal, c.churn_flag
)
SELECT
    cliente_id,
    customer_id_original,
    nome,
    estado,
    perfil_risco,
    churn_flag,
    ROUND(dias_sem_movimento, 0) AS dias_sem_movimento,
    ROUND(total_saidas / NULLIF(renda_mensal, 0), 2) AS pressao_financeira
FROM comportamento
ORDER BY dias_sem_movimento DESC, pressao_financeira DESC
LIMIT 20;

-- 8. Analise por canal de transacao
SELECT
    canal,
    COUNT(*) AS qtd_transacoes,
    ROUND(SUM(valor), 2) AS volume_total,
    ROUND(AVG(valor), 2) AS ticket_medio
FROM transacoes
GROUP BY canal
ORDER BY volume_total DESC;
