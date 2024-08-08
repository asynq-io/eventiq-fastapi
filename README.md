![Tests](https://github.com/asynq-io/eventiq-fastapi/workflows/Tests/badge.svg)
![Build](https://github.com/asynq-io/eventiq-fastapi/workflows/Publish/badge.svg)
![License](https://img.shields.io/github/license/asynq-io/eventiq-fastapi)
![Mypy](https://img.shields.io/badge/mypy-checked-blue)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Python](https://img.shields.io/pypi/pyversions/eventiq-fastapi)
![Format](https://img.shields.io/pypi/format/eventiq-fastapi)
![PyPi](https://img.shields.io/pypi/v/eventiq-fastapi)

# eventiq-fastapi

FastAPI integration for eventiq


## Installation

```shell
pip install eventiq-fastapi
```

## Usage

```python
from fastapi import FastAPI
from eventiq import Service, CloudEvent
from eventiq_fastapi import ServiceDependency, get_service_lifespan


service = Service(...)
app = FastAPI(lifespan=get_service_lifespan(service))

# possibly in dirrerent file/router, service will be injected
@app.post("/send-email")
async def send_mail(service: ServiceDependency):
    await service.send({"some": "data"}, topic="commands.send-email")
```
