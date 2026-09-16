"""XGBoost wrapper for the Africa Data Intelligence ML engine."""

from typing import Optional

import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class XGBoostModel:
    """A wrapper around XGBRegressor with metric helpers."""

    def __init__(
        self,
        n_estimators: int = 200,
        learning_rate: float = 0.1,
        max_depth: int = 6,
        random_state: int = 42,
    ) -> None:
        self.model = XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
            verbosity=0,
        )
        self._is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model on X and y."""
        self.model.fit(X, y)
        self._is_fitted = True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Return predictions on X.

        Raises:
            RuntimeError: If the model has not been fitted.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict")
        return self.model.predict(X)

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict[str, float]:
        """Return RMSE, MAE, and R² on X."""
        predictions = self.predict(X)
        return {
            "rmse": float(np.sqrt(mean_squared_error(y, predictions))),
            "mae": float(mean_absolute_error(y, predictions)),
            "r2": float(r2_score(y, predictions)),
        }

    def feature_importance(self) -> dict[str, float]:
        """Return feature importances indexed by column name."""
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before requesting feature importance")
        names = getattr(self.model, "feature_names_in_", None)
        if names is None:
            names = [f"x{i}" for i in range(len(self.model.feature_importances_))]
        return {name: float(score) for name, score in zip(names, self.model.feature_importances_)}
