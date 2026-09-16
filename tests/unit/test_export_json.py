"""Unit tests for CatalogJSONExporter."""

import json

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.export_json import CatalogJSONExporter


def _entry(name: str = "Kenya Population") -> DatasetEntry:
    return DatasetEntry(
        name=name,
        source="https://example.com",
        country="Kenya",
        geographic_level="national",
        temporal_coverage="2020-2023",
        license="CC-BY-4.0",
        update_frequency="annual",
        variables=["year", "population"],
    )


def test_to_string_returns_valid_json():
    exporter = CatalogJSONExporter()
    payload = exporter.to_string([_entry()])
    parsed = json.loads(payload)
    assert isinstance(parsed, list)
    assert parsed[0]["name"] == "Kenya Population"


def test_to_string_handles_multiple_entries():
    exporter = CatalogJSONExporter()
    payload = exporter.to_string([_entry("A"), _entry("B")])
    parsed = json.loads(payload)
    assert len(parsed) == 2


def test_to_file_writes_json(tmp_path):
    exporter = CatalogJSONExporter()
    target = tmp_path / "catalog.json"
    result = exporter.to_file([_entry()], target)
    assert result.exists()
    data = json.loads(target.read_text())
    assert data[0]["country"] == "Kenya"


def test_to_string_includes_tags():
    exporter = CatalogJSONExporter()
    payload = exporter.to_string([_entry()])
    assert "tags" in payload

