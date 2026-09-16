"""Logistic regression wrapper for the Africa Data Intelligence ML engine."""

from typing import Optional

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class LogisticModel:
    """A thin wrapper around sklearn LogisticRegression with metric helpers."""

    def __init__(self, max_iter: int = 1000, random_state: int = 42) -> None:
        self.model = LogisticRegression(max_iter=max_iter, random_state=random_state)
        self._is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        """Fit the model on X and y."""
        self.model.fit(X, y)
        self._is_fitted = True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Return predicted class labels.

        Raises:
            RuntimeError: If the model has not been fitted.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict")
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Return class probabilities for X."""
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict_proba")
        return self.model.predict_proba(X)

    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> dict[str, float]:
        """Return accuracy, precision, recall, and F1."""
        preds = self.predict(X)
        return {
            "accuracy": float(accuracy_score(y, preds)),
            "precision": float(precision_score(y, preds, average="weighted", zero_division=0)),
            "recall": float(recall_score(y, preds, average="weighted", zero_division=0)),
            "f1": float(f1_score(y, preds, average="weighted", zero_division=0)),
        }

    def coefficients(self, feature_names: Optional[list[str]] = None) -> dict[str, float]:
        """Return class coefficients mapped to feature names."""
        coefs = self.model.coef_
        if coefs.ndim > 1:
            coefs = coefs[0]
        names = feature_names or [f"x{i}" for i in range(len(coefs))]
        return {name: float(c) for name, c in zip(names, coefs)}
