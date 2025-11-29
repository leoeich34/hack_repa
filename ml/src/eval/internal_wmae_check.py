# ml/src/eval/internal_wmae_check.py

from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

from ml.src.utils.metrics import weighted_mae


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
CONFIG_DIR = PROJECT_ROOT / "ml" / "reports"   # тут лежит feature_lists_summary.json
DATA_PATH = DATA_DIR / "income_train_clean.csv"
FEATURE_LISTS_PATH = CONFIG_DIR / "feature_lists_summary.json"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        DATA_PATH,
        sep=";",
        decimal=",",
        low_memory=False,
    )
    df["dt"] = pd.to_datetime(df["dt"])
    return df


def load_feature_list(mode: str = "full") -> List[str]:
    """
    mode:
      - "full"  -> использовать features_final (FULL-модель)
      - "no_leak" -> если позже добавите в JSON features_no_leak
    """
    import json

    with open(FEATURE_LISTS_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    if mode == "full":
        return config["features_final"]
    elif mode == "no_leak":
        return config["features_no_leak"]
    else:
        raise ValueError(f"Unknown mode: {mode}")


def split_by_time(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Делим на train_internal и test_internal:
    - train_internal: все даты до последней
    - test_internal: последняя дата (обычно 2024-06-30)
    """
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    test_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, test_df


def prepare_matrices(df: pd.DataFrame, feature_cols: list[str]):
    """
    Разделяем датафрейм на X, y, w + определяем cat_features.
    """
    meta_cols = ["id", "dt", "target", "w"]
    # оставляем только нужные фичи + таргет/вес, если они есть
    keep_cols = [c for c in meta_cols if c in df.columns] + feature_cols
    df = df[keep_cols].copy()

    # Разделяем
    X = df[feature_cols]
    y = df["target"].values if "target" in df.columns else None
    w = df["w"].values if "w" in df.columns else None

    # Определяем, какие признаки категориальные (по типу object)
    cat_features = X.select_dtypes(include=["object"]).columns.tolist()

    # Иммутация:
    # - числовые: медиана
    # - категориальные: "missing"
    for col in X.columns:
        if col in cat_features:
            X[col] = X[col].astype("object").fillna("missing")
        else:
            median_val = X[col].median()
            X[col] = X[col].fillna(median_val)

    return X, y, w, cat_features


def train_and_eval_internal(mode: str = "full") -> None:
    print(f"Loading data from: {DATA_PATH}")
    df = load_data()

    print("Splitting into internal train/test by time...")
    train_df, test_df = split_by_time(df)
    print(f"train_internal: {train_df.shape}, test_internal: {test_df.shape}")

    feature_cols = load_feature_list(mode=mode)
    print(f"Using {len(feature_cols)} features in mode='{mode}'")

    X_train, y_train, w_train, cat_train = prepare_matrices(train_df, feature_cols)
    X_test, y_test, w_test, cat_test = prepare_matrices(test_df, feature_cols)

    assert cat_train == cat_test, "Категориальные фичи должны совпадать"

    cat_features_idx = [X_train.columns.get_loc(c) for c in cat_train]

    train_pool = Pool(
        X_train,
        label=y_train,
        weight=w_train,
        cat_features=cat_features_idx,
    )
    test_pool = Pool(
        X_test,
        label=y_test,
        weight=w_test,
        cat_features=cat_features_idx,
    )

    model = CatBoostRegressor(
        loss_function="MAE",          # близко к нашей целевой WMAE
        depth=6,
        learning_rate=0.05,
        n_estimators=2000,
        l2_leaf_reg=3.0,
        random_seed=42,
        subsample=0.9,
        colsample_bylevel=0.9,
        verbose=200,
        eval_metric="MAE",
        od_type="Iter",
        od_wait=200,
    )

    print("Training CatBoost model...")
    model.fit(
        train_pool,
        eval_set=test_pool,  # будем смотреть на internal test
        use_best_model=True,
    )

    print("Predicting on internal test...")
    y_pred = model.predict(test_pool)

    wmae_value = weighted_mae(y_true=y_test, y_pred=y_pred, weights=w_test)
    print(f"\n=== INTERNAL WMAE ({mode}) on last month ===")
    print(f"WMAE = {wmae_value:.4f}")


if __name__ == "__main__":
    # Можно запускать с разными режимами, когда добавите no_leak
    train_and_eval_internal(mode="full")
