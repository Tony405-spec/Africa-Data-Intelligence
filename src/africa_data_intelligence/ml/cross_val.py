"""Cross-validation utilities for the Africa Data Intelligence ML engine."""

from typing import Any, Callable

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold


class CrossValidator:
    """Runs k-fold cross-validation for any callable model factory."""

    def __init__(self, n_splits: int = 5, random_state: int = 42) -> None:
        if n_splits < 2:
            raise ValueError("n_splits must be >= 2")
        self.n_splits = n_splits
        self.random_state = random_state

    def run(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        model_factory: Callable[[], Any],
        metric: Callable[[Any, Any], float],
    ) -> dict[str, Any]:
        """Run k-fold CV and return per-fold and aggregate metrics."""
        kf = KFold(
            n_splits=self.n_splits,
            shuffle=True,
            random_state=self.random_state,
        )
        fold_scores: list[float] = []
        for train_idx, test_idx in kf.split(X):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

            model = model_factory()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            fold_scores.append(float(metric(y_test, preds)))

        scores = np.array(fold_scores)
        return {
            "fold_scores": fold_scores,
            "mean": float(scores.mean()),
            "std": float(scores.std()),
            "min": float(scores.min()),
            "max": float(scores.max()),
        }
