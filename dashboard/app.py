"""Africa Data Intelligence dashboard - entry point."""

import streamlit as st

from dashboard.pages import ( climate, countries, economics,  explorer, home, ml_results)

st.set_page_config(
    page_title="Africa Data Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    """Render the dashboard with sidebar navigation."""
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Dataset Explorer", "Countries"],
    )

    if page == "Home":
        home.render()
    elif page == "Dataset Explorer":
        explorer.render()
    elif page == "Countries":
        countries.render()

    page = st.sidebar.radio(
        "Go to",
        ["Home", "Dataset Explorer", "Countries", "Economics"],
    )

    if page == "Home":
        home.render()
    elif page == "Dataset Explorer":
        explorer.render()
    elif page == "Countries":
        countries.render()
    elif page == "Economics":
        economics.render()
    
    page = st.sidebar.radio(
        "Go to",
        ["Home", "Dataset Explorer", "Countries", "Economics", "Climate", "ML Results"],
    )

    if page == "Home":
        home.render()
    elif page == "Dataset Explorer":
        explorer.render()
    elif page == "Countries":
        countries.render()
    elif page == "Economics":
        economics.render()
    elif page == "Climate":
        climate.render()
    elif page == "ML Results":
        ml_results.render()
   page = st.sidebar.radio(
        "Go to",
        [
            "Home",
            "Dataset Explorer",
            "Countries",
            "Economics",
            "Climate",
            "ML Results",
            "Forecast",
        ],
    )

    if page == "Home":
        home.render()
    elif page == "Dataset Explorer":
        explorer.render()
    elif page == "Countries":
        countries.render()
    elif page == "Economics":
        economics.render()
    elif page == "Climate":
        climate.render()
    elif page == "ML Results":
        ml_results.render()
    elif page == "Forecast":
        forecast.render()
if __name__ == "__main__":
    main()
