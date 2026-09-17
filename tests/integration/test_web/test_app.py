"""Integration tests for the web API."""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")


def test_health_endpoint() -> None:
    """`/health` reports the service as up."""
    from fastapi.testclient import TestClient

    from om4mtools.web.app import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
