"""Economics page for the Africa Data Intelligence dashboard."""

import pandas as pd
import streamlit as st

from dashboard.components import charts


_ECONOMIC_DATA = pd.DataFrame(
    {
        "year": [2019, 2020, 2021, 2022, 2023],
        "gdp_usd_billions": [95.5, 101.0, 110.3, 113.4, 108.9],
        "inflation_pct": [5.2, 5.4, 6.1, 7.6, 7.7],
    }
)


def render() -> None:
    """Render the economics page."""
    st.title("Economic Indicators")
    st.caption("Kenya — 2019 to 2023")

    col1, col2 = st.columns(2)

    with col1:
        fig = charts.line_chart(
            _ECONOMIC_DATA,
            x="year",
            y="gdp_usd_billions",
            title="GDP (USD billions)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = charts.bar_chart(
            _ECONOMIC_DATA,
            x="year",
            y="inflation_pct",
            title="Inflation (%)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Raw data"):
        st.dataframe(_ECONOMIC_DATA, use_container_width=True)

