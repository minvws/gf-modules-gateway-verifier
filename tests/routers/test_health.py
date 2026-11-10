from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.container import get_jwt_service
from app.routers.health import router


def test_health_reports_the_jwks_endpoint() -> None:
    jwt_service = MagicMock()
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_jwt_service] = lambda: jwt_service
    client = TestClient(app)

    jwt_service.health_check.return_value = True
    healthy = client.get("/health")
    jwt_service.health_check.return_value = False
    unhealthy = client.get("/health")

    assert healthy.status_code == 200
    assert healthy.json() == {"status": "ok", "components": {"jwks_url": "ok"}}
    assert unhealthy.status_code == 503
    assert unhealthy.json() == {"status": "error", "components": {"jwks_url": "error"}}
