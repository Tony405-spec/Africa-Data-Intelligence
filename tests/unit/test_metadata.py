"""Unit tests for MetadataValidator."""

from datetime import date

import pytest

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.metadata import MetadataValidator


def _entry(**overrides) -> DatasetEntry:
    defaults = dict(
        name="Kenya Population",
        source="https://example.com/data",
        country="Kenya",
        geographic_level="national",
        temporal_coverage="2015-2023",
        license="CC-BY-4.0",
        update_frequency="annual",
        variables=["year", "population"],
    )
    defaults.update(overrides)
    return DatasetEntry(**defaults)


def test_valid_entry_passes():
    MetadataValidator().validate(_entry())


def test_empty_field_raises():
    with pytest.raises(ValueError, match="must not be empty"):
        MetadataValidator().validate(_entry(name=""))


def test_non_url_source_raises():
    with pytest.raises(ValueError, match="must be a URL"):
        MetadataValidator().validate(_entry(source="ftp://example.com"))


def test_variables_must_be_list():
    with pytest.raises(ValueError, match="must be a list"):
        MetadataValidator().validate(_entry(variables="year,population"))


def test_validate_many_returns_count():
    entries = [_entry(name=f"DS{i}") for i in range(4)]
    assert MetadataValidator().validate_many(entries) == 4


def test_old_last_updated_raises():
    with pytest.raises(ValueError, match="1990 or later"):
        MetadataValidator().validate(_entry(last_updated=date(1980, 1, 1)))
