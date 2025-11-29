# ml/notebooks/04_leakage_and_top_features.py

# %%
from pathlib import Path

import numpy as np
import pandas as pd

# %%
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "income_train.csv"

# %%
LEAKAGE_KEYWORDS = [
    "income",
    "salary",
    "payout",
    "earn",
    "доход",     # на всякий случай русские
    "зарплат",
]

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
def find_candidate_leakage_features(df: pd.DataFrame) -> list[str]:
    """
    Ищем фичи, потенциально связанные с доходом/зарплатой по названию.
    """
    candidate_cols: list[str] = []
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in LEAKAGE_KEYWORDS):
            candidate_cols.append(col)
    return candidate_cols

# %%
def compute_correlations_with_target(
    df: pd.DataFrame,
    candidate_columns: list[str],
    target_column: str = "target"
) -> pd.DataFrame:
    """
    Считает корреляции (по Пирсону) между candidate_columns и target.
    Только для числовых признаков.
    """
    if target_column not in df.columns:
        print(f"Target column '{target_column}' not found. Skipping correlation analysis.")
        return pd.DataFrame()

    numeric_df = df.select_dtypes(include=["number"])
    if target_column not in numeric_df.columns:
        print(f"Target column '{target_column}' is not numeric. Skipping correlation analysis.")
        return pd.DataFrame()

    valid_candidates = [c for c in candidate_columns if c in numeric_df.columns]
    rows: list[dict] = []

    for col in valid_candidates:
        series = numeric_df[col]
        target = numeric_df[target_column]

        mask = series.notna() & target.notna()
        if mask.sum() < 50:
            # слишком мало наблюдений для адекватной корреляции
            continue

        corr = series[mask].corr(target[mask])
        rows.append(
            {
                "column": col,
                "corr_with_target": float(corr),
                "n_non_null": int(mask.sum()),
            }
        )

    corr_df = pd.DataFrame(rows).sort_values("corr_with_target", key=lambda s: s.abs(), ascending=False)
    return corr_df

# %%
def main() -> None:
    print("Loading train...")
    train_df = load_train()

    print("\nFinding candidate leakage features by name...")
    candidate_leakage_features = find_candidate_leakage_features(train_df)
    print(f"Found {len(candidate_leakage_features)} candidate leakage features:")
    for col in candidate_leakage_features:
        print(f"  - {col}")

    print("\nComputing correlations with target for candidate leakage features...")
    corr_df = compute_correlations_with_target(train_df, candidate_leakage_features, target_column="target")
    if not corr_df.empty:
        corr_path = REPORTS_DIR / "candidate_leakage_correlations.csv"
        corr_df.to_csv(corr_path, index=False)
        print(f"Saved candidate leakage correlations to: {corr_path}")

        # топ-20 по модулю корреляции
        top20 = corr_df.head(20)
        top20_path = REPORTS_DIR / "top20_leakage_like_features.csv"
        top20.to_csv(top20_path, index=False)
        print(f"Saved top 20 leakage-like features to: {top20_path}")
    else:
        print("No valid numeric candidate leakage features found for correlation analysis.")

    print("\nDone 04_leakage_and_top_features.")

# %%
if __name__ == "__main__":
    main()
