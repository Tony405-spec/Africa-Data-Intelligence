"""Unit tests for the BaseCatalog and DatasetEntry."""

import pytest

from africa_data_intelligence.catalog.base import BaseCatalog, DatasetEntry


def _entry(name: str = "Kenya Population") -> DatasetEntry:
    return DatasetEntry(
        name=name,
        source="https://example.com",
        country="Kenya",
        geographic_level="national",
        temporal_coverage="2015-2023",
        license="CC-BY-4.0",
        update_frequency="annual",
        variables=["year", "population"],
    )


def test_add_and_get_entry():
    catalog = BaseCatalog()
    catalog.add(_entry())
    assert catalog.get("Kenya Population").country == "Kenya"


def test_add_duplicate_raises():
    catalog = BaseCatalog()
    catalog.add(_entry())
    with pytest.raises(ValueError, match="Dataset already exists"):
        catalog.add(_entry())


def test_get_missing_raises():
    catalog = BaseCatalog()
    with pytest.raises(KeyError, match="Dataset not found"):
        catalog.get("Nope")


def test_all_and_names():
    catalog = BaseCatalog()
    catalog.add(_entry("A"))
    catalog.add(_entry("B"))
    assert catalog.names() == ["A", "B"]
    assert len(catalog.all()) == 2


def test_len_and_contains():
    catalog = BaseCatalog()
    catalog.add(_entry("Kenya"))
    assert len(catalog) == 1
    assert "Kenya" in catalog
    assert "Uganda" not in catalog
