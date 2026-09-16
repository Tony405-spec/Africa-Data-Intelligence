"""Kenyan dataset definitions for the Africa Data Intelligence catalog."""

from datetime import date

from africa_data_intelligence.catalog.base import DatasetEntry


KENYA_DATASETS: list[DatasetEntry] = [
    DatasetEntry(
        name="Kenya Population by County",
        source="https://www.knbs.or.ke/",
        country="Kenya",
        geographic_level="county",
        temporal_coverage="2009-2019",
        license="CC-BY-4.0",
        update_frequency="decennial",
        variables=["county", "year", "population", "male", "female"],
        last_updated=date(2024, 1, 1),
        tags=["population", "census", "demographics"],
    ),
    DatasetEntry(
        name="Kenya GDP by Sector",
        source="https://www.knbs.or.ke/",
        country="Kenya",
        geographic_level="national",
        temporal_coverage="2010-2023",
        license="CC-BY-4.0",
        update_frequency="annual",
        variables=["year", "sector", "gdp_kes_billions"],
        last_updated=date(2024, 1, 1),
        tags=["economy", "gdp"],
    ),
    DatasetEntry(
        name="Kenya Rainfall by Station",
        source="https://meteo.go.ke/",
        country="Kenya",
        geographic_level="station",
        temporal_coverage="1981-2023",
        license="CC-BY-4.0",
        update_frequency="daily",
        variables=["station_id", "date", "rainfall_mm"],
        last_updated=date(2024, 1, 1),
        tags=["climate", "rainfall", "weather"],
    ),
]


def get_kenya_datasets() -> list[DatasetEntry]:
    """Return the list of Kenyan dataset entries."""
    return list(KENYA_DATASETS)
