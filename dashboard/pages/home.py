"""Home page for the Africa Data Intelligence dashboard."""

import streamlit as st


def render() -> None:
    """Render the home page."""
    st.title("Africa Data Intelligence")
    st.markdown(
        "An open-source platform for exploring, analyzing, modeling, "
        "and visualizing African data."
    )

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("Datasets", "3+")
    col2.metric("Countries", "8")
    col3.metric("ML Models", "4")

    st.markdown("---")
    st.markdown("### What you can do")
    st.markdown(
        """
        - Explore datasets by country and category
        - Compare model performance
        - Generate forecasts
        - Download reports
        """
    )

