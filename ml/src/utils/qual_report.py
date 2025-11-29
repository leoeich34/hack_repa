# ml/src/utils/data_quality_report.py

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "income_train.csv"
TEST_PATH = DATA_DIR / "income_test.csv"


def load_dataframe(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        sep=";",
        decimal=",",
        low_memory=False
    )
    if "dt" in df.columns:
        df["dt"] = pd.to_datetime(df["dt"])
    return df


def build_data_quality_report(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    """
    Формирует единый датафрейм с:
    - типами колонок
    - долей пропусков
    - числом уникальных значений
    - признаком наличия колонки в train/test
    """
    columns_union = sorted(set(train_df.columns) | set(test_df.columns))

    rows: list[dict] = []
    for col in columns_union:
        row: dict = {"column": col}

        if col in train_df.columns:
            row["in_train"] = True
            row["dtype_train"] = str(train_df[col].dtype)
            row["missing_share_train"] = float(train_df[col].isna().mean())
            row["nunique_train"] = int(train_df[col].nunique(dropna=True))
        else:
            row["in_train"] = False
            row["dtype_train"] = None
            row["missing_share_train"] = None
            row["nunique_train"] = None

        if col in test_df.columns:
            row["in_test"] = True
            row["dtype_test"] = str(test_df[col].dtype)
            row["missing_share_test"] = float(test_df[col].isna().mean())
            row["nunique_test"] = int(test_df[col].nunique(dropna=True))
        else:
            row["in_test"] = False
            row["dtype_test"] = None
            row["missing_share_test"] = None
            row["nunique_test"] = None

        rows.append(row)

    report_df = pd.DataFrame(rows).sort_values("column").reset_index(drop=True)
    return report_df


def main() -> None:
    print("Loading train and test...")
    train_df = load_dataframe(TRAIN_PATH)
    test_df = load_dataframe(TEST_PATH)

    print("Building data quality report...")
    report_df = build_data_quality_report(train_df, test_df)

    out_path = REPORTS_DIR / "data_quality_report.csv"
    report_df.to_csv(out_path, index=False)
    print(f"Saved data quality report to: {out_path}")

    print("Done data_quality_report.")


if __name__ == "__main__":
    main()
