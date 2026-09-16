"""Unit tests for ModelPersister."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.linear import LinearModel
from africa_data_intelligence.ml.persistence import ModelPersister


def _trained_model() -> LinearModel:
    X = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0]})
    y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
    model = LinearModel()
    model.fit(X, y)
    return model


def test_save_and_load_roundtrip(tmp_path):
    persister = ModelPersister(tmp_path)
    model = _trained_model()
    persister.save(model, "linear_v1")

    loaded = persister.load("linear_v1")
    X = pd.DataFrame({"x": [6.0, 7.0]})
    np.testing.assert_allclose(loaded.predict(X), model.predict(X))


def test_save_empty_name_raises(tmp_path):
    persister = ModelPersister(tmp_path)
    with pytest.raises(ValueError, match="must not be empty"):
        persister.save(_trained_model(), "")


def test_load_missing_raises(tmp_path):
    persister = ModelPersister(tmp_path)
    with pytest.raises(FileNotFoundError, match="Model not found"):
        persister.load("nope")


def test_metadata_saved_and_loaded(tmp_path):
    persister = ModelPersister(tmp_path)
    persister.save(_trained_model(), "linear_v1", metadata={"rmse": 0.1, "notes": "baseline"})

    meta = persister.load_metadata("linear_v1")
    assert meta["rmse"] == 0.1
    assert meta["notes"] == "baseline"


def test_list_and_exists(tmp_path):
    persister = ModelPersister(tmp_path)
    persister.save(_trained_model(), "a")
    persister.save(_trained_model(), "b")

    assert persister.list_models() == ["a", "b"]
    assert persister.exists("a") is True
    assert persister.exists("z") is False


def test_delete_removes_model(tmp_path):
    persister = ModelPersister(tmp_path)
    persister.save(_trained_model(), "temp", metadata={"v": 1})
    persister.delete("temp")

    assert persister.exists("temp") is False
    assert persister.load_metadata("temp") == {}
