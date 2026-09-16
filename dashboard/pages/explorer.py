"""Dataset explorer page for the Africa Data Intelligence dashboard."""

import streamlit as st


_DATASETS = [
    {"name": "Kenya Population by County", "country": "Kenya", "category": "population"},
    {"name": "Kenya GDP by Sector", "country": "Kenya", "category": "economy"},
    {"name": "Kenya Rainfall by Station", "country": "Kenya", "category": "climate"},
    {"name": "Nigeria Population by State", "country": "Nigeria", "category": "population"},
    {"name": "Nigeria Oil Production", "country": "Nigeria", "category": "energy"},
]


def render() -> None:
    """Render the dataset explorer page."""
    st.title("Dataset Explorer")

    countries = sorted({d["country"] for d in _DATASETS})
    selected_country = st.selectbox("Filter by country", ["All"] + countries)

    filtered = _DATASETS
    if selected_country != "All":
        filtered = [d for d in _DATASETS if d["country"] == selected_country]

    st.dataframe(filtered, use_container_width=True)
    st.caption(f"Showing {len(filtered)} of {len(_DATASETS)} datasets")
