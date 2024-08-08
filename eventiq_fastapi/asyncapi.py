import json

from eventiq.asyncapi import get_async_api_spec
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic_asyncapi.v3 import AsyncAPI

from .dependencies import ServiceDependency

ASYNCAPI_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="https://www.asyncapi.com/favicon.ico">
    </head>
    <body>
        <script src="https://unpkg.com/@asyncapi/web-component@latest/lib/asyncapi-web-component.js" defer></script>
        <asyncapi-component
          schemaUrl="{asyncapi_url}",
          config='{config}',
          cssImportPath="https://unpkg.com/@asyncapi/react-component@latest/styles/default.min.css">
        </asyncapi-component>
    </body>
    </html>
"""


asyncapi_router = APIRouter(prefix="/asyncapi")


@asyncapi_router.get("", include_in_schema=False, response_class=HTMLResponse)
async def get_asyncapi(request: Request) -> HTMLResponse:
    return HTMLResponse(
        content=ASYNCAPI_HTML.format(
            asyncapi_url="asyncapi.json",
            title=getattr(request.app, "title", "Async API"),
            config=json.dumps(
                getattr(
                    request.app.state,
                    "asyncapi_config",
                    {"show": {"info": True, "sidebar": True}},
                )
            ),
        )
    )


@asyncapi_router.get(".json", include_in_schema=False, response_model=AsyncAPI)
async def get_asyncapi_json(service: ServiceDependency) -> AsyncAPI:
    return get_async_api_spec(service)
