# ml/src/models/train_catboost.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

from ml.src.data.load_data import load_train_clean
from ml.src.features.preprocess import prepare_features
from ml.src.utils.metrics import weighted_mae


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_LISTS_PATH = REPORTS_DIR / "feature_lists_summary.json"


def load_feature_list(mode: Literal["full", "no_leak"] = "full") -> list[str]:
    """
    Читает JSON со списками фич.

    Ожидаем ключи:
      - features_final  (для FULL)
      - features_no_leak (для CLEAN; если нет — используем features_final)
    """
    with open(FEATURE_LISTS_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    if mode == "full":
        return config.get("features_full", config.get("features_final"))
    elif mode == "no_leak":
        if "features_no_leak" in config:
            return config["features_no_leak"]
        # fallback — если не завели отдельный список, используем final
        return config.get("features_final")
    else:
        raise ValueError(f"Unknown mode: {mode}")


def time_split_train_valid(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Разбиваем по времени:
      - train: все даты, кроме последней
      - valid: последняя дата
    """
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    valid_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, valid_df


def train_model(
    mode: Literal["full", "no_leak"] = "full",
    model_name: str | None = None,
) -> None:
    """
    Обучает CatBoost-модель на очищенном train + time-based holdout.
    Сохраняет модель и meta-информацию.
    """
    if model_name is None:
        model_name = f"catboost_{mode}"

    print("Loading train data...")
    df = load_train_clean()
    print(f"Train shape: {df.shape}")

    print("Performing time-based split...")
    train_df, valid_df = time_split_train_valid(df)
    print(f"Train part: {train_df.shape}, valid part (last month): {valid_df.shape}")

    feature_cols = load_feature_list(mode=mode)
    print(f"Using {len(feature_cols)} features (mode={mode})")

    # препроцессинг
    print("Preparing features for train...")
    X_train, y_train, w_train, cat_features, fit_stats = prepare_features(
        train_df, feature_cols, fit_stats=None
    )
    print("Preparing features for valid...")
    X_valid, y_valid, w_valid, cat_features_valid, _ = prepare_features(
        valid_df, feature_cols, fit_stats=fit_stats
    )

    assert cat_features == cat_features_valid, "Набор категориальных фич должен совпадать"

    cat_features_idx = [X_train.columns.get_loc(c) for c in cat_features]

    train_pool = Pool(
        X_train,
        label=y_train,
        weight=w_train,
        cat_features=cat_features_idx,
    )
    valid_pool = Pool(
        X_valid,
        label=y_valid,
        weight=w_valid,
        cat_features=cat_features_idx,
    )

    model = CatBoostRegressor(
        loss_function="MAE",
        eval_metric="MAE",
        depth=8,
        learning_rate = 0.03,
        n_estimators = 3000,
        l2_leaf_reg = 3.0,
        subsample = 0.9,
        colsample_bylevel = 0.9,
        od_type="Iter",
        od_wait=200,
        verbose=200,
    )

    print("Training CatBoost model...")
    model.fit(
        train_pool,
        eval_set=valid_pool,
        use_best_model=True,
    )

    print("Predicting on validation...")
    y_pred_valid = model.predict(valid_pool)
    wmae_value = weighted_mae(y_valid, y_pred_valid, w_valid)
    print(f"\n=== VALID WMAE (mode={mode}) on last month ===")
    print(f"WMAE = {wmae_value:.4f}")

    # сохраняем модель
    model_path = MODELS_DIR / f"{model_name}.cbm"
    model.save_model(model_path)
    print(f"Saved model to: {model_path}")

    # сохраняем мета (какие фичи, какие статистики, какие cat_features)
    meta = {
        "mode": mode,
        "model_path": str(model_path),
        "features": feature_cols,
        "cat_features": cat_features,
        "fit_stats": fit_stats,
        "valid_wmae": float(wmae_value),
    }
    meta_path = MODELS_DIR / f"{model_name}_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Saved model meta to: {meta_path}")


if __name__ == "__main__":
    # по умолчанию учим FULL-модель
    train_model(mode="full")
