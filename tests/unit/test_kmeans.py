"""Unit tests for KMeansModel."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.kmeans import KMeansModel


def _data() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    group_a = rng.normal(0, 0.3, size=(30, 2))
    group_b = rng.normal(5, 0.3, size=(30, 2))
    return pd.DataFrame(np.vstack([group_a, group_b]), columns=["x", "y"])


def test_fit_predict_labels():
    X = _data()
    model = KMeansModel(n_clusters=2)
    model.fit(X)
    labels = model.predict(X)
    assert len(np.unique(labels)) == 2


def test_predict_before_fit_raises():
    X = _data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        KMeansModel().predict(X)


def test_invalid_n_clusters():
    with pytest.raises(ValueError, match="n_clusters"):
        KMeansModel(n_clusters=0)


def test_cluster_centers_shape():
    X = _data()
    model = KMeansModel(n_clusters=2)
    model.fit(X)
    centers = model.cluster_centers()
    assert centers.shape == (2, 2)


def test_inertia_positive():
    X = _data()
    model = KMeansModel(n_clusters=2)
    model.fit(X)
    assert model.inertia() > 0.0


def test_label_counts_total():
    X = _data()
    model = KMeansModel(n_clusters=2)
    model.fit(X)
    counts = model.label_counts(X)
    assert sum(counts.values()) == len(X)


def test_centers_before_fit_raises():
    with pytest.raises(RuntimeError):
        KMeansModel().cluster_centers()
