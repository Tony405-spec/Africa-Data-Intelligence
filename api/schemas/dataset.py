 """Pydantic schemas for dataset endpoints."""

from typing import Optional

from pydantic import BaseModel, Field


class DatasetSummary(BaseModel):
    """Minimal dataset representation for list endpoints."""

    name: str = Field(..., description="Dataset name")
    country: str = Field(..., description="Country of coverage")
    geographic_level: str = Field(..., description="Geographic granularity")
    license: str = Field(..., description="License identifier")


class DatasetDetail(DatasetSummary):
    """Detailed dataset representation including variables and source."""

    source: str
    temporal_coverage: str
    update_frequency: str
    variables: list[str]
    tags: list[str] = []
    last_updated: Optional[str] = None
