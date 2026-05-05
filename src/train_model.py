from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .config import (
    CLASSIFICATION_REPORT_FILE,
    FEATURE_BASE,
    FEATURE_IMPORTANCE_FILE,
    MODEL_FILE,
    MODEL_METRICS_FILE,
    SEED,
    THRESHOLD_ANALYSIS_FILE,
    THRESHOLDS_TO_EVALUATE,
    ensure_directories,
)
from .predict_churn import CATEGORICAL_COLUMNS, EXCLUDED_COLUMNS


def build_pipeline(categorical_columns: list[str], numeric_columns: list[str]) -> Pipeline:
    preprocessor = ColumnTransformer(
        transformers=[
            ("categoricas", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
            ("numericas", "passthrough", numeric_columns),
        ]
    )
    classifier = RandomForestClassifier(
        n_estimators=340,
        max_depth=12,
        min_samples_leaf=4,
        class_weight="balanced",
        random_state=SEED,
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", classifier),
        ]
    )


def evaluate_thresholds(y_true: pd.Series, probabilities: np.ndarray) -> pd.DataFrame:
    rows = []
    for threshold in THRESHOLDS_TO_EVALUATE:
        predictions = (probabilities >= threshold).astype(int)
        precision = float(precision_score(y_true, predictions, zero_division=0))
        recall = float(recall_score(y_true, predictions, zero_division=0))
        f1 = float(f1_score(y_true, predictions, zero_division=0))
        alert_rate = float(predictions.mean())
        retention_score = (recall * 0.55) + (precision * 0.30) + (f1 * 0.15)
        rows.append(
            {
                "threshold": round(float(threshold), 2),
                "accuracy": round(float(accuracy_score(y_true, predictions)), 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1, 4),
                "alert_rate": round(alert_rate, 4),
                "retention_score": round(retention_score, 4),
            }
        )
    return pd.DataFrame(rows).sort_values("threshold").reset_index(drop=True)


def choose_recommended_threshold(threshold_analysis: pd.DataFrame) -> float:
    acceptable = threshold_analysis.loc[threshold_analysis["precision"] >= 0.35].copy()
    if acceptable.empty:
        acceptable = threshold_analysis.copy()
    ordered = acceptable.sort_values(
        by=["retention_score", "f1_score", "precision"],
        ascending=False,
    ).reset_index(drop=True)
    return float(ordered.loc[0, "threshold"])


def execute() -> None:
    ensure_directories()
    base = pd.read_csv(FEATURE_BASE)

    categorical_columns = CATEGORICAL_COLUMNS
    numeric_columns = [column for column in base.columns if column not in EXCLUDED_COLUMNS.union(categorical_columns)]
    X = base[categorical_columns + numeric_columns].copy()
    y = base["churn_flag"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=SEED,
    )

    evaluation_pipeline = build_pipeline(categorical_columns, numeric_columns)
    evaluation_pipeline.fit(X_train, y_train)

    probabilities = evaluation_pipeline.predict_proba(X_test)[:, 1]
    threshold_analysis = evaluate_thresholds(y_test, probabilities)
    recommended_threshold = choose_recommended_threshold(threshold_analysis)
    predictions = (probabilities >= recommended_threshold).astype(int)

    metrics = {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "baseline_churn_rate": round(float(y.mean()), 4),
        "threshold_used": round(float(recommended_threshold), 2),
        "threshold_candidates": list(THRESHOLDS_TO_EVALUATE),
        "threshold_analysis_file": THRESHOLD_ANALYSIS_FILE.name,
        "tradeoff_summary": (
            "Churn é um problema de retenção em que falso negativo importa. "
            "Por isso, a Aurora compara múltiplos thresholds e recomenda um ponto de corte que preserva recall "
            "sem abrir mão demais da precision. Neste MVP, o foco principal é ranking de risco e priorização humana, "
            "não decisão automática."
        ),
        "recommended_threshold_reason": (
            f"O threshold {recommended_threshold:.2f} foi recomendado por apresentar o melhor equilíbrio prático "
            "entre recall e precision para retenção, usando uma pontuação que dá mais peso à captura de clientes em risco "
            "e um piso mínimo de precisão para evitar alertas excessivamente frágeis."
        ),
        "metric_notes": {
            "precision": "Mostra a qualidade dos alertas gerados pelo modelo.",
            "recall": "Mostra a capacidade de capturar clientes que poderiam sair.",
            "false_negative_risk": "Em churn, deixar passar um cliente que sairia pode ser mais custoso do que investigar um alerta extra.",
            "mvp_positioning": "O modelo apoia priorização e ranking de risco, não decisão automática.",
        },
    }

    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)

    production_pipeline = build_pipeline(categorical_columns, numeric_columns)
    production_pipeline.fit(X, y)
    joblib.dump(production_pipeline, MODEL_FILE)

    preprocessor = production_pipeline.named_steps["preprocessor"]
    model = production_pipeline.named_steps["model"]
    features = preprocessor.get_feature_names_out()
    importance = (
        pd.DataFrame({"feature": features, "importance": model.feature_importances_})
        .sort_values("importance", ascending=False)
        .head(20)
    )
    importance.to_csv(FEATURE_IMPORTANCE_FILE, index=False)
    threshold_analysis.to_csv(THRESHOLD_ANALYSIS_FILE, index=False)
    MODEL_METRICS_FILE.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    CLASSIFICATION_REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        "Treinamento concluído | "
        f"roc_auc={metrics['roc_auc']:.4f} | "
        f"precision={metrics['precision']:.4f} | "
        f"recall={metrics['recall']:.4f} | "
        f"threshold={metrics['threshold_used']:.2f}"
    )


if __name__ == "__main__":
    execute()
