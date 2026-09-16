"""Country endpoints for the Africa Data Intelligence API."""

from fastapi import APIRouter

router = APIRouter(prefix="/countries", tags=["countries"])


_COUNTRIES: list[dict[str, str]] = [
    {"code": "KE", "name": "Kenya", "region": "East Africa"},
    {"code": "NG", "name": "Nigeria", "region": "West Africa"},
    {"code": "ZA", "name": "South Africa", "region": "Southern Africa"},
    {"code": "GH", "name": "Ghana", "region": "West Africa"},
    {"code": "TZ", "name": "Tanzania", "region": "East Africa"},
    {"code": "UG", "name": "Uganda", "region": "East Africa"},
    {"code": "ET", "name": "Ethiopia", "region": "East Africa"},
    {"code": "EG", "name": "Egypt", "region": "North Africa"},
]


@router.get("")
def list_countries() -> list[dict[str, str]]:
    """Return a list of supported countries."""
    return _COUNTRIES


@router.get("/{code}")
def get_country(code: str) -> dict[str, str]:
    """Return a country by ISO code.

    Raises:
        HTTPException: 404 if the code is not registered.
    """
    from fastapi import HTTPException

    for country in _COUNTRIES:
        if country["code"].lower() == code.lower():
            return country
    raise HTTPException(status_code=404, detail=f"Country not found: {code}")
