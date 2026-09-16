"""Unit tests for CatalogSearch."""

import pytest

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.search import CatalogSearch


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


def test_search_by_name():
    entries = [_entry("Kenya Population"), _entry("Nigeria Oil")]
    results = CatalogSearch(entries).search("population")
    assert len(results) == 1
    assert results[0].name == "Kenya Population"


def test_search_by_country():
    entries = [_entry("A", "Kenya"), _entry("B", "Nigeria")]
    results = CatalogSearch(entries).search("kenya")
    assert len(results) == 1


def test_search_by_tag():
    entries = [_entry("A", tags=["climate"]), _entry("B", tags=["economy"])]
    results = CatalogSearch(entries).search("climate")
    assert len(results) == 1


def test_search_empty_query_raises():
    with pytest.raises(ValueError, match="must not be empty"):
        CatalogSearch([]).search("   ")


def test_search_case_insensitive():
    entries = [_entry("Kenya Rainfall")]
    assert len(CatalogSearch(entries).search("RAINFALL")) == 1


def test_search_many_returns_dict():
    entries = [_entry("Kenya Population"), _entry("Nigeria Oil")]
    results = CatalogSearch(entries).search_many(["kenya", "oil"])
    assert "kenya" in results
    assert "oil" in results
    assert len(results["kenya"]) == 1
