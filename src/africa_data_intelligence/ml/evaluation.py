"""Model evaluation utilities for the Africa Data Intelligence ML engine."""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)


class RegressionEvaluator:
    """Computes regression metrics for a set of predictions."""

    def evaluate(self, y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
        """Return RMSE, MAE, R², and MAPE."""
        y_true_arr = np.asarray(y_true, dtype=float)
        y_pred_arr = np.asarray(y_pred, dtype=float)

        rmse = float(np.sqrt(mean_squared_error(y_true_arr, y_pred_arr)))
        mae = float(mean_absolute_error(y_true_arr, y_pred_arr))
        r2 = float(r2_score(y_true_arr, y_pred_arr))

        nonzero = y_true_arr != 0
        if nonzero.any():
            mape = float(
                np.mean(np.abs((y_true_arr[nonzero] - y_pred_arr[nonzero]) / y_true_arr[nonzero])) * 100
            )
        else:
            mape = 0.0

        return {"rmse": rmse, "mae": mae, "r2": r2, "mape": mape}

    def to_dataframe(self, y_true: pd.Series, y_pred: np.ndarray) -> pd.DataFrame:
        """Return the evaluation metrics as a tidy DataFrame."""
        return pd.DataFrame(
            list(self.evaluate(y_true, y_pred).items()),
            columns=["metric", "value"],
        )


class ClassificationEvaluator:
    """Computes classification metrics for a set of predictions."""

    def evaluate(self, y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
        """Return accuracy, precision, recall, and F1."""
        return {
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "precision": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
            "recall": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
            "f1": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
        }
