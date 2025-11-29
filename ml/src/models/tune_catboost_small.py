from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

import pandas as pd
from catboost import CatBoostRegressor, Pool

from ml.src.data.load_data import load_train_clean
from ml.src.features.preprocess import prepare_features
from ml.src.utils.metrics import weighted_mae


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
FEATURE_LISTS_PATH = REPORTS_DIR / "feature_lists_summary.json"


def load_feature_list(mode: Literal["full", "no_leak"] = "full") -> list[str]:
    with open(FEATURE_LISTS_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if mode == "full":
        return cfg.get("features_full", cfg.get("features_final"))
    elif mode == "no_leak":
        return cfg.get("features_no_leak", cfg.get("features_final"))
    raise ValueError(mode)


def time_split(df: pd.DataFrame):
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    valid_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, valid_df


def run_single_config(params: dict, mode: str = "full") -> float:
    print(f"\n=== Config: {params} (mode={mode}) ===")
    df = load_train_clean()
    train_df, valid_df = time_split(df)

    feature_cols = load_feature_list(mode=mode)

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

    base_params = dict(
        loss_function="MAE",
        eval_metric="MAE",
        random_seed=42,
        od_type="Iter",
        od_wait=200,
        verbose=200,
    )
    base_params.update(params)

    model = CatBoostRegressor(**base_params)
    model.fit(train_pool, eval_set=valid_pool, use_best_model=True)

    y_pred = model.predict(valid_pool)
    wmae_val = weighted_mae(y_valid, y_pred, w_valid)
    print(f"WMAE: {wmae_val:.4f}")
    return wmae_val


def main():
    # Небольшая сетка конфигов
    configs = [
        # твой текущий лучший
        {"depth": 8, "learning_rate": 0.03, "n_estimators": 3000, "l2_leaf_reg": 3.0, "subsample": 0.9,
         "colsample_bylevel": 0.9},

        # чуть глубже, помедленнее
        {"depth": 9, "learning_rate": 0.025, "n_estimators": 3500, "l2_leaf_reg": 3.0, "subsample": 0.9,
         "colsample_bylevel": 0.9},

        # меньше depth, чуть быстрее lr, но больше деревьев
        {"depth": 7, "learning_rate": 0.035, "n_estimators": 3200, "l2_leaf_reg": 3.0, "subsample": 0.9,
         "colsample_bylevel": 0.9},

        # усилить регуляризацию
        {"depth": 8, "learning_rate": 0.03, "n_estimators": 3200, "l2_leaf_reg": 5.0, "subsample": 0.9,
         "colsample_bylevel": 0.9},

        # чуть меньше subsample — больше рандома
        {"depth": 8, "learning_rate": 0.03, "n_estimators": 3200, "l2_leaf_reg": 3.0, "subsample": 0.75,
         "colsample_bylevel": 0.9},
    ]

    results = []
    for cfg in configs:
        wmae = run_single_config(cfg, mode="full")
        results.append((cfg, wmae))

    print("\n=== Summary ===")
    for cfg, wmae in sorted(results, key=lambda x: x[1]):
        print(f"WMAE={wmae:.4f}  cfg={cfg}")


if __name__ == "__main__":
    main()
