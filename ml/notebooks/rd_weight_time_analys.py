# ml/notebooks/03_weights_and_time_analysis.py

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
def analyze_weights(train_df: pd.DataFrame) -> pd.DataFrame:
    if "w" not in train_df.columns:
        print("Column 'w' not found in train. Skipping weights analysis.")
        return pd.DataFrame()

    w = train_df["w"]
    print("=== WEIGHTS (w) BASIC STATS ===")
    print(w.describe())
    print("Count of zero weights:", (w == 0).sum())

    quantiles = w.quantile([0.0, 0.01, 0.05, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0])
    print("\n=== WEIGHTS (w) QUANTILES ===")
    print(quantiles)

    share_high = (w > 1.0).mean()
    share_very_high = (w > 2.0).mean()
    print(f"\nShare of w > 1.0: {share_high:.4f}")
    print(f"Share of w > 2.0: {share_very_high:.4f}")

    return quantiles.to_frame(name="w_quantile")

# %%
def analyze_target_over_time(train_df: pd.DataFrame) -> pd.DataFrame:
    if "dt" not in train_df.columns or "target" not in train_df.columns:
        print("Columns 'dt' or 'target' not found in train. Skipping time analysis.")
        return pd.DataFrame()

    df = train_df[["dt", "target", "w"]].copy() if "w" in train_df.columns else train_df[["dt", "target"]].copy()

    df["date"] = df["dt"].dt.date

    agg_funcs = {
        "target": ["count", "mean", "median", "min", "max"]
    }
    if "w" in df.columns:
        agg_funcs["w"] = ["mean", "min", "max"]

    grouped = df.groupby("date").agg(agg_funcs)
    grouped.columns = ["_".join(col).strip() for col in grouped.columns.values]
    grouped = grouped.reset_index().sort_values("date")

    print("\n=== TARGET OVER TIME (by date) ===")
    print(grouped.head())

    return grouped

# %%
def main() -> None:
    print("Loading train...")
    train_df = load_train()

    print("\nAnalyzing weights...")
    w_quantiles = analyze_weights(train_df)
    if not w_quantiles.empty:
        w_quantiles_path = REPORTS_DIR / "weights_quantiles.csv"
        w_quantiles.to_csv(w_quantiles_path)
        print(f"Saved weights quantiles to: {w_quantiles_path}")

    print("\nAnalyzing target over time...")
    target_over_time = analyze_target_over_time(train_df)
    if not target_over_time.empty:
        target_over_time_path = REPORTS_DIR / "target_over_time.csv"
        target_over_time.to_csv(target_over_time_path, index=False)
        print(f"Saved target over time to: {target_over_time_path}")

    print("\nDone 03_weights_and_time_analysis.")

# %%
if __name__ == "__main__":
    main()
