import asyncio
import websockets
from .notifier import send_notification

async def handler(websocket, path):
    async for message in websocket:
        send_notification("New Event", message)

def main():
    start_server = websockets.serve(handler, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
