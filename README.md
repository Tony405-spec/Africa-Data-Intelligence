# Africa Data Intelligence

An open-source data intelligence platform for collecting, processing, analyzing, visualizing, and modeling African datasets.

## Overview

Africa Data Intelligence (ADI) provides a reusable technical foundation for working with datasets relating to African cities, economies, demographics, transportation, climate, agriculture, and technology.

## Technology Stack

- **Backend:** Python, FastAPI, PostgreSQL
- **Data:** pandas, NumPy, SQLAlchemy, Pydantic
- **Machine Learning:** scikit-learn, XGBoost
- **Visualization:** Plotly, Streamlit
- **Geospatial:** GeoPandas, Shapely
- **Engineering:** pytest, Ruff, pre-commit, GitHub Actions, Docker

## Repository Structure
Africa-Data-Intelligence/
├── api/ FastAPI application
├── dashboard/ Streamlit dashboard
├── data/ Data storage
├── datasets/ Dataset metadata and catalog
├── docs/ Documentation
├── notebooks/ Exploratory and modeling notebooks
├── src/ Core Python package
├── tests/ Unit and integration tests
└── scripts/ Utility scripts

## Getting Started

```bash
git clone https://github.com/Tony405-spec/Africa-Data-Intelligence.git
cd Africa-Data-Intelligence
python -m venv .venv
source .venv/Scripts/activate
pip install -e ".[dev]"

