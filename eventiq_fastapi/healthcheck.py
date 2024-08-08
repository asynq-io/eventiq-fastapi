from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .dependencies import ServiceDependency

healthcheck_router = APIRouter()


@healthcheck_router.get(
    "",
    response_class=JSONResponse,
    include_in_schema=False,
)
async def healthcheck(service: ServiceDependency) -> JSONResponse:
    if service.broker.is_connected:
        return JSONResponse(status_code=200, content={"status": "ok"})
    return JSONResponse(status_code=503, content={"status": "error"})
