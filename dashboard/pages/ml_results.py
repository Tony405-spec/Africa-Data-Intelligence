"""ML results page for the Africa Data Intelligence dashboard."""

import pandas as pd
import streamlit as st

from dashboard.components import charts


_MODEL_RESULTS = pd.DataFrame(
    {
        "model": ["Random Forest", "XGBoost", "LSTM"],
        "rmse": [43417.96, 45973.23, 51876.20],
        "mae": [31250.10, 33580.75, 38940.60],
        "r2": [0.8383, 0.8187, 0.7654],
    }
)


def render() -> None:
    """Render the ML results page."""
    st.title("Model Performance")
    st.caption("Comparison of forecasting models on Kenyan retail data")

    col1, col2, col3 = st.columns(3)
    best = _MODEL_RESULTS.loc[_MODEL_RESULTS["rmse"].idxmin()]
    col1.metric("Best Model", best["model"])
    col2.metric("R² Score", f"{best['r2']:.4f}")
    col3.metric("RMSE", f"KES {best['rmse']:,.0f}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig = charts.bar_chart(_MODEL_RESULTS, x="model", y="rmse", title="RMSE by Model")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = charts.bar_chart(_MODEL_RESULTS, x="model", y="r2", title="R² by Model")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Model comparison")
    st.dataframe(_MODEL_RESULTS, use_container_width=True)

