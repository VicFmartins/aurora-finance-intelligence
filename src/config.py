from __future__ import annotations

from pathlib import Path

SEED = 42
N_CLIENTES = 2800
MIN_TRANSACOES_POR_CLIENTE = 18
MAX_TRANSACOES_POR_CLIENTE = 34
THRESHOLDS_TO_EVALUATE = (0.30, 0.40, 0.50)
RISK_THRESHOLD = 0.40

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
DADOS_DIR = BASE_DIR / "dados"
RAW_DIR = DADOS_DIR / "raw"
PROCESSED_DIR = DADOS_DIR / "processed"
OUTPUTS_DIR = DADOS_DIR / "outputs"
MODELO_DIR = BASE_DIR / "modelo"
REPORTS_DIR = BASE_DIR / "reports"
FIGURAS_DIR = REPORTS_DIR / "figuras"
SQL_DIR = BASE_DIR / "sql"
DOCS_DIR = BASE_DIR / "docs"
POWERBI_DIR = BASE_DIR / "powerbi"
POWERBI_SCREENSHOTS_DIR = POWERBI_DIR / "screenshots"
APP_DIR = BASE_DIR / "app"
APP_PUBLIC_DATA_DIR = APP_DIR / "public" / "data"

RAW_CLIENTES = RAW_DIR / "clientes.csv"
RAW_CATEGORIAS = RAW_DIR / "categorias.csv"
RAW_TRANSACOES = RAW_DIR / "transacoes.csv"
PUBLIC_CHURN_MODELLING_FILE = RAW_DIR / "churn_modelling.csv"

PROCESSED_CLIENTES = PROCESSED_DIR / "clientes_tratados.csv"
PROCESSED_CATEGORIAS = PROCESSED_DIR / "categorias_tratadas.csv"
PROCESSED_TRANSACOES = PROCESSED_DIR / "transacoes_tratadas.csv"
FEATURE_BASE = PROCESSED_DIR / "base_analitica_clientes.csv"

PROCESSED_CLIENTES_LIMPO = PROCESSED_DIR / "clientes_limpo.csv"
PROCESSED_CATEGORIAS_LIMPO = PROCESSED_DIR / "categorias_limpo.csv"
PROCESSED_TRANSACOES_LIMPO = PROCESSED_DIR / "transacoes_limpo.csv"
BASE_MODELAGEM_FILE = PROCESSED_DIR / "base_modelagem.csv"

MODEL_FILE = MODELO_DIR / "model.pkl"
PREDICTIONS_FILE = OUTPUTS_DIR / "predicoes_churn.csv"
MODEL_METRICS_FILE = OUTPUTS_DIR / "metricas_modelo.json"
FEATURE_IMPORTANCE_FILE = OUTPUTS_DIR / "feature_importance.csv"
CLASSIFICATION_REPORT_FILE = OUTPUTS_DIR / "classification_report.json"
THRESHOLD_ANALYSIS_FILE = OUTPUTS_DIR / "threshold_analysis.csv"
CLIENT_STATS_FILE = OUTPUTS_DIR / "estatisticas_clientes.csv"
TRANSACTION_STATS_FILE = OUTPUTS_DIR / "estatisticas_transacoes.csv"
SUMMARY_FILE = OUTPUTS_DIR / "summary.json"
VALIDATION_REPORT_FILE = OUTPUTS_DIR / "relatorio_validacao.csv"

FRONTEND_METRICS_FILE = APP_PUBLIC_DATA_DIR / "metrics.json"
FRONTEND_PREDICTIONS_FILE = APP_PUBLIC_DATA_DIR / "predictions.json"
FRONTEND_FEATURES_FILE = APP_PUBLIC_DATA_DIR / "feature_importance.json"
FRONTEND_SUMMARY_FILE = APP_PUBLIC_DATA_DIR / "summary.json"
FRONTEND_THRESHOLD_ANALYSIS_FILE = APP_PUBLIC_DATA_DIR / "threshold_analysis.json"


def ensure_directories() -> None:
    for directory in (
        RAW_DIR,
        PROCESSED_DIR,
        OUTPUTS_DIR,
        MODELO_DIR,
        FIGURAS_DIR,
        APP_PUBLIC_DATA_DIR,
        POWERBI_SCREENSHOTS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)
