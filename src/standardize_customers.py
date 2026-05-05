from __future__ import annotations

import re
import unicodedata

import numpy as np
import pandas as pd

from .config import SEED

CUSTOMER_SCHEMA = [
    "cliente_id",
    "customer_id_original",
    "nome",
    "idade",
    "genero",
    "cidade",
    "estado",
    "renda_mensal",
    "saldo_atual",
    "score_credito",
    "tempo_relacionamento",
    "produtos_ativos",
    "tem_cartao_credito",
    "membro_ativo",
    "perfil_risco",
    "data_cadastro",
    "churn_flag",
    "origem_dado",
]

GEOGRAPHY_MAP = {
    "france": ("Paris", "Franca"),
    "germany": ("Berlim", "Alemanha"),
    "spain": ("Madrid", "Espanha"),
}

GENDER_MAP = {
    "female": "Feminino",
    "f": "Feminino",
    "feminino": "Feminino",
    "male": "Masculino",
    "m": "Masculino",
    "masculino": "Masculino",
}


def normalize_column_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", normalized).strip("_").lower()
    return normalized


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.rename(columns={column: normalize_column_name(column) for column in frame.columns})


def get_first_available(frame: pd.DataFrame, candidates: list[str]) -> pd.Series | None:
    for candidate in candidates:
        if candidate in frame.columns:
            return frame[candidate]
    return None


def coerce_numeric(series: pd.Series | None, fallback: pd.Series) -> pd.Series:
    if series is None:
        return fallback
    converted = pd.to_numeric(series, errors="coerce")
    return converted.fillna(fallback)


def normalize_gender(series: pd.Series | None, size: int, index: pd.Index) -> pd.Series:
    if series is None:
        return pd.Series(["Nao informado"] * size, index=index)
    return (
        series.fillna("Nao informado")
        .astype(str)
        .str.strip()
        .str.lower()
        .map(GENDER_MAP)
        .fillna("Nao informado")
    )


def normalize_binary(series: pd.Series | None, default: int, size: int, index: pd.Index) -> pd.Series:
    if series is None:
        return pd.Series([default] * size, index=index, dtype="int64")

    if pd.api.types.is_numeric_dtype(series):
        return pd.to_numeric(series, errors="coerce").fillna(default).round().clip(0, 1).astype(int)

    normalized = series.fillna(default).astype(str).str.strip().str.lower()
    truthy = {"1", "true", "yes", "sim", "active", "ativo", "existing customer", "existing"}
    falsy = {"0", "false", "no", "nao", "inactive", "inativo"}
    converted = normalized.map(lambda value: 1 if value in truthy else 0 if value in falsy else default)
    return converted.astype(int)


def build_customer_ids(size: int, index: pd.Index) -> pd.Series:
    return pd.Series([f"C{position:06d}" for position in range(1, size + 1)], index=index)


def derive_geo_fields(geography: pd.Series, size: int, index: pd.Index) -> tuple[pd.Series, pd.Series]:
    cleaned = geography.fillna("Nao informado").astype(str).str.strip()
    normalized = cleaned.map(normalize_column_name)

    estado = cleaned.copy()
    cidade = cleaned.copy()

    for key, (capital, estado_pt) in GEOGRAPHY_MAP.items():
        mask = normalized.eq(key)
        estado.loc[mask] = estado_pt
        cidade.loc[mask] = capital

    missing_mask = estado.eq("") | estado.isna()
    estado.loc[missing_mask] = "Nao informado"
    cidade.loc[missing_mask] = "Nao informado"
    return cidade.reindex(index).fillna("Nao informado"), estado.reindex(index).fillna("Nao informado")


def derive_registration_dates(tempo_relacionamento: pd.Series) -> pd.Series:
    reference_date = pd.Timestamp("2025-04-30")
    offsets = pd.to_timedelta((tempo_relacionamento.index.to_series() % 365), unit="D")
    registration = reference_date - pd.to_timedelta((tempo_relacionamento * 365).round().astype(int), unit="D") - offsets
    return registration.dt.date.astype(str)


def derive_risk_profile(
    score_credito: pd.Series,
    saldo_atual: pd.Series,
    renda_mensal: pd.Series,
    membro_ativo: pd.Series,
    churn_flag: pd.Series,
) -> pd.Series:
    razao_saldo_renda = saldo_atual / renda_mensal.replace(0, np.nan)
    points = pd.Series(0, index=score_credito.index, dtype="int64")
    points = points + np.where(score_credito >= 740, 2, np.where(score_credito >= 640, 1, -1))
    points = points + np.where(razao_saldo_renda >= 2.4, 1, np.where(razao_saldo_renda <= 0.5, -1, 0))
    points = points + np.where(membro_ativo.eq(1), 1, -1)
    points = points + np.where(churn_flag.eq(1), -1, 0)

    perfil = pd.Series("Moderado", index=score_credito.index)
    perfil.loc[points <= 0] = "Conservador"
    perfil.loc[points >= 3] = "Arrojado"
    return perfil


def standardize_public_customers(raw_customers: pd.DataFrame) -> pd.DataFrame:
    frame = normalize_columns(raw_customers.copy())
    rng = np.random.default_rng(SEED)
    size = len(frame)
    index = frame.index

    customer_id_source = get_first_available(frame, ["customerid", "customer_id", "rownumber", "id"])
    if customer_id_source is None:
        customer_id_original = pd.Series([""] * size, index=index)
    else:
        customer_id_original = customer_id_source.fillna("").astype(str).str.strip()

    nome_source = get_first_available(frame, ["surname", "nome", "sobrenome"])
    if nome_source is None:
        nome = pd.Series([f"Cliente {position:04d}" for position in range(1, size + 1)], index=index)
    else:
        nome = (
            nome_source.fillna("")
            .astype(str)
            .str.strip()
            .replace("", np.nan)
            .fillna(pd.Series([f"Cliente {position:04d}" for position in range(1, size + 1)], index=index))
        )

    idade = coerce_numeric(
        get_first_available(frame, ["age", "idade"]),
        pd.Series(rng.integers(22, 71, size=size), index=index),
    ).round().clip(lower=18, upper=90)
    score_credito = coerce_numeric(
        get_first_available(frame, ["creditscore", "credit_score", "score_credito"]),
        pd.Series(rng.integers(450, 851, size=size), index=index),
    ).round().clip(lower=300, upper=900)
    tempo_relacionamento = coerce_numeric(
        get_first_available(frame, ["tenure", "tempo_relacionamento"]),
        pd.Series(rng.integers(1, 11, size=size), index=index),
    ).round().clip(lower=0, upper=15)

    geography = get_first_available(frame, ["geography", "country", "pais", "estado"])
    if geography is None:
        geography = pd.Series(["Nao informado"] * size, index=index)
    cidade, estado = derive_geo_fields(geography, size, index)

    genero = normalize_gender(get_first_available(frame, ["gender", "genero", "sexo"]), size, index)

    renda_anual = coerce_numeric(
        get_first_available(frame, ["estimatedsalary", "estimated_salary", "salario_estimado"]),
        pd.Series(52000 + rng.normal(0, 18000, size=size), index=index),
    ).clip(lower=12000)
    renda_mensal = (renda_anual / 12).clip(lower=1000)

    saldo_atual = coerce_numeric(
        get_first_available(frame, ["balance", "saldo", "saldo_atual"]),
        pd.Series(renda_mensal * rng.uniform(0.6, 2.8, size=size), index=index),
    ).clip(lower=0)

    produtos_ativos = coerce_numeric(
        get_first_available(frame, ["numofproducts", "num_of_products", "produtos_ativos"]),
        pd.Series(rng.integers(1, 5, size=size), index=index),
    ).round().clip(lower=1, upper=6)
    tem_cartao_credito = normalize_binary(get_first_available(frame, ["hascrcard", "tem_cartao_credito"]), default=1, size=size, index=index)
    membro_ativo = normalize_binary(get_first_available(frame, ["isactivemember", "membro_ativo"]), default=0, size=size, index=index)
    churn_flag = normalize_binary(get_first_available(frame, ["exited", "churn", "churn_flag"]), default=0, size=size, index=index)

    data_cadastro = derive_registration_dates(tempo_relacionamento)
    perfil_risco = derive_risk_profile(score_credito, saldo_atual, renda_mensal, membro_ativo, churn_flag)

    clientes = pd.DataFrame(
        {
            "cliente_id": build_customer_ids(size, index),
            "customer_id_original": customer_id_original,
            "nome": nome,
            "idade": idade.astype(int),
            "genero": genero,
            "cidade": cidade,
            "estado": estado,
            "renda_mensal": renda_mensal.round(2),
            "saldo_atual": saldo_atual.round(2),
            "score_credito": score_credito.astype(int),
            "tempo_relacionamento": tempo_relacionamento.astype(int),
            "produtos_ativos": produtos_ativos.astype(int),
            "tem_cartao_credito": tem_cartao_credito.astype(int),
            "membro_ativo": membro_ativo.astype(int),
            "perfil_risco": perfil_risco,
            "data_cadastro": data_cadastro,
            "churn_flag": churn_flag.astype(int),
            "origem_dado": "public_kaggle_churn_modelling",
        }
    )

    return clientes[CUSTOMER_SCHEMA]
