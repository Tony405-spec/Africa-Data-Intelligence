"""Linear regression wrapper for the Africa Data Intelligence ML engine."""

from typing import Optional

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class LinearModel:
    """A thin wrapper around sklearn LinearRegression with metric helpers."""

    def __init__(self) -> None:
        self.model = LinearRegression()
        self._is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model on X and y."""
        self.model.fit(X, y)
        self._is_fitted = True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict on X.

        Raises:
            RuntimeError: If the model has not been fitted.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict")
        return self.model.predict(X)

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict[str, float]:
        """Return RMSE, MAE, and R² for predictions on X."""
        predictions = self.predict(X)
        return {
            "rmse": float(np.sqrt(mean_squared_error(y, predictions))),
            "mae": float(mean_absolute_error(y, predictions)),
            "r2": float(r2_score(y, predictions)),
        }

    def coefficients(self, feature_names: Optional[list[str]] = None) -> dict[str, float]:
        """Return coefficients mapped to feature names."""
        names = feature_names or [f"x{i}" for i in range(len(self.model.coef_))]
        return {name: float(coef) for name, coef in zip(names, self.model.coef_)}

    def intercept(self) -> float:
        """Return the fitted intercept."""
        return float(self.model.intercept_)
