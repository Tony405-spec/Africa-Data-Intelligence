"""Base classes for the Africa Data Intelligence dataset catalog."""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class DatasetEntry:
    """Metadata describing a single dataset in the catalog.

    Attributes:
        name: Human-readable dataset name.
        source: Where the dataset comes from (URL, portal name).
        country: Primary country covered (ISO name).
        geographic_level: e.g. "national", "county", "city".
        temporal_coverage: Human-readable range, e.g. "2015-2023".
        license: SPDX identifier or descriptive licence string.
        update_frequency: e.g. "monthly", "annual", "irregular".
        variables: List of key column names.
        last_updated: Date the catalog entry was last updated.
        tags: Optional tags for filtering.
    """

    name: str
    source: str
    country: str
    geographic_level: str
    temporal_coverage: str
    license: str
    update_frequency: str
    variables: list[str] = field(default_factory=list)
    last_updated: Optional[date] = None
    tags: list[str] = field(default_factory=list)


class BaseCatalog:
    """In-memory catalog that stores and retrieves DatasetEntry objects."""

    def __init__(self) -> None:
        self._entries: dict[str, DatasetEntry] = {}

    def add(self, entry: DatasetEntry) -> None:
        """Add a dataset entry, keyed by its name.

        Raises:
            ValueError: If an entry with the same name already exists.
        """
        if entry.name in self._entries:
            raise ValueError(f"Dataset already exists: {entry.name}")
        self._entries[entry.name] = entry

    def get(self, name: str) -> DatasetEntry:
        """Return the entry with the given name.

        Raises:
            KeyError: If the dataset is not in the catalog.
        """
        if name not in self._entries:
            raise KeyError(f"Dataset not found: {name}")
        return self._entries[name]

    def all(self) -> list[DatasetEntry]:
        """Return all entries as a list."""
        return list(self._entries.values())

    def names(self) -> list[str]:
        """Return all dataset names."""
        return list(self._entries.keys())

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, name: str) -> bool:
        return name in self._entries
