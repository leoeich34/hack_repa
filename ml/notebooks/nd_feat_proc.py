# ml/notebooks/02_feature_typing_and_missing.py

# %%
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd

# %%
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
CONFIG_DIR = PROJECT_ROOT / "ml" / "src" / "config"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "income_train.csv"
TEST_PATH = DATA_DIR / "income_test.csv"

# %%
def load_train(train_path: Path = TRAIN_PATH) -> pd.DataFrame:
    train_df = pd.read_csv(
        train_path,
        sep=";",
        decimal=",",
        low_memory=False
    )
    if "dt" in train_df.columns:
        train_df["dt"] = pd.to_datetime(train_df["dt"])
    return train_df

# %%
def detect_feature_types(
    df: pd.DataFrame,
    numeric_as_object_threshold: float = 0.9,
    high_card_threshold: int = 100
) -> pd.DataFrame:
    """
    Определяет типы фич:
    - numeric: числовые типы
    - datetime: datetime
    - numeric_from_string: object, которые почти полностью состоят из чисел
    - categorical_low_card: категориальные с небольшим количеством уникальных значений
    - categorical_high_card: категориальные с большим количеством уникальных значений
    """
    result_rows: list[dict] = []

    for col in df.columns:
        raw_dtype = str(df[col].dtype)
        nunique = df[col].nunique(dropna=True)
        missing_share = df[col].isna().mean()

        interpreted_type: str
        subtype: str | None = None

        if np.issubdtype(df[col].dtype, np.number):
            interpreted_type = "numeric"
            subtype = None
        elif np.issubdtype(df[col].dtype, "datetime64[ns]"):
            interpreted_type = "datetime"
            subtype = None
        elif raw_dtype == "object":
            # Пробуем привести к числу
            numeric_series = pd.to_numeric(df[col].astype(str).str.replace(",", "."), errors="coerce")
            non_na_ratio = numeric_series.notna().mean()

            if non_na_ratio >= numeric_as_object_threshold:
                interpreted_type = "numeric_from_string"
                subtype = None
            else:
                # Категориальный
                if nunique <= high_card_threshold:
                    interpreted_type = "categorical"
                    subtype = "low_card"
                else:
                    interpreted_type = "categorical"
                    subtype = "high_card"
        else:
            interpreted_type = "other"
            subtype = None

        result_rows.append(
            {
                "column": col,
                "raw_dtype": raw_dtype,
                "interpreted_type": interpreted_type,
                "subtype": subtype,
                "nunique": int(nunique),
                "missing_share": float(missing_share),
            }
        )

    result_df = pd.DataFrame(result_rows).sort_values("column").reset_index(drop=True)
    return result_df

# %%
def main() -> None:
    print("Loading train...")
    train_df = load_train()

    print("Detecting feature types...")
    feature_types_df = detect_feature_types(train_df)

    feature_types_path = REPORTS_DIR / "feature_types_summary.csv"
    feature_types_df.to_csv(feature_types_path, index=False)
    print(f"Saved feature type summary to: {feature_types_path}")

    # Дополнительно формируем списки по типам, которые потом удобно использовать в DS-части
    numeric_features = feature_types_df[
        feature_types_df["interpreted_type"].isin(["numeric", "numeric_from_string"])
    ]["column"].tolist()

    datetime_features = feature_types_df[
        feature_types_df["interpreted_type"] == "datetime"
    ]["column"].tolist()

    categorical_low_card = feature_types_df[
        (feature_types_df["interpreted_type"] == "categorical")
        & (feature_types_df["subtype"] == "low_card")
    ]["column"].tolist()

    categorical_high_card = feature_types_df[
        (feature_types_df["interpreted_type"] == "categorical")
        & (feature_types_df["subtype"] == "high_card")
    ]["column"].tolist()

    # Целевые/служебные колонки вынесем отдельно, если они есть
    target_columns = [c for c in ["target"] if c in train_df.columns]
    weight_columns = [c for c in ["w"] if c in train_df.columns]
    id_columns = [c for c in ["id"] if c in train_df.columns]
    date_columns = datetime_features

    config_like = {
        "meta_columns": {
            "id_columns": id_columns,
            "date_columns": date_columns,
            "target_columns": target_columns,
            "weight_columns": weight_columns,
        },
        "feature_lists": {
            "numeric_features": numeric_features,
            "categorical_low_card": categorical_low_card,
            "categorical_high_card": categorical_high_card,
        },
    }

    feature_lists_path = CONFIG_DIR / "feature_lists_autodetected.json"
    pd.Series(config_like).to_json(feature_lists_path)
    print(f"Saved auto-detected feature lists to: {feature_lists_path}")

    # Дополнительно сохраним информацию о пропусках
    missing_info = train_df.isna().mean().reset_index()
    missing_info.columns = ["column", "missing_share"]
    missing_info_path = REPORTS_DIR / "missing_share_train.csv"
    missing_info.to_csv(missing_info_path, index=False)
    print(f"Saved missing share info to: {missing_info_path}")

    print("\nDone 02_feature_typing_and_missing.")

# %%
if __name__ == "__main__":
    main()
