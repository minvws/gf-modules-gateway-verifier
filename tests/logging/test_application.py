from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from gfmodules.logging import LoggingStreams
from gfmodules.logging.middleware import RequestContextMiddleware
from gfmodules.logging.testing import capture_records, capture_stream
from pytest_mock import MockerFixture

from app import application
from app.logging.events import Log


def test_a_startup_failure_is_logged_as_an_unhandled_exception(mocker: MockerFixture) -> None:
    mocker.patch("app.application.application_init")
    mocker.patch("app.application.setup_fastapi", side_effect=RuntimeError("startup boom"))

    with capture_records(application.logger.name) as captured, pytest.raises(RuntimeError):
        application.create_fastapi_app()

    records: list[Any] = [entry.record for entry in captured.entries]
    assert [record.event_id for record in records] == [Log.SYS_UNHANDLED_EXCEPTION.event_id]
    assert records[0].exception_type == "RuntimeError"


def test_an_unhandled_exception_answers_500_and_reaches_app_and_siem() -> None:
    fastapi = FastAPI()

    @fastapi.get("/boom")
    def boom() -> None:
        raise RuntimeError("explode")

    fastapi.add_exception_handler(Exception, application._unhandled_exception_handler)
    fastapi.add_middleware(RequestContextMiddleware)

    with (
        capture_stream(LoggingStreams.APP, application.logger.name) as app_stream,
        capture_stream(LoggingStreams.SIEM, application.logger.name) as siem_stream,
    ):
        response = TestClient(fastapi, raise_server_exceptions=False).get("/boom")

    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}
    assert app_stream[0]["exception_type"] == "RuntimeError"
    assert app_stream[0]["endpoint"] == "/boom"
    assert siem_stream[0]["exception_type"] == "RuntimeError"
