"""Nigerian dataset definitions for the Africa Data Intelligence catalog."""

from datetime import date

from africa_data_intelligence.catalog.base import DatasetEntry


NIGERIA_DATASETS: list[DatasetEntry] = [
    DatasetEntry(
        name="Nigeria Population by State",
        source="https://nigeria.opendataforafrica.org/",
        country="Nigeria",
        geographic_level="state",
        temporal_coverage="2006-2022",
        license="CC-BY-4.0",
        update_frequency="annual",
        variables=["state", "year", "population"],
        last_updated=date(2024, 1, 1),
        tags=["population", "demographics"],
    ),
    DatasetEntry(
        name="Nigeria Oil Production",
        source="https://www.opec.org/",
        country="Nigeria",
        geographic_level="national",
        temporal_coverage="2000-2023",
        license="CC-BY-4.0",
        update_frequency="monthly",
        variables=["year", "month", "barrels_per_day"],
        last_updated=date(2024, 1, 1),
        tags=["energy", "oil", "economy"],
    ),
    DatasetEntry(
        name="Nigeria Rainfall by State",
        source="https://nimet.gov.ng/",
        country="Nigeria",
        geographic_level="state",
        temporal_coverage="1981-2023",
        license="CC-BY-4.0",
        update_frequency="daily",
        variables=["state", "date", "rainfall_mm"],
        last_updated=date(2024, 1, 1),
        tags=["climate", "rainfall"],
    ),
]


def get_nigeria_datasets() -> list[DatasetEntry]:
    """Return the list of Nigerian dataset entries."""
    return list(NIGERIA_DATASETS)
