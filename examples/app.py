import asyncio

from eventiq import CloudEvent, Middleware, Publishes, Service
from eventiq.backends.nats import JetStreamBroker
from fastapi import FastAPI
from pydantic import BaseModel

from eventiq_fastapi import get_service_lifespan

broker = JetStreamBroker(url="nats://nats:password@localhost:4222")


class MyData(BaseModel):
    """Main data for service"""

    counter: int
    info: str


class MyEvent(CloudEvent[MyData]):
    """Some custom event"""


class MyCommand(CloudEvent[int], topic="commands.run"):
    """Command representing current number of items"""


class SendMessageMiddleware(Middleware):
    async def after_broker_connect(self):
        await asyncio.sleep(5)
        for i in range(5):
            event = MyEvent.new(MyData(counter=i, info="default"), topic="test.topic")
            await service.publish(event)
        self.logger.info("Published event(s)")


service = Service(
    name="example-service",
    version="1.0",
    broker=broker,
    publishes=[
        Publishes(
            type=MyEvent,
            topic="test.topic.{param}.*",
            tags=["tag2"],
            summary="Publishes when X happens",
            parameters={
                "param": {
                    "enum": ["x", "y", "z"],
                    "description": "Description for param",
                },
            },
        ),
    ],
    tags_metadata=[{"name": "tag1", "description": "Some tag 1"}],
)


@service.subscribe(
    topic="test.topic.{param}.*",
    tags=["tag1"],
    parameters={
        "param": {
            "enum": ["a", "b", "c"],
            "description": "Some description",
            "examples": ["a", "b"],
        }
    },
)
async def example_handler(message: MyEvent) -> None:
    """Consumer for processing MyEvent(s)"""
    print(f"Received Message {message.id} with data: {message.data}")


@service.subscribe
async def example_run(message: MyCommand) -> None:
    """Consumer for processing MyCommands(s)"""
    print(f"Received Message {message.id} with data: {message.data}")


app = FastAPI(lifespan=get_service_lifespan(service))
