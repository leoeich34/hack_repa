# ml/src/features/preprocess.py

from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd


META_COLS = ["id", "dt", "target", "w"]


def prepare_features(
    df: pd.DataFrame,
    feature_cols: List[str],
    fit_stats: dict | None = None,
) -> Tuple[pd.DataFrame, np.ndarray | None, np.ndarray | None, List[str], dict]:
    """
    Общий препроцессинг:
    - отделяем X, y, w;
    - выделяем категориальные фичи (object);
    - для числовых заполняем NaN медианой;
    - для категориальных заполняем NaN значением "missing".

    fit_stats:
      - если None -> считаем медианы и возвращаем их, чтобы потом использовать на тесте
      - если dict -> используем готовые медианы (режим инференса)

    Возвращает:
      X, y, w, cat_features (список имён категориальных фич), fit_stats.
    """
    keep_cols = [c for c in META_COLS if c in df.columns] + feature_cols
    df = df[keep_cols].copy()

    y = df["target"].values if "target" in df.columns else None
    w = df["w"].values if "w" in df.columns else None

    X = df[feature_cols].copy()

    # определяем категориальные признаки по типу
    cat_features = X.select_dtypes(include=["object"]).columns.tolist()
    num_features = [c for c in X.columns if c not in cat_features]

    if fit_stats is None:
        fit_stats = {}

    # числовые: медиана
    if "numeric_medians" not in fit_stats:
        fit_stats["numeric_medians"] = {}
        for col in num_features:
            med = X[col].median()
            fit_stats["numeric_medians"][col] = med
    for col in num_features:
        med = fit_stats["numeric_medians"].get(col, 0.0)
        X[col] = X[col].fillna(med)

    # категориальные: missing
    if "categorical_fill" not in fit_stats:
        fit_stats["categorical_fill"] = {}
        for col in cat_features:
            fit_stats["categorical_fill"][col] = "missing"
    for col in cat_features:
        fill_val = fit_stats["categorical_fill"].get(col, "missing")
        X[col] = X[col].astype("object").fillna(fill_val)

    # на всякий случай фиксируем порядок колонок
    X = X[feature_cols]

    return X, y, w, cat_features, fit_stats
