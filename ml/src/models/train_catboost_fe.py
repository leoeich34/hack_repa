# ml/src/models/train_catboost_fe.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import pandas as pd
from catboost import CatBoostRegressor, Pool

from ml.src.features.preprocess import prepare_features
from ml.src.utils.metrics import weighted_mae


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_FE_PATH = DATA_DIR / "income_train_fe.csv"
FEATURE_LISTS_FE_PATH = REPORTS_DIR / "feature_lists_summary_fe.json"


def load_train_fe() -> pd.DataFrame:
    df = pd.read_csv(TRAIN_FE_PATH, sep=";", decimal=",", low_memory=False)
    if "dt" in df.columns:
        df["dt"] = pd.to_datetime(df["dt"])
    return df


def load_feature_list_fe(mode: Literal["full_fe"] = "full_fe") -> list[str]:
    with open(FEATURE_LISTS_FE_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if mode == "full_fe":
        return cfg["features_final_fe"]
    else:
        raise ValueError(f"Unknown mode: {mode}")


def time_split_train_valid(df: pd.DataFrame):
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    valid_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, valid_df


def train_model_fe(
    mode: Literal["full_fe"] = "full_fe",
    model_name: str | None = None,
) -> None:
    if model_name is None:
        model_name = f"catboost_{mode}"

    print(f"Loading FE train from: {TRAIN_FE_PATH}")
    df = load_train_fe()
    print(f"Train FE shape: {df.shape}")

    print("Time-based split...")
    train_df, valid_df = time_split_train_valid(df)
    print(f"Train: {train_df.shape}, valid: {valid_df.shape}")

    feature_cols = load_feature_list_fe(mode=mode)
    print(f"Using {len(feature_cols)} features (mode={mode})")

    print("Preparing features...")
    X_train, y_train, w_train, cat_features, fit_stats = prepare_features(
        train_df, feature_cols, fit_stats=None
    )
    X_valid, y_valid, w_valid, cat_features_valid, _ = prepare_features(
        valid_df, feature_cols, fit_stats=fit_stats
    )

    assert cat_features == cat_features_valid
    cat_idx = [X_train.columns.get_loc(c) for c in cat_features]

    train_pool = Pool(X_train, label=y_train, weight=w_train, cat_features=cat_idx)
    valid_pool = Pool(X_valid, label=y_valid, weight=w_valid, cat_features=cat_idx)

    model = CatBoostRegressor(
        loss_function="MAE",
        eval_metric="MAE",
        depth=8,
        learning_rate=0.03,
        n_estimators=3000,
        l2_leaf_reg=3.0,
        subsample=0.9,
        colsample_bylevel=0.9,
        random_seed=42,
        od_type="Iter",
        od_wait=200,
        verbose=200,
    )

    print("Training CatBoost on FE data...")
    model.fit(train_pool, eval_set=valid_pool, use_best_model=True)

    print("Predicting on validation...")
    y_pred_valid = model.predict(valid_pool)
    wmae_value = weighted_mae(y_valid, y_pred_valid, w_valid)
    print(f"\n=== VALID WMAE (FE, mode={mode}) on last month ===")
    print(f"WMAE = {wmae_value:.4f}")

    model_path = MODELS_DIR / f"{model_name}.cbm"
    model.save_model(model_path)
    print(f"Saved FE model to: {model_path}")

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
    print(f"Saved FE model meta to: {meta_path}")


if __name__ == "__main__":
    train_model_fe(mode="full_fe")
