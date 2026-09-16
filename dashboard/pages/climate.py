"""Climate page for the Africa Data Intelligence dashboard."""

import pandas as pd
import streamlit as st

from dashboard.components import charts


_RAINFALL_DATA = pd.DataFrame(
    {
        "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "rainfall_mm": [30, 45, 120, 210, 170, 40, 25, 30, 50, 130, 160, 80],
        "temperature_c": [24, 25, 24, 23, 22, 21, 20, 21, 23, 24, 23, 23],
    }
)


def render() -> None:
    """Render the climate page."""
    st.title("Climate Patterns")
    st.caption("Nairobi — 2023 monthly averages")

    col1, col2 = st.columns(2)

    with col1:
        fig = charts.bar_chart(
            _RAINFALL_DATA,
            x="month",
            y="rainfall_mm",
            title="Monthly Rainfall (mm)",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = charts.line_chart(
            _RAINFALL_DATA,
            x="month",
            y="temperature_c",
            title="Monthly Temperature (°C)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Key observations")
    st.markdown(
        """
        - April and November are the wettest months (long and short rains)
        - Temperatures stay between 20°C and 25°C year round
        - Dry season runs from June to September
        """
    )

    with st.expander("Raw data"):
        st.dataframe(_RAINFALL_DATA, use_container_width=True)

