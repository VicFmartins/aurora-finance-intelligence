from __future__ import annotations

import json

import joblib
import pandas as pd

from .config import FEATURE_BASE, MODEL_FILE, MODEL_METRICS_FILE, PREDICTIONS_FILE, RISK_THRESHOLD, ensure_directories

CATEGORICAL_COLUMNS = ["genero", "estado", "perfil_risco", "origem_dado"]
EXCLUDED_COLUMNS = {
    "cliente_id",
    "customer_id_original",
    "nome",
    "cidade",
    "data_cadastro",
    "primeira_transacao",
    "ultimo_movimento",
    "churn_flag",
}


def build_feature_frame(base: pd.DataFrame) -> pd.DataFrame:
    numeric_columns = [column for column in base.columns if column not in EXCLUDED_COLUMNS.union(CATEGORICAL_COLUMNS)]
    return base[CATEGORICAL_COLUMNS + numeric_columns].copy()


def load_prediction_threshold() -> float:
    if MODEL_METRICS_FILE.exists():
        metrics = json.loads(MODEL_METRICS_FILE.read_text(encoding="utf-8"))
        return float(metrics.get("threshold_used", RISK_THRESHOLD))
    return float(RISK_THRESHOLD)


def classify_risk(probabilidade: float, threshold: float) -> str:
    if probabilidade >= 0.70:
        return "Alto"
    if probabilidade >= threshold:
        return "Medio"
    return "Baixo"


def recommend_action(probabilidade: float, perfil_risco: str, pressao_financeira: float, threshold: float) -> str:
    if probabilidade >= 0.70:
        if pressao_financeira > 1.05:
            return "Oferecer plano de retencao com renegociacao e acompanhamento proximo."
        return "Ativar contato consultivo com proposta personalizada de retencao."
    if probabilidade >= threshold:
        if perfil_risco == "Conservador":
            return "Enviar jornada educativa com foco em previsibilidade e reserva."
        return "Disparar campanha de engajamento com beneficios de relacionamento."
    return "Manter relacionamento com comunicacao de valor e monitoramento leve."


def execute() -> None:
    ensure_directories()
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Modelo nao encontrado em '{MODEL_FILE}'. Execute 'python -m src.train_model' primeiro.")

    threshold = load_prediction_threshold()
    base = pd.read_csv(FEATURE_BASE)
    model = joblib.load(MODEL_FILE)
    X = build_feature_frame(base)
    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    saida = pd.DataFrame(
        {
            "cliente_id": base["cliente_id"],
            "customer_id_original": base.get("customer_id_original", ""),
            "nome": base["nome"],
            "estado": base["estado"],
            "perfil_risco": base["perfil_risco"],
            "origem_dado": base["origem_dado"],
            "renda_mensal": base["renda_mensal"].round(2),
            "saldo_atual": base["saldo_atual"].round(2),
            "churn_real": base["churn_flag"],
            "prob_churn": probabilities.round(4),
            "predicao_churn": predictions,
            "risco": [classify_risk(value, threshold) for value in probabilities],
            "recomendacao": [
                recommend_action(value, perfil, pressao, threshold)
                for value, perfil, pressao in zip(
                    probabilities,
                    base["perfil_risco"],
                    base["pressao_financeira"],
                    strict=True,
                )
            ],
        }
    ).sort_values("prob_churn", ascending=False)
    saida.to_csv(PREDICTIONS_FILE, index=False)
    print(f"Predicoes exportadas para {PREDICTIONS_FILE.name}.")


if __name__ == "__main__":
    execute()
