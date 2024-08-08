import asyncio
from collections.abc import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from eventiq import Service
from eventiq.backends.stub import StubBroker
from fastapi import FastAPI
from httpx import AsyncClient

from eventiq_fastapi import ServiceDependency, get_service_lifespan
from eventiq_fastapi.asyncapi import asyncapi_router
from eventiq_fastapi.healthcheck import healthcheck_router


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture()
def broker():
    return StubBroker()


@pytest.fixture()
def service(broker):
    return Service(broker=broker, name="test_service")


@pytest.fixture()
def lifespan(service):
    return get_service_lifespan(service)


@pytest.fixture()
def app(lifespan):
    app = FastAPI(lifespan=lifespan)
    app.include_router(asyncapi_router)
    app.include_router(healthcheck_router, prefix="/healthcheck")

    @app.get("/test-service")
    async def test_service_dependency(x: ServiceDependency) -> dict[str, str]:
        assert isinstance(x, Service)
        return {"status": "ok"}

    return app


@pytest.fixture()
async def client(app) -> AsyncIterator[AsyncClient]:
    async with (
        LifespanManager(app, startup_timeout=30),
        AsyncClient(app=app, base_url="http://test") as ac,
    ):
        yield ac
