"""Unit tests for CatalogRegistry."""

import pytest

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.registry import CatalogRegistry


def _entry(name: str, country: str = "Kenya", tags: list[str] | None = None) -> DatasetEntry:
    return DatasetEntry(
        name=name,
        source="https://example.com",
        country=country,
        geographic_level="national",
        temporal_coverage="2020-2023",
        license="CC-BY-4.0",
        update_frequency="annual",
        tags=tags or [],
    )


def test_register_and_len():
    reg = CatalogRegistry()
    reg.register(_entry("A"))
    reg.register(_entry("B"))
    assert len(reg) == 2


def test_register_many_returns_count():
    reg = CatalogRegistry()
    count = reg.register_many([_entry("A"), _entry("B"), _entry("C")])
    assert count == 3


def test_register_many_duplicate_raises():
    reg = CatalogRegistry()
    reg.register(_entry("A"))
    with pytest.raises(ValueError, match="Dataset already exists"):
        reg.register_many([_entry("B"), _entry("A")])


def test_find_by_country_case_insensitive():
    reg = CatalogRegistry()
    reg.register(_entry("A", country="Kenya"))
    reg.register(_entry("B", country="kenya"))
    reg.register(_entry("C", country="Uganda"))
    assert len(reg.find_by_country("Kenya")) == 2


def test_find_by_tag():
    reg = CatalogRegistry()
    reg.register(_entry("A", tags=["population", "census"]))
    reg.register(_entry("B", tags=["climate"]))
    assert len(reg.find_by_tag("population")) == 1


def test_all_and_names():
    reg = CatalogRegistry()
    reg.register(_entry("A"))
    reg.register(_entry("B"))
    assert reg.names() == ["A", "B"]
    assert len(reg.all()) == 2
