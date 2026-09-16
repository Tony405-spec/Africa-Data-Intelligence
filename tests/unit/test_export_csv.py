"""Unit tests for CatalogCSVExporter."""

import csv

from africa_data_intelligence.catalog.base import DatasetEntry
from africa_data_intelligence.catalog.export_csv import CatalogCSVExporter


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
        tags=["population"],
    )


def test_to_string_has_header():
    exporter = CatalogCSVExporter()
    text = exporter.to_string([_entry()])
    header, _, _ = text.partition("\n")
    assert "name" in header
    assert "country" in header


def test_to_string_row_count():
    exporter = CatalogCSVExporter()
    text = exporter.to_string([_entry("A"), _entry("B")])
    lines = text.splitlines()
    assert len(lines) == 3  # header + 2 rows


def test_variables_joined_with_semicolon():
    exporter = CatalogCSVExporter()
    text = exporter.to_string([_entry()])
    assert "year;population" in text


def test_to_file_writes_csv(tmp_path):
    exporter = CatalogCSVExporter()
    target = tmp_path / "catalog.csv"
    result = exporter.to_file([_entry()], target)
    assert result.exists()

    with target.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 1
    assert rows[0]["country"] == "Kenya"

