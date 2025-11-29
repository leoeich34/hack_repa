# ml/notebooks/01_eda_overview.py

# %%
import os
from pathlib import Path

import numpy as np
import pandas as pd

# %%
# Пути к данным (при необходимости поменяй)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "income_train.csv"
TEST_PATH = DATA_DIR / "income_test.csv"

# %%
def load_train_test(train_path: Path = TRAIN_PATH, test_path: Path = TEST_PATH) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Загружает train и test в соответствии с форматом:
    - разделитель ';'
    - десятичный разделитель ','
    - парсинг dt как даты
    """
    train_df = pd.read_csv(
        train_path,
        sep=";",
        decimal=",",
        low_memory=False
    )
    test_df = pd.read_csv(
        test_path,
        sep=";",
        decimal=",",
        low_memory=False
    )

    # Приводим dt к datetime (если есть)
    if "dt" in train_df.columns:
        train_df["dt"] = pd.to_datetime(train_df["dt"])
    if "dt" in test_df.columns:
        test_df["dt"] = pd.to_datetime(test_df["dt"])

    return train_df, test_df

# %%
def basic_overview(train_df: pd.DataFrame, test_df: pd.DataFrame) -> None:
    """
    Печатает базовую информацию по train/test и сохраняет summary в CSV.
    """
    print("=== SHAPES ===")
    print(f"train: {train_df.shape}")
    print(f"test:  {test_df.shape}")

    # Сводка по типам
    print("\n=== DTYPES (train) ===")
    print(train_df.dtypes)

    print("\n=== DTYPES (test) ===")
    print(test_df.dtypes)

    # Числовые и категориальные колонки
    numeric_cols_train = train_df.select_dtypes(include=["number"]).columns.tolist()
    object_cols_train = train_df.select_dtypes(include=["object"]).columns.tolist()
    datetime_cols_train = train_df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

    print("\n=== COLUMN TYPE COUNTS (train) ===")
    print(f"numeric:   {len(numeric_cols_train)}")
    print(f"object:    {len(object_cols_train)}")
    print(f"datetime:  {len(datetime_cols_train)}")

    # Описание таргета и весов, если есть
    if "target" in train_df.columns:
        print("\n=== TARGET describe ===")
        print(train_df["target"].describe())

    if "w" in train_df.columns:
        print("\n=== WEIGHTS (w) describe ===")
        print(train_df["w"].describe())
        print("Count of zero weights:", (train_df["w"] == 0).sum())

    # Диапазон дат
    if "dt" in train_df.columns:
        print("\n=== DATE RANGE (train.dt) ===")
        print("min dt:", train_df["dt"].min())
        print("max dt:", train_df["dt"].max())

    # Пропуски
    print("\n=== MISSING VALUES (train, top 20) ===")
    missing_train = train_df.isna().mean().sort_values(ascending=False)
    print(missing_train.head(20))

    print("\nNUMBER OF COLUMNS WITHOUT MISSING (train):")
    print(int((missing_train == 0).sum()))

    # Сохранение summary в CSV
    summary_df = pd.DataFrame({
        "column": train_df.columns,
        "dtype_train": train_df.dtypes.astype(str).values,
        "missing_share_train": train_df.isna().mean().values,
        "nunique_train": train_df.nunique().values
    })
    summary_path = REPORTS_DIR / "eda_basic_summary_train.csv"
    summary_df.to_csv(summary_path, index=False)
    print(f"\nSaved basic summary for train to: {summary_path}")

# %%
def main() -> None:
    print("Loading data...")
    train_df, test_df = load_train_test()

    print("\nRunning basic EDA overview...")
    basic_overview(train_df, test_df)

    print("\nDone 01_eda_overview.")

# %%
if __name__ == "__main__":
    main()
