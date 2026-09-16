"""Model persistence utilities for the Africa Data Intelligence ML engine."""

import json
from pathlib import Path
from typing import Any

import joblib


class ModelPersister:
    """Saves and loads trained models plus small metadata sidecars."""

    def __init__(self, base_dir: str | Path = "models") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, model: Any, name: str, metadata: dict | None = None) -> Path:
        """Serialize the model (and optional metadata) to disk.

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Model name must not be empty")

        model_path = self.base_dir / f"{name}.joblib"
        joblib.dump(model, model_path)

        if metadata is not None:
            meta_path = self.base_dir / f"{name}.json"
            meta_path.write_text(json.dumps(metadata, default=str), encoding="utf-8")

        return model_path

    def load(self, name: str) -> Any:
        """Load a model from disk.

        Raises:
            FileNotFoundError: If the model file does not exist.
        """
        model_path = self.base_dir / f"{name}.joblib"
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        return joblib.load(model_path)

    def load_metadata(self, name: str) -> dict:
        """Load metadata for a saved model, or return an empty dict if absent."""
        meta_path = self.base_dir / f"{name}.json"
        if not meta_path.exists():
            return {}
        return json.loads(meta_path.read_text(encoding="utf-8"))

    def list_models(self) -> list[str]:
        """Return the names of all saved models."""
        return sorted(p.stem for p in self.base_dir.glob("*.joblib"))

    def exists(self, name: str) -> bool:
        """Return True if a model with this name exists."""
        return (self.base_dir / f"{name}.joblib").exists()

    def delete(self, name: str) -> None:
        """Delete a saved model and its metadata if present."""
        model_path = self.base_dir / f"{name}.joblib"
        meta_path = self.base_dir / f"{name}.json"
        if model_path.exists():
            model_path.unlink()
        if meta_path.exists():
            meta_path.unlink()
