import asyncio
import websockets
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from .notifier import send_notification
from .config import settings

broker = RabbitBroker(settings.rabbitmq_url)
app = FastStream(broker)

connected_websockets = set()

async def websocket_handler(websocket, path):
    connected_websockets.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_websockets.remove(websocket)

@app.on_startup
async def startup():
    asyncio.create_task(websockets.serve(websocket_handler, "localhost", 8765))

@broker.subscriber("notification.desktop")
async def handle_desktop_notification(message: dict):
    event_title = message.get("event_title")
    if event_title:
        send_notification("New Event", event_title)
        # Also send to connected WebSocket clients
        for websocket in connected_websockets:
            await websocket.send(f"New Event: {event_title}")

if __name__ == "__main__":
    app.run()