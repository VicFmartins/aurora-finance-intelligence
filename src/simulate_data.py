from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .config import N_CLIENTES, RAW_CATEGORIAS, RAW_CLIENTES, RAW_TRANSACOES, SEED, ensure_directories
from .load_public_dataset import load_public_churn_modelling
from .simulate_transactions import assign_synthetic_churn, build_categories, classify_risk_profile, generate_transactions
from .standardize_customers import CUSTOMER_SCHEMA, standardize_public_customers

ESTADOS_CIDADES = {
    "SP": ["Sao Paulo", "Campinas", "Santos", "Sao Jose dos Campos"],
    "RJ": ["Rio de Janeiro", "Niteroi", "Petropolis", "Nova Iguacu"],
    "MG": ["Belo Horizonte", "Uberlandia", "Juiz de Fora", "Contagem"],
    "BA": ["Salvador", "Feira de Santana", "Camacari", "Vitoria da Conquista"],
    "PE": ["Recife", "Olinda", "Caruaru", "Petrolina"],
    "PR": ["Curitiba", "Londrina", "Maringa", "Ponta Grossa"],
    "CE": ["Fortaleza", "Sobral", "Juazeiro do Norte", "Caucaia"],
    "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Santa Maria"],
}

FIRST_NAMES = [
    "Ana",
    "Beatriz",
    "Camila",
    "Daniela",
    "Elisa",
    "Fernanda",
    "Giovana",
    "Helena",
    "Isabela",
    "Juliana",
    "Larissa",
    "Marina",
    "Natalia",
    "Olivia",
    "Priscila",
    "Renata",
    "Sabrina",
    "Tatiane",
]

LAST_NAMES = [
    "Almeida",
    "Barbosa",
    "Cardoso",
    "Costa",
    "Dias",
    "Ferreira",
    "Freitas",
    "Gomes",
    "Lima",
    "Martins",
    "Melo",
    "Oliveira",
    "Pereira",
    "Rocha",
    "Santos",
    "Souza",
    "Teixeira",
    "Vieira",
]

GENDERS = ["Feminino", "Masculino", "Nao informado"]


def build_name(rng: random.Random) -> str:
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def generate_synthetic_clients(np_rng: np.random.Generator, py_rng: random.Random) -> pd.DataFrame:
    reference_date = datetime(2025, 4, 30)
    estados = list(ESTADOS_CIDADES)
    pesos_estados = np.array([0.30, 0.14, 0.16, 0.10, 0.08, 0.09, 0.06, 0.07], dtype=float)
    pesos_estados = pesos_estados / pesos_estados.sum()
    rows: list[dict[str, object]] = []

    for index in range(1, N_CLIENTES + 1):
        renda = float(np_rng.lognormal(mean=8.45, sigma=0.47))
        saldo = float(np_rng.normal(loc=renda * 2.0, scale=renda * 0.95))
        saldo = max(300.0, saldo)
        idade = int(np_rng.integers(21, 70))
        estado = str(np_rng.choice(estados, p=pesos_estados))
        cidade = py_rng.choice(ESTADOS_CIDADES[estado])
        score_credito = int(np.clip(np_rng.normal(loc=655, scale=88), 380, 860))
        tempo_relacionamento = int(np_rng.integers(1, 11))
        produtos_ativos = int(np_rng.integers(1, 5))
        tem_cartao_credito = int(np_rng.binomial(1, 0.76))
        membro_ativo = int(np_rng.binomial(1, 0.72 if produtos_ativos >= 2 else 0.58))
        genero = str(np_rng.choice(GENDERS, p=[0.48, 0.44, 0.08]))
        data_cadastro = (reference_date - timedelta(days=tempo_relacionamento * 365 + int(index % 180))).date().isoformat()

        rows.append(
            {
                "cliente_id": f"C{index:06d}",
                "customer_id_original": "",
                "nome": build_name(py_rng),
                "idade": idade,
                "genero": genero,
                "cidade": cidade,
                "estado": estado,
                "renda_mensal": round(renda, 2),
                "saldo_atual": round(saldo, 2),
                "score_credito": score_credito,
                "tempo_relacionamento": tempo_relacionamento,
                "produtos_ativos": produtos_ativos,
                "tem_cartao_credito": tem_cartao_credito,
                "membro_ativo": membro_ativo,
                "perfil_risco": classify_risk_profile(score_credito, saldo, renda, 0, membro_ativo),
                "data_cadastro": data_cadastro,
                "churn_flag": 0,
                "origem_dado": "synthetic_fallback",
            }
        )

    clientes = pd.DataFrame(rows)
    if not clientes.empty:
        clientes.loc[np_rng.choice(clientes.index, size=max(10, N_CLIENTES // 75), replace=False), "genero"] = np.nan
        clientes.loc[np_rng.choice(clientes.index, size=max(10, N_CLIENTES // 100), replace=False), "perfil_risco"] = np.nan
    return clientes[CUSTOMER_SCHEMA]


def load_or_generate_clients(np_rng: np.random.Generator, py_rng: random.Random) -> tuple[pd.DataFrame, str]:
    public_dataset = load_public_churn_modelling()
    if public_dataset is not None:
        clientes = standardize_public_customers(public_dataset)
        return clientes, "public_kaggle_churn_modelling"

    clientes = generate_synthetic_clients(np_rng, py_rng)
    return clientes, "synthetic_fallback"


def execute() -> None:
    ensure_directories()
    np_rng = np.random.default_rng(SEED)
    py_rng = random.Random(SEED)

    categorias = build_categories()
    clientes, source_type = load_or_generate_clients(np_rng, py_rng)
    transacoes = generate_transactions(clientes, categorias, np_rng, use_churn_signal=(source_type == "synthetic_fallback"))

    if source_type == "synthetic_fallback":
        clientes = assign_synthetic_churn(clientes, transacoes, categorias)

    categorias.to_csv(RAW_CATEGORIAS, index=False)
    clientes.to_csv(RAW_CLIENTES, index=False)
    transacoes.to_csv(RAW_TRANSACOES, index=False)

    print(
        "Simulacao concluida | "
        f"clientes={len(clientes)} | "
        f"transacoes={len(transacoes)} | "
        f"categorias={len(categorias)} | "
        f"churn_rate={clientes['churn_flag'].mean():.2%} | "
        f"origem={source_type}"
    )


if __name__ == "__main__":
    execute()
