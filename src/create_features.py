from __future__ import annotations

import numpy as np
import pandas as pd

from .config import BASE_MODELAGEM_FILE, FEATURE_BASE, PROCESSED_CATEGORIAS, PROCESSED_CLIENTES, PROCESSED_TRANSACOES, ensure_directories


def execute() -> None:
    ensure_directories()
    clientes = pd.read_csv(PROCESSED_CLIENTES, parse_dates=["data_cadastro"])
    categorias = pd.read_csv(PROCESSED_CATEGORIAS)
    transacoes = pd.read_csv(PROCESSED_TRANSACOES, parse_dates=["data"])

    tx = transacoes.rename(columns={"tipo": "tipo_transacao"}).merge(
        categorias[["categoria_id", "tipo_macro"]],
        on="categoria_id",
        how="left",
    )
    referencia = tx["data"].max() + pd.Timedelta(days=1)

    geral = (
        tx.groupby("cliente_id")
        .agg(
            qtd_transacoes=("transacao_id", "count"),
            valor_total=("valor", "sum"),
            ticket_medio=("valor", "mean"),
            desvio_valor=("valor", "std"),
            maior_transacao=("valor", "max"),
            menor_transacao=("valor", "min"),
            ultimo_movimento=("data", "max"),
            primeira_transacao=("data", "min"),
            qtd_outliers=("flag_outlier", "sum"),
        )
        .reset_index()
    )
    geral["dias_desde_ultima_transacao"] = (referencia - geral["ultimo_movimento"]).dt.days
    geral["meses_atividade"] = ((geral["ultimo_movimento"] - geral["primeira_transacao"]).dt.days / 30).round().clip(lower=1).astype(int)

    tipo_valor = (
        tx.pivot_table(index="cliente_id", columns="tipo_transacao", values="valor", aggfunc="sum", fill_value=0)
        .rename(columns=lambda c: f"valor_{str(c).lower()}")
        .reset_index()
    )
    macro_valor = (
        tx.pivot_table(index="cliente_id", columns="tipo_macro", values="valor", aggfunc="sum", fill_value=0)
        .rename(columns=lambda c: f"valor_macro_{str(c).lower()}")
        .reset_index()
    )
    canal_digital = (
        tx.assign(canal_digital=tx["canal"].fillna("").str.contains("App|Internet|PIX", regex=True).astype(int))
        .groupby("cliente_id", as_index=False)
        .agg(pct_canal_digital=("canal_digital", "mean"))
    )
    mensal = (
        tx.groupby(["cliente_id", "ano_mes"], as_index=False)["valor"]
        .sum()
        .groupby("cliente_id", as_index=False)
        .agg(media_mensal=("valor", "mean"), desvio_mensal=("valor", "std"), pico_mensal=("valor", "max"))
    )

    base = clientes.merge(geral, on="cliente_id", how="left")
    for frame in [tipo_valor, macro_valor, canal_digital, mensal]:
        base = base.merge(frame, on="cliente_id", how="left")

    base["meses_relacionamento"] = ((referencia - base["data_cadastro"]).dt.days / 30).round().clip(lower=1).astype(int)

    fill_numeric = [
        column
        for column in base.columns
        if column.startswith("valor_")
        or column in {
            "ticket_medio",
            "desvio_valor",
            "maior_transacao",
            "menor_transacao",
            "media_mensal",
            "desvio_mensal",
            "pico_mensal",
            "pct_canal_digital",
            "qtd_transacoes",
            "qtd_outliers",
            "dias_desde_ultima_transacao",
            "meses_atividade",
            "meses_relacionamento",
        }
    ]
    for col in fill_numeric:
        base[col] = pd.to_numeric(base[col], errors="coerce").fillna(0)

    base["razao_saldo_renda"] = base["saldo_atual"] / base["renda_mensal"].replace(0, np.nan)
    base["gasto_total_saida"] = base.get("valor_debito", 0) + base.get("valor_transferencia", 0) + base.get("valor_pix", 0)
    base["pressao_financeira"] = base["gasto_total_saida"] / base["renda_mensal"].replace(0, np.nan)
    base["intensidade_credito"] = base.get("valor_credito", 0) / base["valor_total"].replace(0, np.nan)
    base["razao_gasto_renda"] = base["valor_total"] / base["renda_mensal"].replace(0, np.nan)

    macro_columns = [column for column in base.columns if column.startswith("valor_macro_")]
    for col in macro_columns:
        suffix = col.replace("valor_macro_", "")
        base[f"pct_{suffix}"] = base[col] / base["valor_total"].replace(0, np.nan)

    base = base.fillna(0)
    base.to_csv(FEATURE_BASE, index=False)
    base.to_csv(BASE_MODELAGEM_FILE, index=False)
    print(f"Base analitica criada com {len(base)} clientes.")


if __name__ == "__main__":
    execute()
