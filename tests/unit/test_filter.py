"""Unit tests for CatalogFilter."""

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.filter import CatalogFilter


def _entry(
    name: str,
    country: str = "Kenya",
    level: str = "national",
    freq: str = "annual",
) -> DatasetEntry:
    return DatasetEntry(
        name=name,
        source="https://example.com",
        country=country,
        geographic_level=level,
        temporal_coverage="2020-2023",
        license="CC-BY-4.0",
        update_frequency=freq,
    )


def test_by_country():
    entries = [_entry("A", "Kenya"), _entry("B", "Nigeria")]
    assert len(CatalogFilter(entries).by_country("Kenya")) == 1


def test_by_geographic_level():
    entries = [_entry("A", level="county"), _entry("B", level="national")]
    assert len(CatalogFilter(entries).by_geographic_level("county")) == 1


def test_by_update_frequency():
    entries = [_entry("A", freq="annual"), _entry("B", freq="daily")]
    assert len(CatalogFilter(entries).by_update_frequency("daily")) == 1


def test_combine_returns_only_matching_all():
    entries = [
        _entry("A", "Kenya", "county", "annual"),
        _entry("B", "Kenya", "national", "annual"),
        _entry("C", "Nigeria", "county", "annual"),
    ]
    results = CatalogFilter(entries).combine(
        country="Kenya", geographic_level="county"
    )
    assert len(results) == 1
    assert results[0].name == "A"


def test_combine_with_no_filters_returns_all():
    entries = [_entry("A"), _entry("B")]
    assert len(CatalogFilter(entries).combine()) == 2


def test_combine_all_three_filters():
    entries = [
        _entry("A", "Kenya", "county", "daily"),
        _entry("B", "Kenya", "county", "annual"),
    ]
    results = CatalogFilter(entries).combine(
        country="Kenya", geographic_level="county", update_frequency="daily"
    )
    assert len(results) == 1

