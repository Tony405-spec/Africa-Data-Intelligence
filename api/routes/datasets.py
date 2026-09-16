"""Dataset endpoints for the Africa Data Intelligence API."""

from fastapi import APIRouter, HTTPException

from api.schemas.dataset import DatasetDetail, DatasetSummary

router = APIRouter(prefix="/datasets", tags=["datasets"])


_DATASETS: dict[str, DatasetDetail] = {
    "Kenya Population by County": DatasetDetail(
        name="Kenya Population by County",
        source="https://www.knbs.or.ke/",
        country="Kenya",
        geographic_level="county",
        temporal_coverage="2009-2019",
        license="CC-BY-4.0",
        update_frequency="decennial",
        variables=["county", "year", "population"],
        tags=["population", "census"],
        last_updated="2024-01-01",
    ),
    "Nigeria Oil Production": DatasetDetail(
        name="Nigeria Oil Production",
        source="https://www.opec.org/",
        country="Nigeria",
        geographic_level="national",
        temporal_coverage="2000-2023",
        license="CC-BY-4.0",
        update_frequency="monthly",
        variables=["year", "month", "barrels_per_day"],
        tags=["energy", "oil"],
        last_updated="2024-01-01",
    ),
}


@router.get("", response_model=list[DatasetSummary])
def list_datasets() -> list[DatasetSummary]:
    """Return a summary of all registered datasets."""
    return [
        DatasetSummary(
            name=entry.name,
            country=entry.country,
            geographic_level=entry.geographic_level,
            license=entry.license,
        )
        for entry in _DATASETS.values()
    ]


@router.get("/{name}", response_model=DatasetDetail)
def get_dataset(name: str) -> DatasetDetail:
    """Return a single dataset by name.

    Raises:
        HTTPException: 404 if the dataset is not registered.
    """
    if name not in _DATASETS:
        raise HTTPException(status_code=404, detail=f"Dataset not found: {name}")
    return _DATASETS[name]
