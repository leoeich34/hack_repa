# ml/src/models/predict_on_test.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from ml.src.data.load_data import (
    load_test_clean,
    load_test_fe,
)
from ml.src.features.preprocess import prepare_features


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = PROJECT_ROOT / "ml" / "models"
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
SAMPLE_SUB_PATH = DATA_DIR / "sample_submission.csv"


def load_model_and_meta(model_name: str) -> tuple[CatBoostRegressor, dict]:
    model_path = MODELS_DIR / f"{model_name}.cbm"
    meta_path = MODELS_DIR / f"{model_name}_meta.json"

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not meta_path.exists():
        raise FileNotFoundError(f"Meta file not found: {meta_path}")

    model = CatBoostRegressor()
    model.load_model(str(model_path))

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    return model, meta


def predict_test(
    model_name: str,
    output_path: Optional[Path] = None,
) -> Path:
    """
    Загружает обученную модель, считает предсказания на тесте
    и сохраняет submission.csv.

    Автоматически:
    - выбирает правильный датасет (clean или fe) по meta["mode"] / имени модели;
    - применяет обратное преобразование для лог-таргет модели, если нужно.
    """
    print(f"Loading model '{model_name}'...")
    model, meta = load_model_and_meta(model_name)
    feature_cols = meta["features"]
    fit_stats = meta["fit_stats"]
    mode = meta.get("mode", "")

    # решаем, какой датасет использовать
    use_fe = ("_fe" in mode) or model_name.endswith("_fe")
    if use_fe:
        print("Detected FE model → loading income_test_fe.csv")
        test_df = load_test_fe()
    else:
        print("Detected clean model → loading income_test_clean.csv")
        test_df = load_test_clean()

    print(f"Test shape: {test_df.shape}")

    print("Preparing test features...")
    X_test, _, _, _, _ = prepare_features(
        test_df, feature_cols, fit_stats=fit_stats
    )

    print("Predicting on test...")
    y_pred = model.predict(X_test)

    # если модель обучалась на log1p(target), вернёмся в исходный масштаб
    if meta.get("target_transform") == "log1p":
        y_pred = np.expm1(y_pred)

    # готовим сабмит
    if SAMPLE_SUB_PATH.exists():
        sample_sub = pd.read_csv(SAMPLE_SUB_PATH)
        if "id" in sample_sub.columns:
            sub = sample_sub.copy()
            target_col_candidates = [c for c in sample_sub.columns if c != "id"]
            target_col = target_col_candidates[0] if target_col_candidates else "target"
            if target_col not in sub.columns:
                sub[target_col] = y_pred
            else:
                sub[target_col] = y_pred
        else:
            sub = pd.DataFrame({"id": test_df["id"], "target": y_pred})
    else:
        sub = pd.DataFrame({"id": test_df["id"], "target": y_pred})

    if output_path is None:
        output_path = PROJECT_ROOT / "submission.csv"

    sub.to_csv(output_path, index=False)
    print(f"Saved submission to: {output_path}")

    return output_path


if __name__ == "__main__":
    # для FE-модели:
    predict_test(model_name="catboost_full_fe")
    # при желании можно поменять имя, если используешь другую модель
