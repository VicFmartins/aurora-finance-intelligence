from __future__ import annotations

import json

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from .config import (
    CLIENT_STATS_FILE,
    FEATURE_BASE,
    FIGURAS_DIR,
    PROCESSED_CATEGORIAS,
    PROCESSED_CLIENTES,
    PROCESSED_TRANSACOES,
    SUMMARY_FILE,
    TRANSACTION_STATS_FILE,
    ensure_directories,
)

matplotlib.use("Agg")


def summarize_numeric(series: pd.Series) -> dict[str, float]:
    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    mean = float(series.mean())
    std = float(series.std())
    mode = series.mode()
    return {
        "count": float(series.count()),
        "mean": mean,
        "median": float(series.median()),
        "mode": float(mode.iat[0]) if not mode.empty else 0.0,
        "std": std,
        "var": float(series.var()),
        "min": float(series.min()),
        "p10": float(series.quantile(0.10)),
        "p25": q1,
        "p50": float(series.quantile(0.50)),
        "p75": q3,
        "p90": float(series.quantile(0.90)),
        "max": float(series.max()),
        "skew": float(series.skew()),
        "kurtosis": float(series.kurtosis()),
        "cv_pct": float((std / mean) * 100) if mean else 0.0,
        "iqr": q3 - q1,
    }


def plot_histograma_renda(clientes: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5))
    plt.hist(clientes["renda_mensal"], bins=30, color="#22d3ee", edgecolor="#0f172a")
    plt.title("Distribuicao de renda mensal")
    plt.xlabel("Renda mensal (R$)")
    plt.ylabel("Quantidade de clientes")
    plt.tight_layout()
    plt.savefig(FIGURAS_DIR / "histograma_renda.png", dpi=150)
    plt.close()


def plot_top_categorias(transacoes: pd.DataFrame, categorias: pd.DataFrame) -> pd.DataFrame:
    base = transacoes.merge(categorias[["categoria_id", "nome_categoria"]], on="categoria_id", how="left")
    ranking = base.groupby("nome_categoria", as_index=False)["valor"].sum().sort_values("valor", ascending=False).head(8)
    plt.figure(figsize=(10, 5))
    plt.bar(ranking["nome_categoria"], ranking["valor"], color="#8b5cf6")
    plt.title("Top categorias por volume transacionado")
    plt.xlabel("Categoria")
    plt.ylabel("Valor total (R$)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURAS_DIR / "top_categorias.png", dpi=150)
    plt.close()
    return ranking


def plot_evolucao_mensal(transacoes: pd.DataFrame) -> pd.DataFrame:
    mensal = transacoes.groupby("ano_mes", as_index=False)["valor"].sum().sort_values("ano_mes")
    plt.figure(figsize=(10, 5))
    plt.plot(mensal["ano_mes"], mensal["valor"], marker="o", color="#38bdf8")
    plt.title("Evolucao mensal do volume financeiro")
    plt.xlabel("Ano-mes")
    plt.ylabel("Volume (R$)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURAS_DIR / "evolucao_mensal.png", dpi=150)
    plt.close()
    return mensal


def plot_ticket_por_churn(base: pd.DataFrame) -> None:
    groups = [base.loc[base["churn_flag"] == 0, "ticket_medio"], base.loc[base["churn_flag"] == 1, "ticket_medio"]]
    plt.figure(figsize=(8, 5))
    bp = plt.boxplot(groups, labels=["Ativo", "Churn"], patch_artist=True)
    for patch, color in zip(bp["boxes"], ["#1d4ed8", "#ef4444"], strict=True):
        patch.set_facecolor(color)
    plt.title("Ticket medio por status de churn")
    plt.ylabel("Ticket medio (R$)")
    plt.tight_layout()
    plt.savefig(FIGURAS_DIR / "ticket_por_churn.png", dpi=150)
    plt.close()


def execute() -> None:
    ensure_directories()
    clientes = pd.read_csv(PROCESSED_CLIENTES)
    categorias = pd.read_csv(PROCESSED_CATEGORIAS)
    transacoes = pd.read_csv(PROCESSED_TRANSACOES)
    base = pd.read_csv(FEATURE_BASE)

    client_stats = pd.DataFrame(
        {
            column: summarize_numeric(clientes[column])
            for column in ["idade", "renda_mensal", "saldo_atual", "score_credito", "tempo_relacionamento"]
        }
    ).T
    client_stats.index.name = "variavel"

    transaction_stats = pd.DataFrame({column: summarize_numeric(transacoes[column]) for column in ["valor", "flag_outlier"]}).T
    transaction_stats.index.name = "variavel"

    top_categorias = plot_top_categorias(transacoes, categorias)
    evolucao = plot_evolucao_mensal(transacoes)
    plot_histograma_renda(clientes)
    plot_ticket_por_churn(base)

    origem_series = clientes["origem_dado"].fillna("synthetic_fallback").astype(str)
    public_dataset_used = bool(origem_series.eq("public_kaggle_churn_modelling").any())

    summary = {
        "total_clientes": int(len(clientes)),
        "total_transacoes": int(len(transacoes)),
        "churn_rate_real": round(float(clientes["churn_flag"].mean()), 4),
        "ticket_medio": round(float(transacoes["valor"].mean()), 2),
        "volume_total": round(float(transacoes["valor"].sum()), 2),
        "top_categorias_consumo": top_categorias.to_dict(orient="records"),
        "evolucao_mensal": evolucao.tail(12).to_dict(orient="records"),
        "distribuicao_estados": clientes["estado"].value_counts().to_dict(),
        "data_source_type": "public_kaggle_churn_modelling_plus_synthetic_transactions" if public_dataset_used else "synthetic_fallback",
        "data_source_name": "Churn Modelling",
        "data_source_platform": "Kaggle",
        "data_source_file": "dados/raw/churn_modelling.csv",
        "public_dataset_used": public_dataset_used,
        "synthetic_transactions_used": True,
        "data_source_note": "Base publica de churn bancario enriquecida com camada sintetica de transacoes financeiras.",
        "origem_dado_counts": origem_series.value_counts().to_dict(),
        "impacto_negocio": {
            "headline": "A Aurora transforma sinais financeiros em priorizacao de retencao.",
            "pontos": [
                "antecipar clientes com maior risco de churn",
                "usar Exited como target de churn do Kaggle",
                "enriquecer a base publica com transacoes sinteticas reprodutiveis",
            ],
        },
    }

    client_stats.to_csv(CLIENT_STATS_FILE)
    transaction_stats.to_csv(TRANSACTION_STATS_FILE)
    SUMMARY_FILE.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("EDA concluida com estatisticas, resumo e figuras.")


if __name__ == "__main__":
    execute()
