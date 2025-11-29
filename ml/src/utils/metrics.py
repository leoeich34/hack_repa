# ml/src/utils/metrics.py

from __future__ import annotations
import numpy as np


def weighted_mae(y_true, y_pred, weights=None) -> float:
    """
    WMAE = sum_i w_i * |y_i - yhat_i| / sum_i w_i

    Если weights=None, считается обычный MAE.
    """
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    if weights is None:
        return np.mean(np.abs(y_true - y_pred))

    w = np.asarray(weights)
    return float((w * np.abs(y_true - y_pred)).sum() / w.sum())
