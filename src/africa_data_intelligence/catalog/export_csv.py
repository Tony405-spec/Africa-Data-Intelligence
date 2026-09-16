"""CSV export for the Africa Data Intelligence dataset catalog."""

import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from africa_data_intelligence.catalog.base import DatasetEntry


class CatalogCSVExporter:
    """Serializes DatasetEntry objects to CSV files or strings."""

    FIELDS = (
        "name",
        "source",
        "country",
        "geographic_level",
        "temporal_coverage",
        "license",
        "update_frequency",
        "variables",
        "last_updated",
        "tags",
    )

    def to_string(self, entries: Iterable[DatasetEntry]) -> str:
        """Return entries serialized as a CSV string."""
        lines = [",".join(self.FIELDS)]
        for entry in entries:
            row = self._row(entry)
            lines.append(",".join(row))
        return "\n".join(lines)

    def to_file(self, entries: Iterable[DatasetEntry], path: str | Path) -> Path:
        """Write entries to a CSV file and return the path."""
        target = Path(path)
        with target.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.FIELDS)
            for entry in entries:
                writer.writerow(self._row(entry))
        return target

    def _row(self, entry: DatasetEntry) -> list[str]:
        data = asdict(entry)
        row: list[str] = []
        for field in self.FIELDS:
            value = data.get(field)
            if isinstance(value, list):
                value = ";".join(str(v) for v in value)
            elif value is None:
                value = ""
            else:
                value = str(value)
            row.append(value.replace(",", ";"))
        return row

