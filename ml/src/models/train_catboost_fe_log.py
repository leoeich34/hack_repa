from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, List

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor, Pool

from ml.src.data.load_data import load_train_fe
from ml.src.features.preprocess import prepare_features
from ml.src.utils.metrics import weighted_mae


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

FEATURE_LISTS_FE_PATH = REPORTS_DIR / "feature_lists_summary_fe.json"


def load_feature_list_fe(mode: Literal["full_fe"] = "full_fe") -> list[str]:
    with open(FEATURE_LISTS_FE_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if mode == "full_fe":
        return cfg["features_final_fe"]
    else:
        raise ValueError(f"Unknown mode: {mode}")


def time_split_train_valid(df: pd.DataFrame):
    """
    Тайм-сплит: последний месяц -> валидация, остальное -> train
    """
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    valid_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, valid_df


def train_single_seed(
    seed: int,
    mode: Literal["full_fe"] = "full_fe",
) -> dict:
    model_name = f"catboost_full_fe_log_s{seed}"

    print(f"\n==============================")
    print(f"Training FE+LOG CatBoost, seed={seed}, mode={mode}")
    print(f"==============================")

    df = load_train_fe()
    print(f"Train FE shape: {df.shape}")

    train_df, valid_df = time_split_train_valid(df)
    print(f"Train: {train_df.shape}, valid: {valid_df.shape}")

    feature_cols = load_feature_list_fe(mode=mode)
    print(f"Using {len(feature_cols)} features (mode={mode})")

    # подготовка фич
    X_train, y_train, w_train, cat_features, fit_stats = prepare_features(
        train_df, feature_cols, fit_stats=None
    )
    X_valid, y_valid, w_valid, cat_features_valid, _ = prepare_features(
        valid_df, feature_cols, fit_stats=fit_stats
    )
    assert cat_features == cat_features_valid


    y_train_log = np.log1p(y_train)
    y_valid_log = np.log1p(y_valid)

    cat_idx = [X_train.columns.get_loc(c) for c in cat_features]

    train_pool = Pool(X_train, label=y_train_log, weight=w_train, cat_features=cat_idx)
    valid_pool = Pool(X_valid, label=y_valid_log, weight=w_valid, cat_features=cat_idx)


    model = CatBoostRegressor(
        loss_function="RMSE",
        eval_metric="RMSE",
        depth=8,
        learning_rate=0.03,
        n_estimators=3500,
        l2_leaf_reg=3.0,
        subsample=0.9,
        colsample_bylevel=0.9,
        random_seed=seed,
        od_type="Iter",
        od_wait=200,
        verbose=200,
    )

    print("Training CatBoost (FE + log-target)...")
    model.fit(train_pool, eval_set=valid_pool, use_best_model=True)

    print("Predicting on validation (with inverse log) ...")
    y_pred_log_valid = model.predict(valid_pool)
    y_pred_valid = np.expm1(y_pred_log_valid)

    wmae_value = weighted_mae(y_valid, y_pred_valid, w_valid)
    print(f"\n=== VALID WMAE (FE + LOG, seed={seed}) on last month ===")
    print(f"WMAE = {wmae_value:.4f}")

    # сохраняем модель и мету
    model_path = MODELS_DIR / f"{model_name}.cbm"
    model.save_model(model_path)
    print(f"Saved FE+LOG model to: {model_path}")

    meta = {
        "mode": "full_fe_log",
        "seed": seed,
        "model_path": str(model_path),
        "features": feature_cols,
        "cat_features": cat_features,
        "fit_stats": fit_stats,
        "valid_wmae": float(wmae_value),
        "target_transform": "log1p",
    }
    meta_path = MODELS_DIR / f"{model_name}_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Saved FE+LOG model meta to: {meta_path}")

    return {
        "seed": seed,
        "model_name": model_name,
        "valid_wmae": float(wmae_value),
    }


def main() -> None:
    seeds: List[int] = [42, 43, 44]

    results = []
    for s in seeds:
        res = train_single_seed(seed=s, mode="full_fe")
        results.append(res)

    print("\n======== SUMMARY (FE + LOG, multi-seed) ========")
    for r in sorted(results, key=lambda x: x["valid_wmae"]):
        print(f"seed={r['seed']}  model={r['model_name']}  WMAE={r['valid_wmae']:.4f}")


if __name__ == "__main__":
    main()
