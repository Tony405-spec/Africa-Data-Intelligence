"""Forecast page for the Africa Data Intelligence dashboard."""

import streamlit as st


def _linear_forecast(series: list[float]) -> float:
    """Return a simple linear-trend forecast for the next period."""
    n = len(series)
    x_mean = (n - 1) / 2
    y_mean = sum(series) / n
    numerator = sum((i - x_mean) * (y - y_mean) for i, y in enumerate(series))
    denominator = sum((i - x_mean) ** 2 for i in range(n)) or 1.0
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    return intercept + slope * n


def render() -> None:
    """Render the forecast page."""
    st.title("Demand Forecast")
    st.caption("Enter recent sales observations to get a next-period forecast")

    raw = st.text_area(
        "Observations (comma-separated)",
        value="200000, 220000, 210000, 240000, 260000",
        height=80,
    )

    if st.button("Generate Forecast"):
        try:
            series = [float(x.strip()) for x in raw.split(",") if x.strip()]
        except ValueError:
            st.error("Please enter numeric values separated by commas.")
            return

        if len(series) < 2:
            st.error("Please enter at least two observations.")
            return

        prediction = _linear_forecast(series)
        st.metric("Predicted Demand", f"KES {prediction:,.2f}")
        st.info(
            f"Forecast based on a linear trend over {len(series)} observations."
        )
