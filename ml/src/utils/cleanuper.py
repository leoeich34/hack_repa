from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


# Строим пути относительно корня проекта:
# project-root/
#   ml/
#     data/raw/
#     src/utils/prepare_clean_datasets.py   <-- этот файл
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "ml" / "data" / "raw"
REPORTS_DIR = PROJECT_ROOT / "ml" / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

TRAIN_PATH = DATA_DIR / "hackathon_income_train.csv"
TEST_PATH = DATA_DIR / "hackathon_income_test.csv"
FEATURES_DESC_PATH = DATA_DIR / "features_description.csv"

# Ключевые слова для income/зарплаты/доходов
INCOME_KEYWORDS = [
    "доход",
    "зарплат",
    "income",
    "salary",
    "payout",
    "profit",
]


def load_feature_description(path: Path = FEATURES_DESC_PATH) -> pd.DataFrame:
    """
    Загружает файл с описанием признаков (features_description.csv).
    Пытается несколько кодировок, чтобы не ловить проблемы с UTF-8/CP1251.
    """
    encodings = ["utf-8", "cp1251", "cp866"]
    last_error: Exception | None = None
    df: pd.DataFrame | None = None

    for enc in encodings:
        try:
            df = pd.read_csv(path, sep=";", encoding=enc)
            break
        except Exception as e:  # noqa: BLE001
            last_error = e

    if df is None:
        raise RuntimeError(
            f"Не удалось прочитать {path} ни в одной кодировке. Последняя ошибка: {last_error}"
        )

    expected_cols = {"признак", "описание"}
    if not expected_cols.issubset(set(df.columns)):
        raise ValueError(
            f"Файл описания признаков должен содержать колонки {expected_cols}, "
            f"найдено: {df.columns}"
        )

    return df


def load_train(train_path: Path = TRAIN_PATH) -> pd.DataFrame:
    """
    Загружает обучающую выборку.
    """
    df = pd.read_csv(
        train_path,
        sep=";",
        decimal=",",
        low_memory=False,
    )
    if "dt" in df.columns:
        df["dt"] = pd.to_datetime(df["dt"])
    return df


def load_test(test_path: Path = TEST_PATH) -> pd.DataFrame:
    """
    Загружает тестовую выборку.
    """
    df = pd.read_csv(
        test_path,
        sep=";",
        decimal=",",
        low_memory=False,
    )
    if "dt" in df.columns:
        df["dt"] = pd.to_datetime(df["dt"])
    return df


def detect_income_related_features(desc_df: pd.DataFrame) -> pd.DataFrame:
    """
    Находит признаки, связанные с доходом/зарплатой/платежами по названию или описанию.
    """
    pattern = "|".join(INCOME_KEYWORDS)
    mask = desc_df["описание"].str.lower().str.contains(pattern) | desc_df["признак"].str.lower().str.contains(pattern)
    income_feats = desc_df[mask].copy()
    income_feats["tag"] = "income_related"
    return income_feats


def compute_numeric_correlations(train_df: pd.DataFrame, max_features: int | None = None) -> pd.DataFrame:
    """
    Считает корреляции числовых фич с target.
    Важный момент: это не взвешенная корреляция, но для отбора фич для EDA этого достаточно.
    """
    if "target" not in train_df.columns:
        raise ValueError("Колонка 'target' не найдена в train_df.")

    numeric_cols = train_df.select_dtypes(include=["number"]).columns.tolist()
    ignore_cols = {"target", "w"}
    feature_cols = [c for c in numeric_cols if c not in ignore_cols]

    rows: list[dict] = []

    for col in feature_cols:
        series = train_df[col]
        mask = series.notna() & train_df["target"].notna()
        if mask.sum() < 100:
            # Слишком мало наблюдений, корреляция будет шумной
            continue

        corr = series[mask].corr(train_df.loc[mask, "target"])
        missing_share = float(series.isna().mean())
        rows.append(
            {
                "feature": col,
                "corr_with_target": float(corr),
                "abs_corr_with_target": float(abs(corr)),
                "missing_share": missing_share,
                "n_non_null": int(mask.sum()),
            }
        )

    corr_df = pd.DataFrame(rows).sort_values("abs_corr_with_target", ascending=False)

    if max_features is not None:
        corr_df = corr_df.head(max_features)

    return corr_df


def build_clean_feature_set(
    train_df: pd.DataFrame,
    desc_df: pd.DataFrame,
    missing_threshold: float = 0.95,
    drop_income_related: bool = False,
) -> Dict[str, List[str]]:
    """
    Формирует список признаков, которые будем использовать в модели.

    Правила:
    - исключаем служебные колонки: id, dt, target, w;
    - считаем долю пропусков и выкидываем признаки с missing_share > missing_threshold;
    - помечаем income-related признаки (по описанию);
    - по флагу drop_income_related можно их выкинуть из финального набора.

    На выходе:
    - features_all
    - features_dropped_missing
    - features_income_related
    - features_final
    """
    all_cols = list(train_df.columns)
    service_cols = {"id", "dt", "target", "w"}
    feature_cols = [c for c in all_cols if c not in service_cols]

    # Доля пропусков
    missing_share = train_df[feature_cols].isna().mean()

    # Income-related по описанию
    income_desc_df = detect_income_related_features(desc_df)
    income_related = set(income_desc_df["признак"].tolist())

    dropped_missing = set(missing_share[missing_share > missing_threshold].index.tolist())

    features_all = feature_cols
    features_income_related = [c for c in feature_cols if c in income_related]
    features_dropped_missing = [c for c in feature_cols if c in dropped_missing]

    # Кандидаты — все, кроме очень пустых
    features_candidate = [c for c in feature_cols if c not in dropped_missing]

    # В первой версии не выкидываем income-related, но оставляем флаг drop_income_related на будущее
    if drop_income_related:
        features_final = [c for c in features_candidate if c not in income_related]
    else:
        features_final = features_candidate

    return {
        "features_all": features_all,
        "features_dropped_missing": features_dropped_missing,
        "features_income_related": features_income_related,
        "features_final": features_final,
    }


def save_clean_datasets(
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    feature_lists: Dict[str, List[str]],
) -> None:
    """
    Сохраняет очищенные train/test:
    - только признаки из features_final
    - плюс служебные колонки id, dt, target, w (если есть)
    """
    final_features = feature_lists["features_final"]

    service_cols = [c for c in ["id", "dt", "target", "w"] if c in train_df.columns]
    keep_cols_train = service_cols + final_features
    keep_cols_test = [c for c in ["id", "dt"] if c in test_df.columns] + final_features

    train_clean = train_df[keep_cols_train].copy()
    test_clean = test_df[keep_cols_test].copy()

    out_train_csv = DATA_DIR / "income_train_clean.csv"
    out_test_csv = DATA_DIR / "income_test_clean.csv"

    train_clean.to_csv(out_train_csv, index=False, sep=";", decimal=",")
    test_clean.to_csv(out_test_csv, index=False, sep=";", decimal=",")

    print(f"Saved cleaned train to: {out_train_csv}")
    print(f"Saved cleaned test to: {out_test_csv}")


def main() -> None:
    print("Загружаем описание признаков...")
    desc_df = load_feature_description()

    print("Загружаем train/test...")
    train_df = load_train()
    test_df = load_test()

    print("Строим список income-related признаков...")
    income_feats = detect_income_related_features(desc_df)
    income_feats_path = REPORTS_DIR / "income_related_features.csv"
    income_feats.to_csv(income_feats_path, index=False)
    print(f"Сохранён список income-related фич: {income_feats_path}")

    print("Считаем корреляции числовых фич с target...")
    corr_df = compute_numeric_correlations(train_df)
    corr_path = REPORTS_DIR / "numeric_correlations_with_target.csv"
    corr_df.to_csv(corr_path, index=False)
    print(f"Сохранены корреляции: {corr_path}")

    print("Формируем набор признаков для модели...")
    feature_lists = build_clean_feature_set(
        train_df=train_df,
        desc_df=desc_df,
        missing_threshold=0.95,
        drop_income_related=False,  # можно переключить на True для «жёсткой» борьбы с утечками
    )

    features_summary_path = REPORTS_DIR / "feature_lists_summary.json"
    pd.Series(feature_lists, index=list(feature_lists.keys())).to_json(features_summary_path)
    print(f"Сохранён summary по фичам: {features_summary_path}")

    print("Сохраняем очищенные датасеты...")
    save_clean_datasets(train_df, test_df, feature_lists)

    print("Готово: построены отчёты и очищенные файлы для обучения.")


if __name__ == "__main__":
    main()
