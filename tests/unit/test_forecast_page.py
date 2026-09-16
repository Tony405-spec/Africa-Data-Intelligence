"""Unit tests for the forecast dashboard page."""

from dashboard.pages import forecast


def test_render_is_callable():
    assert callable(forecast.render)


def test_linear_forecast_increasing_series():
    result = forecast._linear_forecast([1, 2, 3, 4, 5])
    assert result == 6.0


def test_linear_forecast_flat_series():
    result = forecast._linear_forecast([10, 10, 10])
    assert result == 10.0


def test_linear_forecast_decreasing_series():
    result = forecast._linear_forecast([5, 4, 3, 2, 1])
    assert result == 0.0


def test_linear_forecast_two_points():
    result = forecast._linear_forecast([1, 3])
    assert result == 5.0

