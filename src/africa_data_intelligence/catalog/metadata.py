"""Dataset metadata validation for the catalog."""

from africa_data_intelligence.catalog.base import DatasetEntry


_REQUIRED_FIELDS = (
    "name",
    "source",
    "country",
    "geographic_level",
    "temporal_coverage",
    "license",
    "update_frequency",
)


class MetadataValidator:
    """Validates DatasetEntry objects against required metadata rules."""

    def validate(self, entry: DatasetEntry) -> None:
        """Validate a single DatasetEntry.

        Raises:
            ValueError: If any required field is empty or malformed.
        """
        for field in _REQUIRED_FIELDS:
            value = getattr(entry, field, None)
            if not value or not str(value).strip():
                raise ValueError(f"Field '{field}' must not be empty")

        if not entry.source.startswith(("http://", "https://")):
            raise ValueError(f"Source must be a URL: {entry.source}")

        if not isinstance(entry.variables, list):
            raise ValueError("'variables' must be a list")

        if entry.last_updated is not None and entry.last_updated.year < 1990:
            raise ValueError("last_updated must be 1990 or later")

    def validate_many(self, entries: list[DatasetEntry]) -> int:
        """Validate many entries; returns the number that passed."""
        for entry in entries:
            self.validate(entry)
        return len(entries)
