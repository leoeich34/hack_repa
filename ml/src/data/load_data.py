# ml/src/data/load_data.py

from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"

# базовые очищенные датасеты
TRAIN_CLEAN_PATH = DATA_DIR / "income_train_clean.csv"
TEST_CLEAN_PATH = DATA_DIR / "income_test_clean.csv"

# датасеты с feature engineering
TRAIN_FE_PATH = DATA_DIR / "income_train_fe.csv"
TEST_FE_PATH = DATA_DIR / "income_test_fe.csv"


def _load_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", decimal=",", low_memory=False)
    if "dt" in df.columns:
        df["dt"] = pd.to_datetime(df["dt"])
    return df


def load_train_clean(path: Path | None = None) -> pd.DataFrame:
    """
    Загружает очищенный train без FE.
    """
    if path is None:
        path = TRAIN_CLEAN_PATH
    return _load_csv(path)


def load_test_clean(path: Path | None = None) -> pd.DataFrame:
    """
    Загружает очищенный test без FE.
    """
    if path is None:
        path = TEST_CLEAN_PATH
    return _load_csv(path)


def load_train_fe(path: Path | None = None) -> pd.DataFrame:
    """
    Загружает train с feature engineering (income_train_fe.csv).
    """
    if path is None:
        path = TRAIN_FE_PATH
    return _load_csv(path)


def load_test_fe(path: Path | None = None) -> pd.DataFrame:
    """
    Загружает test с feature engineering (income_test_fe.csv).
    """
    if path is None:
        path = TEST_FE_PATH
    return _load_csv(path)
