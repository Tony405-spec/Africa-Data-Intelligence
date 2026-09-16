"""Unit tests for dashboard chart components."""

import pandas as pd

from dashboard.components import charts


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "month": ["Jan", "Feb", "Mar"],
            "sales": [100, 150, 200],
            "category": ["A", "B", "C"],
        }
    )


def test_line_chart_returns_figure():
    fig = charts.line_chart(_df(), x="month", y="sales", title="Test")
    assert fig is not None
    assert fig.layout.title.text == "Test"


def test_bar_chart_returns_figure():
    fig = charts.bar_chart(_df(), x="month", y="sales", title="Bars")
    assert fig.layout.title.text == "Bars"


def test_pie_chart_returns_figure():
    fig = charts.pie_chart(_df(), names="category", values="sales", title="Pie")
    assert fig.layout.title.text == "Pie"


def test_color_sequence_has_five_colours():
    colours = list(charts.color_sequence())
    assert len(colours) == 5
    assert all(c.startswith("#") for c in colours)

