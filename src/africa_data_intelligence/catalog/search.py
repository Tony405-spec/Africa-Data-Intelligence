"""Search utilities for the Africa Data Intelligence dataset catalog."""

from africa_data_intelligence.catalog.base import DatasetEntry


class CatalogSearch:
    """Searches a list of DatasetEntry objects by free-text query."""

    def __init__(self, entries: list[DatasetEntry]) -> None:
        self.entries = entries

    def search(self, query: str) -> list[DatasetEntry]:
        """Return entries whose name, country, or tags contain the query.

        Raises:
            ValueError: If the query is empty.
        """
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        needle = query.strip().lower()
        results: list[DatasetEntry] = []
        for entry in self.entries:
            haystack = " ".join(
                [entry.name, entry.country, entry.geographic_level, *entry.tags]
            ).lower()
            if needle in haystack:
                results.append(entry)
        return results

    def search_many(self, queries: list[str]) -> dict[str, list[DatasetEntry]]:
        """Return a mapping of query -> matching entries."""
        return {q: self.search(q) for q in queries}
