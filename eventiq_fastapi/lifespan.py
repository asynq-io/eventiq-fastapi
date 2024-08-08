import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from typing import Callable

from eventiq import Service
from fastapi import FastAPI
from typing_extensions import AsyncContextManager


def get_service_lifespan(
    service: Service, run: bool = False
) -> Callable[[FastAPI], AsyncContextManager[None]]:
    @asynccontextmanager
    async def run_service_lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.service = service
        task = asyncio.create_task(service.run(enable_signal_handler=False))
        await asyncio.sleep(0)
        yield
        with suppress(asyncio.CancelledError):
            task.cancel()
            await task

    @asynccontextmanager
    async def service_connect_lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.service = service
        await service.connect()
        yield
        await service.disconnect()

    return run_service_lifespan if run else service_connect_lifespan
