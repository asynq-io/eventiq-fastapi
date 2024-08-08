from typing import Annotated

from eventiq import Service
from fastapi import Depends, Request
from typing_extensions import TypeAlias


async def get_service(request: Request) -> Service:
    return request.app.state.service


ServiceDependency: TypeAlias = Annotated[Service, Depends(get_service, use_cache=True)]
