DROP TABLE IF EXISTS predicoes_churn;
DROP TABLE IF EXISTS base_modelagem;
DROP TABLE IF EXISTS transacoes;
DROP TABLE IF EXISTS categorias;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    cliente_id TEXT PRIMARY KEY,
    customer_id_original TEXT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    genero TEXT,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    renda_mensal REAL NOT NULL,
    saldo_atual REAL NOT NULL,
    score_credito INTEGER NOT NULL,
    tempo_relacionamento INTEGER NOT NULL,
    produtos_ativos INTEGER NOT NULL,
    tem_cartao_credito INTEGER NOT NULL,
    membro_ativo INTEGER NOT NULL,
    perfil_risco TEXT,
    data_cadastro DATE NOT NULL,
    churn_flag INTEGER NOT NULL DEFAULT 0,
    origem_dado TEXT NOT NULL
);

CREATE TABLE categorias (
    categoria_id INTEGER PRIMARY KEY,
    nome_categoria TEXT NOT NULL,
    tipo_macro TEXT NOT NULL,
    descricao TEXT
);

CREATE TABLE transacoes (
    transacao_id TEXT PRIMARY KEY,
    cliente_id TEXT NOT NULL REFERENCES clientes(cliente_id),
    data DATE NOT NULL,
    tipo TEXT NOT NULL,
    categoria_id INTEGER NOT NULL REFERENCES categorias(categoria_id),
    valor REAL NOT NULL,
    descricao TEXT,
    canal TEXT,
    ano_mes TEXT,
    flag_outlier INTEGER
);

CREATE TABLE base_modelagem (
    cliente_id TEXT PRIMARY KEY REFERENCES clientes(cliente_id),
    customer_id_original TEXT,
    nome TEXT NOT NULL,
    idade INTEGER NOT NULL,
    genero TEXT,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL,
    renda_mensal REAL NOT NULL,
    saldo_atual REAL NOT NULL,
    score_credito INTEGER NOT NULL,
    tempo_relacionamento INTEGER NOT NULL,
    produtos_ativos INTEGER NOT NULL,
    tem_cartao_credito INTEGER NOT NULL,
    membro_ativo INTEGER NOT NULL,
    perfil_risco TEXT,
    data_cadastro DATE NOT NULL,
    churn_flag INTEGER NOT NULL,
    origem_dado TEXT NOT NULL,
    qtd_transacoes INTEGER,
    valor_total REAL,
    ticket_medio REAL,
    desvio_valor REAL,
    maior_transacao REAL,
    menor_transacao REAL,
    ultimo_movimento DATE,
    primeira_transacao DATE,
    qtd_outliers INTEGER,
    dias_desde_ultima_transacao INTEGER,
    meses_atividade INTEGER,
    valor_credito REAL,
    valor_debito REAL,
    valor_pix REAL,
    valor_transferencia REAL,
    valor_macro_essencial REAL,
    valor_macro_financeiro REAL,
    valor_macro_investimento REAL,
    valor_macro_lazer REAL,
    valor_macro_outros REAL,
    pct_canal_digital REAL,
    meses_relacionamento INTEGER,
    media_mensal REAL,
    desvio_mensal REAL,
    pico_mensal REAL,
    razao_saldo_renda REAL,
    gasto_total_saida REAL,
    pressao_financeira REAL,
    intensidade_credito REAL,
    razao_gasto_renda REAL,
    pct_essencial REAL,
    pct_financeiro REAL,
    pct_investimento REAL,
    pct_lazer REAL,
    pct_outros REAL
);

CREATE TABLE predicoes_churn (
    cliente_id TEXT PRIMARY KEY REFERENCES clientes(cliente_id),
    customer_id_original TEXT,
    nome TEXT NOT NULL,
    estado TEXT NOT NULL,
    perfil_risco TEXT,
    origem_dado TEXT NOT NULL,
    renda_mensal REAL NOT NULL,
    saldo_atual REAL NOT NULL,
    churn_real INTEGER,
    prob_churn REAL NOT NULL,
    predicao_churn INTEGER NOT NULL,
    risco TEXT NOT NULL,
    recomendacao TEXT
);

CREATE INDEX idx_transacoes_cliente ON transacoes (cliente_id);
CREATE INDEX idx_transacoes_data ON transacoes (data);
CREATE INDEX idx_transacoes_categoria ON transacoes (categoria_id);
CREATE INDEX idx_clientes_estado ON clientes (estado);
CREATE INDEX idx_clientes_origem ON clientes (origem_dado);
