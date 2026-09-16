"""Unit tests for the Kenyan catalog entries."""

from africa_data_intelligence.catalog.kenya import KENYA_DATASETS, get_kenya_datasets
from africa_data_intelligence.catalog.metadata import MetadataValidator


def test_kenya_datasets_not_empty():
    assert len(KENYA_DATASETS) >= 3


def test_get_kenya_datasets_returns_copy():
    a = get_kenya_datasets()
    b = get_kenya_datasets()
    assert a == b
    assert a is not b


def test_all_entries_valid():
    validator = MetadataValidator()
    for entry in KENYA_DATASETS:
        validator.validate(entry)


def test_entries_have_country_kenya():
    for entry in KENYA_DATASETS:
        assert entry.country == "Kenya"


def test_entries_have_expected_tags():
    tags = {tag for e in KENYA_DATASETS for tag in e.tags}
    assert "population" in tags or "demographics" in tags
    assert any("climate" in t or "weather" in t for t in tags)
