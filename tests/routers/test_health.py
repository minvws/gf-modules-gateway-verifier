from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient
from gfmodules.logging.testing import capture_records

from app.container import get_jwt_service
from app.logging.events import Log
from app.routers.health import router


def test_health_reports_the_jwks_endpoint() -> None:
    jwt_service = MagicMock()
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_jwt_service] = lambda: jwt_service
    client = TestClient(app)

    with capture_records("app.routers.health") as captured:
        jwt_service.health_check.return_value = True
        healthy = client.get("/health")
        jwt_service.health_check.return_value = False
        unhealthy = client.get("/health")

    assert healthy.status_code == 200
    assert healthy.json() == {"status": "ok", "components": {"jwks_url": "ok"}}
    assert unhealthy.status_code == 503
    assert unhealthy.json() == {"status": "error", "components": {"jwks_url": "error"}}
    events = captured.for_event(Log.HEALTH_UNHEALTHY)
    assert len(events) == 1
    assert events[0].message["component"] == "jwks_url"
    assert events[0].message["status"] == "error"
