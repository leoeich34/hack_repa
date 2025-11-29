from __future__ import annotations

import json
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from ml.src.data.load_data import load_test_fe
from ml.src.features.preprocess import prepare_features


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
SAMPLE_SUB_PATH = DATA_DIR / "sample_submission.csv"


def load_model_and_meta(model_name: str):
    model_path = MODELS_DIR / f"{model_name}.cbm"
    meta_path = MODELS_DIR / f"{model_name}_meta.json"

    model = CatBoostRegressor()
    model.load_model(str(model_path))

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    return model, meta


def predict_ensemble_fe(
    model_names: List[str],
    output_name: str = "submission_fe_log_ensemble.csv",
) -> Path:
    print("Loading FE test data...")
    test_df = load_test_fe()
    print(f"Test FE shape: {test_df.shape}")

    preds = []

    common_feature_cols = None
    common_fit_stats = None

    for i, name in enumerate(model_names):
        print(f"\n=== Using model: {name} ===")
        model, meta = load_model_and_meta(name)

        feature_cols = meta["features"]
        fit_stats = meta["fit_stats"]

        if common_feature_cols is None:
            common_feature_cols = feature_cols
            common_fit_stats = fit_stats
        else:
            assert feature_cols == common_feature_cols, "Feature lists differ between models!"

        X_test, _, _, _, _ = prepare_features(
            test_df, common_feature_cols, fit_stats=common_fit_stats
        )

        y_pred = model.predict(X_test)

        if meta.get("target_transform") == "log1p":
            y_pred = np.expm1(y_pred)

        preds.append(y_pred)

    print("\nAveraging predictions ...")
    y_pred_mean = np.mean(preds, axis=0)

    # считаем ансамбль и записываем в отправку
    if SAMPLE_SUB_PATH.exists():
        sample_sub = pd.read_csv(SAMPLE_SUB_PATH)
        if "id" in sample_sub.columns:
            sub = sample_sub.copy()
            target_col_candidates = [c for c in sub.columns if c != "id"]
            target_col = target_col_candidates[0] if target_col_candidates else "target"
            sub[target_col] = y_pred_mean
        else:
            sub = pd.DataFrame({"id": test_df["id"], "target": y_pred_mean})
    else:
        sub = pd.DataFrame({"id": test_df["id"], "target": y_pred_mean})

    out_path = PROJECT_ROOT / output_name
    sub.to_csv(out_path, index=False)
    print(f"\nSaved FE+LOG ensemble submission to: {out_path}")
    return out_path


def main() -> None:
    model_names = [
        "catboost_full_fe_log_s42",
        "catboost_full_fe_log_s43",
        "catboost_full_fe_log_s44",
    ]
    predict_ensemble_fe(model_names)


if __name__ == "__main__":
    main()
