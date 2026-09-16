"""FastAPI application for Africa Data Intelligence."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import countries, datasets, health

app = FastAPI(
    title="Africa Data Intelligence API",
    description="Open-source API for African datasets.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(datasets.router)
app.include_router(countries.router)
@app.get("/")
def root() -> dict[str, str]:
    """Return a friendly landing message."""
    return {
        "name": "Africa Data Intelligence API",
        "version": "0.1.0",
        "docs": "/docs",
    }
