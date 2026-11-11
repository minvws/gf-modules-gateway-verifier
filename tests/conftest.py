from collections.abc import Iterator
from typing import Any

import gfmodules.logging as gflog
import pytest
from gfmodules.logging import ConfigLogging
from gfmodules.logging.testing import reset_for_tests

from app.config import (
    Config,
    ConfigApp,
    ConfigKongProxy,
    ConfigOin,
    ConfigStats,
    ConfigTelemetry,
    ConfigUvicorn,
    reset_config,
    set_config,
)
from app.logging.events import Log


@pytest.fixture
def oin() -> str:
    return "00000001123456700000"


def make_config(**overrides: Any) -> Config:
    sections: dict[str, Any] = {
        "app": ConfigApp(),
        "oin": ConfigOin(
            issuer="test-issuer",
            audience=["test-audience"],
            jwks_url="http://localhost/jwks",
        ),
        "telemetry": ConfigTelemetry(endpoint=None, service_name=None, tracer_name=None),
        "stats": ConfigStats(host=None, port=None, module_name=None),
        "uvicorn": ConfigUvicorn(ssl_base_dir=None, ssl_cert_file=None, ssl_key_file=None),
        "kong_proxy": ConfigKongProxy(url="http://kong.example.com"),
    }
    sections.update(overrides)
    return Config(**sections)


@pytest.fixture(autouse=True)
def default_config() -> Iterator[Config]:
    # Without this, get_config() reads app.conf from disk
    # exists on a developer's machine but not in CI.
    cfg = make_config()
    set_config(cfg)
    yield cfg
    reset_config()


@pytest.fixture(autouse=True)
def logging_catalogue() -> Iterator[None]:
    gflog.configure(
        config=ConfigLogging(console_streams=["debug"], access_logs=True),
        loglevel="DEBUG",
        catalogue=Log,
        strict_fields=True,
    )
    try:
        yield
    finally:
        reset_for_tests()
