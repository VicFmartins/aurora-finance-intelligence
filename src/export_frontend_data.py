from __future__ import annotations

import json

import pandas as pd

from .config import (
    FEATURE_BASE,
    FEATURE_IMPORTANCE_FILE,
    FRONTEND_FEATURES_FILE,
    FRONTEND_METRICS_FILE,
    FRONTEND_PREDICTIONS_FILE,
    FRONTEND_SUMMARY_FILE,
    FRONTEND_THRESHOLD_ANALYSIS_FILE,
    MODEL_METRICS_FILE,
    PREDICTIONS_FILE,
    SUMMARY_FILE,
    THRESHOLD_ANALYSIS_FILE,
    ensure_directories,
)


def execute() -> None:
    ensure_directories()
    metrics = json.loads(MODEL_METRICS_FILE.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY_FILE.read_text(encoding="utf-8"))
    predictions = pd.read_csv(PREDICTIONS_FILE)
    importance = pd.read_csv(FEATURE_IMPORTANCE_FILE)
    threshold_analysis = pd.read_csv(THRESHOLD_ANALYSIS_FILE) if THRESHOLD_ANALYSIS_FILE.exists() else pd.DataFrame()
    base = pd.read_csv(FEATURE_BASE)

    risk_distribution = predictions["risco"].value_counts().reindex(["Alto", "Medio", "Baixo"], fill_value=0)
    avg_prob_by_state = predictions.groupby("estado", as_index=False)["prob_churn"].mean().sort_values("prob_churn", ascending=False).head(10)
    impact = {
        "clientes_alto_risco": int(risk_distribution.get("Alto", 0)),
        "clientes_medio_risco": int(risk_distribution.get("Medio", 0)),
        "clientes_baixo_risco": int(risk_distribution.get("Baixo", 0)),
        "ticket_medio_clientes_alto_risco": round(float(predictions.loc[predictions["risco"] == "Alto", "renda_mensal"].mean()), 2),
        "share_clientes_alto_risco": round(float((predictions["risco"] == "Alto").mean()), 4),
    }
    public_dataset_used = bool(summary.get("public_dataset_used", False))
    summary_payload = {
        **summary,
        "risk_distribution": [{"name": index, "value": int(value)} for index, value in risk_distribution.items()],
        "avg_prob_by_state": avg_prob_by_state.round(4).to_dict(orient="records"),
        "impact": impact,
        "frontend_notes": {
            "premium_free": "O app roda de forma estatica com JSON local, sem backend nem banco cloud obrigatorios.",
            "aws_ready": "O mesmo build pode ser publicado em S3 Static Website ou AWS Amplify sem mudar a aplicacao.",
            "data_foundation": (
                "Base publica Kaggle + camada sintetica de transacoes"
                if public_dataset_used
                else "Fallback sintetico + camada sintetica de transacoes"
            ),
        },
        "top_states_by_churn_risk": avg_prob_by_state.to_dict(orient="records"),
        "feature_base_columns": list(base.columns[:16]),
        "threshold_analysis": threshold_analysis.to_dict(orient="records"),
        "model_positioning": {
            "false_negative_importance": "Em churn, falso negativo importa porque um cliente que sairia pode passar despercebido.",
            "precision_meaning": "Precision indica a qualidade dos alertas.",
            "recall_meaning": "Recall indica a capacidade de capturar clientes que poderiam sair.",
            "mvp_scope": "A Aurora usa ranking de risco e priorizacao, nao decisao automatica.",
        },
    }

    FRONTEND_METRICS_FILE.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    FRONTEND_SUMMARY_FILE.write_text(json.dumps(summary_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    FRONTEND_PREDICTIONS_FILE.write_text(
        json.dumps(predictions.head(250).to_dict(orient="records"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    FRONTEND_FEATURES_FILE.write_text(
        json.dumps(importance.round(6).to_dict(orient="records"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    FRONTEND_THRESHOLD_ANALYSIS_FILE.write_text(
        json.dumps(threshold_analysis.to_dict(orient="records"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print("JSONs do frontend exportados com sucesso.")


if __name__ == "__main__":
    execute()
