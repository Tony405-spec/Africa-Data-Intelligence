"""Smoke tests for the dashboard modules (no streamlit runtime required)."""

import inspect

from dashboard.pages import countries, explorer, home


def test_home_exposes_render():
    assert callable(home.render)


def test_explorer_exposes_render():
    assert callable(explorer.render)


def test_countries_exposes_render():
    assert callable(countries.render)


def test_countries_dataset_shape():
    assert isinstance(countries._COUNTRIES, list)
    assert all("code" in c and "name" in c for c in countries._COUNTRIES)


def test_explorer_dataset_shape():
    assert isinstance(explorer._DATASETS, list)
    assert all("name" in d and "country" in d for d in explorer._DATASETS)


def test_render_functions_take_no_args():
    for module in (home, explorer, countries):
        sig = inspect.signature(module.render)
        assert len(sig.parameters) == 0

