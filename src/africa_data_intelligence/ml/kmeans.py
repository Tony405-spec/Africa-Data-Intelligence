"""KMeans clustering wrapper for the Africa Data Intelligence ML engine."""

from typing import Optional

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans


class KMeansModel:
    """A wrapper around sklearn KMeans with helper utilities."""

    def __init__(
        self,
        n_clusters: int = 3,
        random_state: int = 42,
        n_init: int = 10,
    ) -> None:
        if n_clusters < 1:
            raise ValueError("n_clusters must be >= 1")
        self.model = KMeans(
            n_clusters=n_clusters,
            random_state=random_state,
            n_init=n_init,
        )
        self._is_fitted = False

    def fit(self, X: pd.DataFrame) -> None:
        """Fit the clustering model on X."""
        self.model.fit(X)
        self._is_fitted = True

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Return cluster labels for X.

        Raises:
            RuntimeError: If the model has not been fitted.
        """
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before calling predict")
        return self.model.predict(X)

    def cluster_centers(self) -> np.ndarray:
        """Return the cluster centers."""
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before requesting centers")
        return self.model.cluster_centers_

    def inertia(self) -> float:
        """Return the within-cluster sum of squares."""
        if not self._is_fitted:
            raise RuntimeError("Model must be fitted before requesting inertia")
        return float(self.model.inertia_)

    def label_counts(self, X: pd.DataFrame) -> dict[int, int]:
        """Return cluster label -> count."""
        labels = self.predict(X)
        unique, counts = np.unique(labels, return_counts=True)
        return {int(u): int(c) for u, c in zip(unique, counts)}

