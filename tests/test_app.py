from fastapi import FastAPI


async def test_app_instance(app):
    assert isinstance(app, FastAPI)


async def test_healthcheck(client):
    response = await client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_fail_healthcheck(client, service):
    service.broker._connected = False
    response = await client.get("/healthcheck")
    assert response.status_code == 503


async def test_asyncapi_json_route(client):
    response = await client.get("/asyncapi.json")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["asyncapi"] == "3.0.0"


async def test_asyncapi_html_file(client):
    response = await client.get("/asyncapi")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"


async def get_not_found(client):
    response = await client.get("/not_found")
    assert response.status_code == 404


async def test_service_dependency(client):
    response = await client.get("/test-service")
    assert response.status_code == 200
