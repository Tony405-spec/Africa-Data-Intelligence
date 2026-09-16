"""Unit tests for the Nigerian catalog entries."""

from africa_data_intelligence.catalog.metadata import MetadataValidator
from africa_data_intelligence.catalog.nigeria import (
    NIGERIA_DATASETS,
    get_nigeria_datasets,
)


def test_nigeria_datasets_not_empty():
    assert len(NIGERIA_DATASETS) >= 3


def test_get_nigeria_datasets_returns_copy():
    a = get_nigeria_datasets()
    b = get_nigeria_datasets()
    assert a == b
    assert a is not b


def test_all_entries_valid():
    validator = MetadataValidator()
    for entry in NIGERIA_DATASETS:
        validator.validate(entry)


def test_entries_have_country_nigeria():
    for entry in NIGERIA_DATASETS:
        assert entry.country == "Nigeria"


def test_entries_cover_expected_domains():
    tags = {tag for e in NIGERIA_DATASETS for tag in e.tags}
    assert "population" in tags
    assert any(t in tags for t in ("energy", "oil"))

