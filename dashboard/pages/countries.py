"""Countries page for the Africa Data Intelligence dashboard."""

import streamlit as st


_COUNTRIES = [
    {"code": "KE", "name": "Kenya", "region": "East Africa"},
    {"code": "NG", "name": "Nigeria", "region": "West Africa"},
    {"code": "ZA", "name": "South Africa", "region": "Southern Africa"},
    {"code": "GH", "name": "Ghana", "region": "West Africa"},
    {"code": "TZ", "name": "Tanzania", "region": "East Africa"},
    {"code": "UG", "name": "Uganda", "region": "East Africa"},
]


def render() -> None:
    """Render the countries page."""
    st.title("Countries")
    st.dataframe(_COUNTRIES, use_container_width=True)
    st.caption(f"{len(_COUNTRIES)} countries currently supported")
