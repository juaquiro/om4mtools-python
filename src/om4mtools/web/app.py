"""FastAPI application exposing the core API over HTTP."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="om4mtools")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check.

    Returns
    -------
    dict[str, str]
        ``{"status": "ok"}`` when the service is up.
    """
    return {"status": "ok"}
