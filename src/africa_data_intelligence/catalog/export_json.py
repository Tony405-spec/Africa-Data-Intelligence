"""JSON export for the Africa Data Intelligence dataset catalog."""

import json
from dataclasses import asdict
from pathlib import Path

from africa_data_intelligence.catalog.base import DatasetEntry


class CatalogJSONExporter:
    """Serializes DatasetEntry objects to JSON files or strings."""

    def to_string(self, entries: list[DatasetEntry], indent: int = 2) -> str:
        """Return entries serialized as a JSON string."""
        payload = [self._serialize(e) for e in entries]
        return json.dumps(payload, indent=indent, default=str)

    def to_file(self, entries: list[DatasetEntry], path: str | Path) -> Path:
        """Write entries to a JSON file and return the path."""
        target = Path(path)
        target.write_text(self.to_string(entries), encoding="utf-8")
        return target

    def _serialize(self, entry: DatasetEntry) -> dict:
        data = asdict(entry)
        if data.get("last_updated") is not None:
            data["last_updated"] = str(data["last_updated"])
        return data

