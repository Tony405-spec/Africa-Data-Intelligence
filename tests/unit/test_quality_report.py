"""Unit tests for QualityReportBuilder."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.validation.quality_report import (
    QualityReport,
    QualityReportBuilder,
)


def test_build_basic_report():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    report = QualityReportBuilder().build(df)

    assert report.rows == 3
    assert report.columns == 2
    assert report.missing_values == 0
    assert report.duplicate_rows == 0


def test_report_detects_missing_values():
    df = pd.DataFrame({"a": [1, np.nan, 3]})
    report = QualityReportBuilder().build(df)

    assert report.missing_values == 1
    assert report.missing_percentage > 0


def test_report_detects_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2]})
    report = QualityReportBuilder().build(df)

    assert report.duplicate_rows == 1


def test_report_records_dtypes():
    df = pd.DataFrame({"a": [1], "b": ["x"]})
    report = QualityReportBuilder().build(df)

    assert "a" in report.column_dtypes
    assert "b" in report.column_dtypes


def test_to_dataframe():
    df = pd.DataFrame({"a": [1, 2]})
    report = QualityReportBuilder().build(df)
    tidy = report.to_dataframe()

    assert "metric" in tidy.columns
    assert "value" in tidy.columns
    assert "rows" in tidy["metric"].tolist()


def test_non_dataframe_raises():
    with pytest.raises(TypeError):
        QualityReportBuilder().build([1, 2, 3])


def test_empty_dataframe_handled():
    df = pd.DataFrame()
    report = QualityReportBuilder().build(df)

    assert report.rows == 0
    assert report.missing_percentage == 0.0

