from __future__ import annotations

from .clean_data import execute as execute_clean
from .create_features import execute as execute_features
from .exploratory_analysis import execute as execute_eda
from .export_frontend_data import execute as execute_export
from .predict_churn import execute as execute_predict
from .simulate_data import execute as execute_simulation
from .train_model import execute as execute_train


def execute() -> None:
    steps = [
        ("simulação de dados", execute_simulation),
        ("limpeza dos dados", execute_clean),
        ("criação da base analítica", execute_features),
        ("estatística exploratória", execute_eda),
        ("treinamento do modelo", execute_train),
        ("predições de churn", execute_predict),
        ("exportação para frontend", execute_export),
    ]
    for name, func in steps:
        print(f"Iniciando etapa: {name}")
        func()
    print("Pipeline completo executado com sucesso.")


if __name__ == "__main__":
    execute()
