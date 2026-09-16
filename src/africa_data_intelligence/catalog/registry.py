"""Global registry for datasets across the catalog."""

from typing import Iterable

from africa_data_intelligence.catalog.base import BaseCatalog, DatasetEntry


class CatalogRegistry:
    """A thin manager around BaseCatalog that supports bulk loading."""

    def __init__(self) -> None:
        self._catalog = BaseCatalog()

    def register(self, entry: DatasetEntry) -> None:
        """Add a single entry to the registry."""
        self._catalog.add(entry)

    def register_many(self, entries: Iterable[DatasetEntry]) -> int:
        """Add many entries; returns the number successfully added.

        Raises:
            ValueError: If any entry has a duplicate name.
        """
        count = 0
        for entry in entries:
            self._catalog.add(entry)
            count += 1
        return count

    def find_by_country(self, country: str) -> list[DatasetEntry]:
        """Return all entries for a given country (case-insensitive)."""
        country_lower = country.lower()
        return [e for e in self._catalog.all() if e.country.lower() == country_lower]

    def find_by_tag(self, tag: str) -> list[DatasetEntry]:
        """Return all entries containing the given tag (case-insensitive)."""
        tag_lower = tag.lower()
        return [
            e for e in self._catalog.all() if tag_lower in [t.lower() for t in e.tags]
        ]

    def all(self) -> list[DatasetEntry]:
        """Return every entry in the registry."""
        return self._catalog.all()

    def names(self) -> list[str]:
        """Return all dataset names."""
        return self._catalog.names()

    def __len__(self) -> int:
        return len(self._catalog)
