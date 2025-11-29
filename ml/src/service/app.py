import sys
import json
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from catboost import CatBoostRegressor, Pool

# --- НАСТРОЙКИ ---
current_file = Path(__file__).resolve()
project_root = current_file.parents[3]
sys.path.append(str(project_root))

try:
    from ml.src.features.preprocess import prepare_features
    from ml.src.features.add_engineered_features import add_fe_block
except ImportError as e:
    print(f"IMPORT ERROR: {e}")

MODEL_NAME = "catboost_full_fe"
MODELS_DIR = project_root / "ml" / "models"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

model: CatBoostRegressor = None
meta: dict = None
feature_cols: List[str] = []
fit_stats: dict = None
model_cat_features: List[str] = []  # Точный список категорий из модели


@app.on_event("startup")
def load_model():
    global model, meta, feature_cols, fit_stats, model_cat_features

    model_path = MODELS_DIR / f"{MODEL_NAME}.cbm"
    meta_path = MODELS_DIR / f"{MODEL_NAME}_meta.json"

    logger.info(f"Loading model from {model_path}...")
    if not model_path.exists():
        logger.error("Model file not found!")
        return

    model = CatBoostRegressor()
    model.load_model(str(model_path))

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    feature_cols = meta["features"]
    fit_stats = meta["fit_stats"]

    # ВАЖНО: Получаем индексы категориальных фичей прямо из модели
    # и мапим их на имена колонок
    cat_indices = model.get_cat_feature_indices()
    model_cat_features = [feature_cols[i] for i in cat_indices]

    logger.info(f"Model loaded! Found {len(model_cat_features)} categorical features.")


class PredictRequest(BaseModel):
    client_id: str
    features: Dict[str, Any]


def fill_missing_columns_optimized(df: pd.DataFrame, target_cols: List[str]) -> pd.DataFrame:
    missing = [c for c in target_cols if c not in df.columns]
    if missing:
        missing_df = pd.DataFrame(np.nan, index=df.index, columns=missing)
        df = pd.concat([df, missing_df], axis=1)
    return df


@app.post("/predict")
def predict(request: PredictRequest):
    try:
        df = pd.DataFrame([request.features])
        df["id"] = request.client_id

        # Список сырых колонок, которые нужны для FE (на всякий случай)
        raw_cols_needed = [
            'acard', 'accountsalary_out_flag', 'age', 'gender', 'incomeValue',
            'salary_6to12m_avg', 'hdb_bki_total_max_limit', 'hdb_bki_total_products',
            'avg_cur_cr_turn', 'avg_cur_db_turn', 'adminarea', 'city_smart_name',
            'per_capita_income_rur_amt', 'salary_median_in_gex_r1',
            'dp_ils_avg_salary_3y', 'profit_income_out_rur_amt_l2m',
            'profit_income_out_rur_amt_12m', 'profit_income_out_rur_amt_9m'
        ]
        df = fill_missing_columns_optimized(df, raw_cols_needed)

        # FE
        try:
            df = add_fe_block(df)
        except Exception as e:
            logger.warning(f"FE failed: {e}")

        # Дополняем все фичи перед препроцессингом
        df = fill_missing_columns_optimized(df, feature_cols)

        # Preprocessing
        # prepare_features вернет X в правильном порядке колонок
        X, _, _, _, _ = prepare_features(
            df,
            feature_cols=feature_cols,
            fit_stats=fit_stats
        )

        # --- ФИНАЛЬНЫЙ ФИКС ТИПОВ ---
        # Проходимся по тем колонкам, которые МОДЕЛЬ считает категориальными
        for col in model_cat_features:
            if col in X.columns:
                # Превращаем всё в строки.
                # 0.0 -> "0.0", NaN -> "nan" -> "missing"
                X[col] = X[col].astype(str)
                X.loc[X[col] == 'nan', col] = 'missing'
                X.loc[X[col] == 'None', col] = 'missing'

        # Predict
        y_pred = model.predict(X)
        prediction_value = y_pred[0]

        if meta.get("target_transform") == "log1p":
            prediction_value = np.expm1(prediction_value)

        # SHAP
        top_factors = []
        try:
            # Для SHAP тоже нужно убедиться, что типы правильные
            shap_pool = Pool(data=X, cat_features=model_cat_features)
            shap_values = model.get_feature_importance(data=shap_pool, type='ShapValues')
            features_shap = shap_values[0][:-1]

            contributions = []
            for name, value in zip(feature_cols, features_shap):
                if abs(value) > 0.01:
                    contributions.append({
                        "name": str(name),
                        "value": float(round(value, 2)),
                        "desc": f"Фактор: {name}"
                    })

            contributions.sort(key=lambda x: abs(x["value"]), reverse=True)
            top_factors = contributions[:20]
        except Exception as shap_e:
            logger.warning(f"SHAP failed: {shap_e}")

        return {
            "client_id": request.client_id,
            "predicted_income": float(round(prediction_value, 2)),
            "model_version": MODEL_NAME,
            "shap_values": top_factors
        }

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))