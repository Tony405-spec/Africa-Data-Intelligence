"""Filtering utilities for the Africa Data Intelligence dataset catalog."""

from typing import Optional

from africa_data_intelligence.catalog.base import DatasetEntry


class CatalogFilter:
    """Filters a list of DatasetEntry objects by structured criteria."""

    def __init__(self, entries: list[DatasetEntry]) -> None:
        self.entries = entries

    def by_country(self, country: str) -> list[DatasetEntry]:
        """Return entries for a country (case-insensitive)."""
        needle = country.strip().lower()
        return [e for e in self.entries if e.country.lower() == needle]

    def by_geographic_level(self, level: str) -> list[DatasetEntry]:
        """Return entries for a geographic level (case-insensitive)."""
        needle = level.strip().lower()
        return [e for e in self.entries if e.geographic_level.lower() == needle]

    def by_update_frequency(self, frequency: str) -> list[DatasetEntry]:
        """Return entries for an update frequency (case-insensitive)."""
        needle = frequency.strip().lower()
        return [e for e in self.entries if e.update_frequency.lower() == needle]

    def combine(
        self,
        country: Optional[str] = None,
        geographic_level: Optional[str] = None,
        update_frequency: Optional[str] = None,
    ) -> list[DatasetEntry]:
        """Return entries matching all provided criteria simultaneously."""
        results = list(self.entries)
        if country:
            results = [e for e in results if e.country.lower() == country.lower()]
        if geographic_level:
            results = [
                e
                for e in results
                if e.geographic_level.lower() == geographic_level.lower()
            ]
        if update_frequency:
            results = [
                e
                for e in results
                if e.update_frequency.lower() == update_frequency.lower()
            ]
        return results
