from __future__ import annotations

import pandas as pd

from .config import PUBLIC_CHURN_MODELLING_FILE


def public_dataset_exists() -> bool:
    return PUBLIC_CHURN_MODELLING_FILE.exists()


def load_public_churn_modelling() -> pd.DataFrame | None:
    if not public_dataset_exists():
        return None

    dataset = pd.read_csv(PUBLIC_CHURN_MODELLING_FILE)
    if dataset.empty:
        raise ValueError(
            "O arquivo 'dados/raw/churn_modelling.csv' foi encontrado, mas esta vazio. "
            "Preencha o CSV ou remova o arquivo para usar o fallback sintetico."
        )
    return dataset
