# utils.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# -------------------------
# Load Dataset
# -------------------------
def load_data(path="data/kaggle.csv"):
    """Load dataset from CSV."""
    df = pd.read_csv(path)
    return df

# -------------------------
# Prepare Features & Target
# -------------------------
def prepare_data(df, features=None, target="mental_wellness_index_0_100"):
    """
    Split features and target.
    Default features include 7 daily-only columns.
    """
    if features is None:
        features = [
            "screen_time_hours",
            "work_screen_hours",
            "leisure_screen_hours",
            "sleep_hours",
            "sleep_quality_1_5",
            "stress_level_0_10",
            "productivity_0_100"
        ]
    X = df[features]
    y = df[target]
    return X, y, features

# -------------------------
# Train Random Forest Model
# -------------------------
def train_model(X, y, test_size=0.2, random_state=42, n_estimators=300):
    """
    Train Random Forest Regressor with provided features and target.
    Returns model + train/test splits + predictions.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    return model, X_train, X_test, y_train, y_test, y_pred

# -------------------------
# Calculate Model Metrics
# -------------------------
def calculate_metrics(y_test, y_pred, X_columns=None, model=None):
    """
    Return dict of R2, MAE, MAPE, SMAPE, feature importance.
    """
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    
    mask = y_test != 0
    mape = np.mean(np.abs((y_test[mask] - y_pred[mask]) / y_test[mask])) * 100
    smape = np.mean(2 * np.abs(y_test - y_pred) / (np.abs(y_test) + np.abs(y_pred))) * 100
    
    feat_imp_df = None
    if X_columns is not None and model is not None:
        feat_imp_df = pd.DataFrame({
            "Feature": X_columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

    return {
        "r2": r2,
        "mae": mae,
        "mape": mape,
        "smape": smape,
        "feat_imp_df": feat_imp_df
    }

# -------------------------
# Full Training Pipeline
# -------------------------
def train_pipeline(path="data/kaggle.csv", target="mental_wellness_index_0_100"):
    """
    Load dataset, prepare daily-only features, train model, and return metrics + model.
    """
    df = load_data(path)
    X, y, features = prepare_data(df, target=target)
    model, X_train, X_test, y_train, y_test, y_pred = train_model(X, y)
    metrics = calculate_metrics(y_test, y_pred, X_columns=features, model=model)
    return model, metrics, X_train, X_test, y_train, y_test, y_pred
