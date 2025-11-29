# ml/src/features/add_engineered_features.py

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"

TRAIN_CLEAN_PATH = DATA_DIR / "income_train_clean.csv"
TEST_CLEAN_PATH = DATA_DIR / "income_test_clean.csv"

TRAIN_FE_PATH = DATA_DIR / "income_train_fe.csv"
TEST_FE_PATH = DATA_DIR / "income_test_fe.csv"

FEATURE_LISTS_PATH = REPORTS_DIR / "feature_lists_summary.json"


BKI_LIMIT_COLS = [
    "hdb_bki_total_max_limit",
    "hdb_bki_total_cc_max_limit",
    "hdb_bki_total_pil_max_limit",
    "hdb_bki_total_auto_max_limit",
    "hdb_bki_total_ip_max_limit",
    "bki_total_max_limit",
    "bki_total_il_max_limit",
]

BKI_DEBT_COLS = [
    "hdb_bki_other_active_pil_outstanding",
    "hdb_bki_other_active_ip_outstanding",
    "hdb_bki_active_cc_max_outstand",
    "bki_total_ip_max_outstand",
]

TOTAL_PRODUCTS_COLS = [
    "hdb_bki_total_products",
    "bki_total_products",
]


def sum_existing(df: pd.DataFrame, cols: List[str]) -> pd.Series:
    """
    Складывает только существующие колонки, заранее приводя их к float.
    """
    existing = [c for c in cols if c in df.columns]
    if not existing:
        return pd.Series(0.0, index=df.index)

    block = df[existing].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    return block.sum(axis=1)


def cast_numeric(df: pd.DataFrame, cols: List[str]) -> None:
    """
    In-place приводит список колонок к числам (float), если они есть в df.
    """
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")


def add_fe_block(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # все колонки, которые должны быть числовыми
    numeric_expected = (
        BKI_LIMIT_COLS
        + BKI_DEBT_COLS
        + TOTAL_PRODUCTS_COLS
        + [
            "incomeValue",
            "per_capita_income_rur_amt",
            "salary_median_in_gex_r1",
            "salary_6to12m_avg",
            "dp_ils_avg_salary_3y",
            "profit_income_out_rur_amt_l2m",
            "profit_income_out_rur_amt_9m",
            "profit_income_out_rur_amt_12m",
        ]
    )
    cast_numeric(df, numeric_expected)

    # BKI aggregate features
    df["fe_bki_total_limit"] = sum_existing(df, BKI_LIMIT_COLS)
    df["fe_bki_total_debt"] = sum_existing(df, BKI_DEBT_COLS)

    denom_limit = df["fe_bki_total_limit"].abs() + 1.0
    df["fe_bki_utilization"] = df["fe_bki_total_debt"] / denom_limit

    total_products = sum_existing(df, TOTAL_PRODUCTS_COLS)
    df["fe_bki_limit_per_product"] = df["fe_bki_total_limit"] / (total_products + 1.0)

    # Income vs region / salaries
    if "incomeValue" in df.columns and "per_capita_income_rur_amt" in df.columns:
        df["fe_income_to_region_per_capita"] = df["incomeValue"] / (
            df["per_capita_income_rur_amt"].abs() + 1.0
        )
    else:
        df["fe_income_to_region_per_capita"] = 0.0

    if "incomeValue" in df.columns and "salary_median_in_gex_r1" in df.columns:
        df["fe_income_to_region_salary_median"] = df["incomeValue"] / (
            df["salary_median_in_gex_r1"].abs() + 1.0
        )
    else:
        df["fe_income_to_region_salary_median"] = 0.0

    if "salary_6to12m_avg" in df.columns and "dp_ils_avg_salary_3y" in df.columns:
        df["fe_salary_6to12_to_ils_3y"] = df["salary_6to12m_avg"] / (
            df["dp_ils_avg_salary_3y"].abs() + 1.0
        )
    else:
        df["fe_salary_6to12_to_ils_3y"] = 0.0

    # Income dynamics
    if (
        "profit_income_out_rur_amt_l2m" in df.columns
        and "profit_income_out_rur_amt_12m" in df.columns
    ):
        df["fe_profit_l2m_to_12m"] = df["profit_income_out_rur_amt_l2m"] / (
            df["profit_income_out_rur_amt_12m"].abs() + 1.0
        )
    else:
        df["fe_profit_l2m_to_12m"] = 0.0

    if (
        "profit_income_out_rur_amt_9m" in df.columns
        and "profit_income_out_rur_amt_12m" in df.columns
    ):
        df["fe_profit_9m_to_12m"] = df["profit_income_out_rur_amt_9m"] / (
            df["profit_income_out_rur_amt_12m"].abs() + 1.0
        )
    else:
        df["fe_profit_9m_to_12m"] = 0.0

    return df


def update_feature_lists(new_feature_names: List[str]) -> None:
    with open(FEATURE_LISTS_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    base_final = cfg.get("features_final", [])
    meta_cols = {"id", "dt", "target", "w"}
    base_final = [c for c in base_final if c not in meta_cols]

    features_final_fe = base_final + new_feature_names
    features_final_fe = sorted(list(dict.fromkeys(features_final_fe)))

    cfg["features_final_fe"] = features_final_fe

    out_path = REPORTS_DIR / "feature_lists_summary_fe.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    print(f"Updated feature lists with FE and saved to: {out_path}")
    print(f"Total features_final_fe: {len(features_final_fe)}")


def main() -> None:
    print(f"Loading train from: {TRAIN_CLEAN_PATH}")
    train_df = pd.read_csv(TRAIN_CLEAN_PATH, sep=";", decimal=",", low_memory=False)
    print(f"Train shape before FE: {train_df.shape}")

    print(f"Loading test from: {TEST_CLEAN_PATH}")
    test_df = pd.read_csv(TEST_CLEAN_PATH, sep=";", decimal=",", low_memory=False)
    print(f"Test shape before FE: {test_df.shape}")

    train_fe = add_fe_block(train_df)
    test_fe = add_fe_block(test_df)

    print(f"Train shape after FE: {train_fe.shape}")
    print(f"Test shape after FE: {test_fe.shape}")

    train_fe.to_csv(TRAIN_FE_PATH, sep=";", decimal=",", index=False)
    test_fe.to_csv(TEST_FE_PATH, sep=";", decimal=",", index=False)
    print(f"Saved FE train to: {TRAIN_FE_PATH}")
    print(f"Saved FE test  to: {TEST_FE_PATH}")

    new_features = [c for c in train_fe.columns if c.startswith("fe_")]
    print(f"New FE features: {new_features}")

    update_feature_lists(new_features)


if __name__ == "__main__":
    main()
