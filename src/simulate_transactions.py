from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .config import MAX_TRANSACOES_POR_CLIENTE, MIN_TRANSACOES_POR_CLIENTE, SEED

CATEGORIAS = [
    {"categoria_id": 1, "nome_categoria": "Alimentacao", "tipo_macro": "Essencial", "descricao": "Mercado, feira e refeicoes do dia a dia"},
    {"categoria_id": 2, "nome_categoria": "Moradia", "tipo_macro": "Essencial", "descricao": "Aluguel, contas e manutencao residencial"},
    {"categoria_id": 3, "nome_categoria": "Transporte", "tipo_macro": "Essencial", "descricao": "Combustivel, transporte publico e mobilidade"},
    {"categoria_id": 4, "nome_categoria": "Saude", "tipo_macro": "Essencial", "descricao": "Farmacia, consultas e cuidados medicos"},
    {"categoria_id": 5, "nome_categoria": "Educacao", "tipo_macro": "Essencial", "descricao": "Cursos, escola e desenvolvimento profissional"},
    {"categoria_id": 6, "nome_categoria": "Lazer", "tipo_macro": "Lazer", "descricao": "Restaurantes, viagens e entretenimento"},
    {"categoria_id": 7, "nome_categoria": "Assinaturas", "tipo_macro": "Lazer", "descricao": "Streaming, apps e servicos recorrentes"},
    {"categoria_id": 8, "nome_categoria": "Investimentos", "tipo_macro": "Investimento", "descricao": "Aportes, poupanca e carteira financeira"},
    {"categoria_id": 9, "nome_categoria": "Servicos Financeiros", "tipo_macro": "Financeiro", "descricao": "Tarifas, seguros e operacoes de credito"},
    {"categoria_id": 10, "nome_categoria": "Outros", "tipo_macro": "Outros", "descricao": "Despesas diversas e compras ocasionais"},
]

TRANS_TYPES = ["Credito", "Debito", "Transferencia", "Pix"]
CHANNELS = ["App Mobile", "Internet Banking", "Cartao", "PIX", "Agencia"]
RISK_PROFILE_SCORES = {"Conservador": -0.10, "Moderado": 0.08, "Arrojado": 0.18}


def sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


def build_categories() -> pd.DataFrame:
    return pd.DataFrame(CATEGORIAS)


def classify_risk_profile(
    score_credito: float,
    saldo_atual: float,
    renda_mensal: float,
    churn_flag: int,
    membro_ativo: int,
) -> str:
    pontos = 0
    if score_credito >= 740:
        pontos += 2
    elif score_credito >= 640:
        pontos += 1
    else:
        pontos -= 1

    if renda_mensal > 0:
        razao_saldo = saldo_atual / renda_mensal
        if razao_saldo >= 2.4:
            pontos += 1
        elif razao_saldo <= 0.5:
            pontos -= 1

    if churn_flag == 1:
        pontos -= 1
    if membro_ativo == 1:
        pontos += 1

    if pontos <= 0:
        return "Conservador"
    if pontos >= 3:
        return "Arrojado"
    return "Moderado"


def generate_transactions(
    clientes: pd.DataFrame,
    categorias: pd.DataFrame,
    np_rng: np.random.Generator,
    use_churn_signal: bool = True,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    start = datetime(2024, 1, 1)
    end = datetime(2025, 4, 30)
    total_days = (end - start).days
    categorias_records = categorias.to_dict(orient="records")

    tx_id = 1
    for cliente in clientes.itertuples(index=False):
        renda = float(cliente.renda_mensal)
        saldo = float(cliente.saldo_atual)
        idade = int(cliente.idade)
        churn_flag = int(getattr(cliente, "churn_flag", 0))
        effective_churn_flag = churn_flag if use_churn_signal else 0
        membro_ativo = int(getattr(cliente, "membro_ativo", 1))
        produtos_ativos = int(getattr(cliente, "produtos_ativos", 2))
        score_credito = float(getattr(cliente, "score_credito", 650))
        tem_cartao_credito = int(getattr(cliente, "tem_cartao_credito", 1))
        tempo_relacionamento = int(getattr(cliente, "tempo_relacionamento", 3))

        base_volume = int(np_rng.integers(MIN_TRANSACOES_POR_CLIENTE, MAX_TRANSACOES_POR_CLIENTE + 1))
        volume_adjustment = 0
        volume_adjustment += 2 if membro_ativo == 1 else -3
        volume_adjustment += 1 if produtos_ativos >= 3 else -1 if produtos_ativos <= 1 else 0
        volume_adjustment += 1 if tempo_relacionamento >= 5 else 0
        volume_adjustment += -4 if effective_churn_flag == 1 else 1
        volume = int(np.clip(base_volume + volume_adjustment, 10, MAX_TRANSACOES_POR_CLIENTE + 10))

        renda_segura = max(renda, 1000.0)
        stress_score = float(
            np.clip(
                0.30
                + (0.22 if effective_churn_flag == 1 else 0.0)
                + (0.12 if membro_ativo == 0 else -0.03)
                + max(0.0, 0.9 - (saldo / max(renda_segura, 1.0))) * 0.14
                + max(0.0, 650 - score_credito) / 1000,
                0.08,
                0.92,
            )
        )
        digital_score = float(
            np.clip(
                0.42
                + (0.20 if membro_ativo == 1 else -0.08)
                + (0.06 if idade < 35 else -0.05 if idade > 58 else 0.0)
                + (0.04 if produtos_ativos >= 3 else 0.0),
                0.12,
                0.96,
            )
        )

        for _ in range(volume):
            if effective_churn_flag == 1 and np_rng.random() < 0.72:
                sampled_days = int(np_rng.integers(0, max(total_days - 55, 1)))
            else:
                sampled_days = int(np_rng.integers(0, total_days + 1))
            data_tx = start + timedelta(days=sampled_days)
            tipo = str(np_rng.choice(TRANS_TYPES, p=[0.17, 0.39, 0.18, 0.26]))

            weights = []
            for categoria in categorias_records:
                macro = categoria["tipo_macro"]
                if tipo == "Credito":
                    if categoria["categoria_id"] == 9:
                        weight = 0.29
                    elif macro == "Investimento":
                        weight = 0.22 + (0.06 if score_credito >= 700 else -0.04 if effective_churn_flag == 1 else 0.0)
                    else:
                        weight = 0.49 / 7
                elif macro == "Essencial":
                    weight = 0.24 + (0.04 if effective_churn_flag == 1 else 0.0)
                elif macro == "Lazer":
                    weight = max(0.06, 0.19 - stress_score * 0.09 - (0.03 if effective_churn_flag == 1 else 0.0))
                elif macro == "Investimento":
                    weight = max(
                        0.04,
                        0.17
                        - stress_score * 0.08
                        + (0.05 if score_credito >= 700 else -0.04)
                        - (0.04 if effective_churn_flag == 1 else 0.0),
                    )
                elif macro == "Financeiro":
                    weight = 0.12 + (0.03 if effective_churn_flag == 1 else 0.0)
                else:
                    weight = 0.08
                weights.append(weight)

            probs = np.array(weights, dtype=float)
            probs = probs / probs.sum()
            categoria = categorias_records[int(np_rng.choice(np.arange(len(categorias_records)), p=probs))]
            macro = categoria["tipo_macro"]

            if tipo == "Credito":
                multiplier = 0.58 if effective_churn_flag == 1 else 0.66
                valor = float(np_rng.normal(loc=renda_segura * multiplier, scale=renda_segura * 0.13))
            elif macro == "Investimento":
                base = max(renda_segura * (0.10 if effective_churn_flag == 1 else 0.16), 150.0)
                valor = float(np_rng.normal(loc=base, scale=max(base * 0.28, 55.0)))
            elif macro == "Essencial":
                base = max(renda_segura * (0.13 if effective_churn_flag == 1 else 0.11), 100.0)
                valor = float(np_rng.normal(loc=base, scale=max(base * 0.26, 30.0)))
            elif macro == "Lazer":
                base = max(renda_segura * (0.06 if effective_churn_flag == 1 else 0.08), 70.0)
                valor = float(np_rng.normal(loc=base, scale=max(base * 0.30, 22.0)))
            else:
                base = max(renda_segura * (0.08 if effective_churn_flag == 1 else 0.06), 50.0)
                valor = float(np_rng.normal(loc=base, scale=max(base * 0.25, 18.0)))

            channel_weights = np.array(
                [
                    0.30 + digital_score * 0.14,
                    0.14 + digital_score * 0.08,
                    0.19 + (0.10 if tem_cartao_credito == 1 else -0.06),
                    0.17 + digital_score * 0.11,
                    0.20 - digital_score * 0.18 - (0.04 if tem_cartao_credito == 1 else 0.0),
                ],
                dtype=float,
            )
            channel_weights = np.clip(channel_weights, 0.04, None)
            channel_weights = channel_weights / channel_weights.sum()

            rows.append(
                {
                    "transacao_id": f"T{tx_id:07d}",
                    "cliente_id": cliente.cliente_id,
                    "data": data_tx.date().isoformat(),
                    "tipo": tipo,
                    "categoria_id": int(categoria["categoria_id"]),
                    "valor": round(max(8.0, valor), 2),
                    "descricao": categoria["descricao"],
                    "canal": str(np_rng.choice(CHANNELS, p=channel_weights)),
                }
            )
            tx_id += 1

    transacoes = pd.DataFrame(rows)
    if not transacoes.empty:
        canal_missing = max(20, len(transacoes) // 120)
        descricao_missing = max(20, len(transacoes) // 150)
        transacoes.loc[np_rng.choice(transacoes.index, size=min(canal_missing, len(transacoes)), replace=False), "canal"] = np.nan
        transacoes.loc[np_rng.choice(transacoes.index, size=min(descricao_missing, len(transacoes)), replace=False), "descricao"] = np.nan
        duplicatas = transacoes.sample(n=max(8, len(transacoes) // 4500), random_state=SEED)
        transacoes = pd.concat([transacoes, duplicatas], ignore_index=True)

    return transacoes


def assign_synthetic_churn(clientes: pd.DataFrame, transacoes: pd.DataFrame, categorias: pd.DataFrame) -> pd.DataFrame:
    tx = transacoes.rename(columns={"tipo": "tipo_transacao"}).copy()
    tx["data"] = pd.to_datetime(tx["data"])
    tx = tx.merge(categorias[["categoria_id", "tipo_macro"]], on="categoria_id", how="left")

    referencia = tx["data"].max() + pd.Timedelta(days=1)
    agregado = (
        tx.groupby("cliente_id")
        .agg(
            qtd_transacoes=("transacao_id", "count"),
            ultimo_movimento=("data", "max"),
            total_credito=("valor", lambda s: s[tx.loc[s.index, "tipo_transacao"].eq("Credito")].sum()),
            total_saida=("valor", lambda s: s[~tx.loc[s.index, "tipo_transacao"].eq("Credito")].sum()),
            valor_essencial=("valor", lambda s: s[tx.loc[s.index, "tipo_macro"].eq("Essencial")].sum()),
            valor_investimento=("valor", lambda s: s[tx.loc[s.index, "tipo_macro"].eq("Investimento")].sum()),
            qtd_digital=("canal", lambda s: s.fillna("").str.contains("App|Internet|PIX", regex=True).sum()),
        )
        .reset_index()
    )
    agregado["dias_sem_movimento"] = (referencia - agregado["ultimo_movimento"]).dt.days
    agregado["pct_digital"] = agregado["qtd_digital"] / agregado["qtd_transacoes"].clip(lower=1)
    agregado["share_essencial"] = agregado["valor_essencial"] / agregado["total_saida"].replace(0, np.nan)
    agregado["share_investimento"] = agregado["valor_investimento"] / agregado["total_saida"].replace(0, np.nan)
    agregado = agregado.fillna(0)

    base = clientes.merge(agregado, on="cliente_id", how="left").fillna(
        {
            "qtd_transacoes": 0,
            "dias_sem_movimento": 120,
            "pct_digital": 0,
            "share_essencial": 0,
            "share_investimento": 0,
            "total_credito": 0,
            "total_saida": 0,
        }
    )
    saldo_renda = base["saldo_atual"] / base["renda_mensal"].replace(0, np.nan)
    pressao = (base["total_saida"] - base["total_credito"]) / base["renda_mensal"].replace(0, np.nan)
    perfil_score = base["perfil_risco"].map(RISK_PROFILE_SCORES).fillna(0.05)

    logits = (
        -0.95
        + 0.020 * base["dias_sem_movimento"]
        + 0.64 * np.clip(pressao.fillna(0), -1.5, 3.0)
        - 0.48 * np.clip(saldo_renda.fillna(0), 0, 6)
        + 0.54 * np.clip(base["share_essencial"], 0, 1)
        - 0.56 * np.clip(base["share_investimento"], 0, 1)
        - 0.28 * np.clip(base["pct_digital"], 0, 1)
        - 0.0018 * base["score_credito"].fillna(650)
        - 0.12 * base["membro_ativo"].fillna(1)
        + 0.08 * np.clip(3 - base["produtos_ativos"].fillna(2), 0, 2)
        + 0.05 * np.clip(base["tem_cartao_credito"].fillna(1), 0, 1)
        + perfil_score
    )
    rng = np.random.default_rng(SEED)
    churn = rng.binomial(1, np.clip(sigmoid(logits.to_numpy(dtype=float)), 0.03, 0.88))

    resultado = clientes.copy()
    resultado["churn_flag"] = churn
    resultado["perfil_risco"] = [
        classify_risk_profile(score, saldo, renda, churn_flag, membro)
        for score, saldo, renda, churn_flag, membro in zip(
            resultado["score_credito"],
            resultado["saldo_atual"],
            resultado["renda_mensal"],
            resultado["churn_flag"],
            resultado["membro_ativo"],
            strict=True,
        )
    ]
    return resultado
