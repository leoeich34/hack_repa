from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from ml.src.data.load_data import load_train_clean
from ml.src.utils.metrics import weighted_mae


def time_split_train_valid(df: pd.DataFrame):
    last_date = df["dt"].max().date()
    train_df = df[df["dt"].dt.date < last_date].copy()
    valid_df = df[df["dt"].dt.date == last_date].copy()
    return train_df, valid_df


def baseline_constant(train_df: pd.DataFrame, valid_df: pd.DataFrame) -> None:
    y_train = train_df["target"].values
    y_valid = valid_df["target"].values
    w_valid = valid_df["w"].values

    mean_pred = np.full_like(y_valid, y_train.mean())
    median_pred = np.full_like(y_valid, np.median(y_train))

    wmae_mean = weighted_mae(y_valid, mean_pred, w_valid)
    wmae_median = weighted_mae(y_valid, median_pred, w_valid)

    print("=== Constant baselines ===")
    print(f"WMAE (constant = global mean):   {wmae_mean:.4f}")
    print(f"WMAE (constant = global median): {wmae_median:.4f}")


def baseline_month_median(train_df: pd.DataFrame, valid_df: pd.DataFrame) -> None:
    train_df = train_df.copy()
    valid_df = valid_df.copy()

    train_df["month"] = train_df["dt"].dt.to_period("M")
    valid_df["month"] = valid_df["dt"].dt.to_period("M")

    # медиана по месяцу на train (хотя у нас валид отдельно последним месяцем)
    month_medians = train_df.groupby("month")["target"].median().to_dict()

    # для валида — берём медиану последнего месяца, если есть,
    # иначе глобальную медиану
    global_median = train_df["target"].median()
    last_month = valid_df["month"].iloc[0]
    mmed = month_medians.get(last_month, global_median)

    y_valid = valid_df["target"].values
    w_valid = valid_df["w"].values
    preds = np.full_like(y_valid, mmed)

    wmae_month = weighted_mae(y_valid, preds, w_valid)
    print("\n=== Month baseline ===")
    print(f"WMAE (constant = median of last month on train): {wmae_month:.4f}")


def main() -> None:
    df = load_train_clean()
    train_df, valid_df = time_split_train_valid(df)

    print(f"Train: {train_df.shape}, valid: {valid_df.shape}")
    baseline_constant(train_df, valid_df)
    baseline_month_median(train_df, valid_df)


if __name__ == "__main__":
    main()
