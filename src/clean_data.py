from __future__ import annotations

import pandas as pd

from .config import (
    PROCESSED_CATEGORIAS,
    PROCESSED_CATEGORIAS_LIMPO,
    PROCESSED_CLIENTES,
    PROCESSED_CLIENTES_LIMPO,
    PROCESSED_TRANSACOES,
    PROCESSED_TRANSACOES_LIMPO,
    RAW_CATEGORIAS,
    RAW_CLIENTES,
    RAW_TRANSACOES,
    VALIDATION_REPORT_FILE,
    ensure_directories,
)


def flag_outliers_iqr(series: pd.Series) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return ((series < lower) | (series > upper)).astype(int)


def execute() -> None:
    ensure_directories()
    clientes = pd.read_csv(RAW_CLIENTES)
    categorias = pd.read_csv(RAW_CATEGORIAS)
    transacoes = pd.read_csv(RAW_TRANSACOES)

    validation = [
        {"etapa": "clientes_raw", "linhas_antes": len(clientes), "duplicadas_removidas": int(clientes.duplicated(subset=["cliente_id"]).sum())},
        {"etapa": "categorias_raw", "linhas_antes": len(categorias), "duplicadas_removidas": int(categorias.duplicated(subset=["categoria_id"]).sum())},
        {"etapa": "transacoes_raw", "linhas_antes": len(transacoes), "duplicadas_removidas": int(transacoes.duplicated(subset=["transacao_id"]).sum())},
    ]

    clientes = clientes.drop_duplicates(subset=["cliente_id"]).copy()
    categorias = categorias.drop_duplicates(subset=["categoria_id"]).copy()
    transacoes = transacoes.drop_duplicates(subset=["transacao_id"]).copy()

    clientes["data_cadastro"] = pd.to_datetime(clientes["data_cadastro"], errors="coerce")
    transacoes["data"] = pd.to_datetime(transacoes["data"], errors="coerce")

    clientes["genero"] = (
        clientes["genero"]
        .replace({"Nao Informado": "Nao informado", "Não Informado": "Nao informado"})
        .fillna("Nao informado")
        .astype(str)
        .str.strip()
    )
    clientes["perfil_risco"] = clientes["perfil_risco"].fillna("Moderado").astype(str).str.strip()
    clientes["cidade"] = clientes["cidade"].fillna("Desconhecida").astype(str).str.strip()
    clientes["estado"] = clientes["estado"].fillna("Nao informado").astype(str).str.strip()
    clientes["nome"] = clientes["nome"].fillna("Cliente sem nome").astype(str).str.strip()
    clientes["customer_id_original"] = clientes.get("customer_id_original", "")
    clientes["customer_id_original"] = clientes["customer_id_original"].fillna("").astype(str).str.strip()
    clientes["origem_dado"] = clientes.get("origem_dado", "synthetic_fallback")
    clientes["origem_dado"] = clientes["origem_dado"].fillna("synthetic_fallback").astype(str).str.strip()

    numeric_columns = [
        "idade",
        "renda_mensal",
        "saldo_atual",
        "score_credito",
        "tempo_relacionamento",
        "produtos_ativos",
        "tem_cartao_credito",
        "membro_ativo",
        "churn_flag",
    ]
    for col in numeric_columns:
        clientes[col] = pd.to_numeric(clientes[col], errors="coerce")
        clientes[col] = clientes[col].fillna(clientes[col].median())

    clientes["idade"] = clientes["idade"].round().clip(lower=18, upper=90).astype(int)
    clientes["renda_mensal"] = clientes["renda_mensal"].clip(lower=0).round(2)
    clientes["saldo_atual"] = clientes["saldo_atual"].clip(lower=0).round(2)
    clientes["score_credito"] = clientes["score_credito"].round().clip(lower=300, upper=900).astype(int)
    clientes["tempo_relacionamento"] = clientes["tempo_relacionamento"].round().clip(lower=0, upper=20).astype(int)
    clientes["produtos_ativos"] = clientes["produtos_ativos"].round().clip(lower=1, upper=10).astype(int)
    clientes["tem_cartao_credito"] = clientes["tem_cartao_credito"].round().clip(lower=0, upper=1).astype(int)
    clientes["membro_ativo"] = clientes["membro_ativo"].round().clip(lower=0, upper=1).astype(int)
    clientes["churn_flag"] = clientes["churn_flag"].round().clip(lower=0, upper=1).astype(int)
    clientes = clientes.dropna(subset=["data_cadastro"])

    categorias["nome_categoria"] = categorias["nome_categoria"].astype(str).str.strip()
    categorias["tipo_macro"] = categorias["tipo_macro"].fillna("Outros").astype(str).str.strip()
    categorias["descricao"] = categorias["descricao"].fillna("Descricao nao informada").astype(str).str.strip()

    transacoes["tipo"] = transacoes["tipo"].fillna("Debito").astype(str).str.strip()
    transacoes["descricao"] = transacoes["descricao"].fillna("Descricao nao informada").astype(str).str.strip()
    transacoes["canal"] = transacoes["canal"].fillna("Canal nao informado").astype(str).str.strip()
    transacoes["valor"] = pd.to_numeric(transacoes["valor"], errors="coerce")
    transacoes["categoria_id"] = pd.to_numeric(transacoes["categoria_id"], errors="coerce")

    transacoes["valor"] = transacoes["valor"].fillna(transacoes["valor"].median()).clip(lower=0.01).round(2)
    transacoes["categoria_id"] = transacoes["categoria_id"].fillna(transacoes["categoria_id"].mode().iat[0]).astype(int)
    transacoes = transacoes.dropna(subset=["data", "cliente_id"])
    transacoes["ano_mes"] = transacoes["data"].dt.to_period("M").astype(str)
    transacoes["flag_outlier"] = flag_outliers_iqr(transacoes["valor"])

    clientes.to_csv(PROCESSED_CLIENTES, index=False)
    clientes.to_csv(PROCESSED_CLIENTES_LIMPO, index=False)
    categorias.to_csv(PROCESSED_CATEGORIAS, index=False)
    categorias.to_csv(PROCESSED_CATEGORIAS_LIMPO, index=False)
    transacoes.to_csv(PROCESSED_TRANSACOES, index=False)
    transacoes.to_csv(PROCESSED_TRANSACOES_LIMPO, index=False)
    pd.DataFrame(validation).to_csv(VALIDATION_REPORT_FILE, index=False)

    print(
        "Limpeza concluida | "
        f"clientes={len(clientes)} | categorias={len(categorias)} | transacoes={len(transacoes)}"
    )


if __name__ == "__main__":
    execute()
