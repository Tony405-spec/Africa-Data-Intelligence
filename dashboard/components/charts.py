"""Reusable chart components for the Africa Data Intelligence dashboard."""

from typing import Iterable

import pandas as pd
import plotly.express as px


BRAND_PRIMARY = "#ff6666"
BRAND_SECONDARY = "#525266"


def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
):
    """Return a Plotly line chart styled with project colours."""
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_traces(line_color=BRAND_PRIMARY, line_width=2)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=BRAND_SECONDARY,
    )
    return fig


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
):
    """Return a Plotly bar chart styled with project colours."""
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_traces(marker_color=BRAND_PRIMARY)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=BRAND_SECONDARY,
    )
    return fig


def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
):
    """Return a Plotly pie chart with a branded colour sequence."""
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=[
            BRAND_PRIMARY,
            BRAND_SECONDARY,
            "#cbbeb5",
            "#ffe5a9",
            "#423f3b",
        ],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color=BRAND_SECONDARY,
    )
    return fig


def color_sequence() -> Iterable[str]:
    """Return the standard brand colour sequence."""
    return [BRAND_PRIMARY, BRAND_SECONDARY, "#cbbeb5", "#ffe5a9", "#423f3b"]

