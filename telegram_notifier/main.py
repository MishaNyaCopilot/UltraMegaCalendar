import asyncio
import os
from dotenv import load_dotenv
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from telegram.ext import Application

from .bot import create_bot
from .config import settings

load_dotenv()

broker = RabbitBroker(settings.rabbitmq_url)
app = FastStream(broker)

telegram_app: Application | None = None

@app.on_startup
async def startup():
    global telegram_app
    telegram_app = create_bot(settings.telegram_token)
    asyncio.create_task(telegram_app.run_polling())

@app.on_shutdown
async def shutdown():
    if telegram_app:
        await telegram_app.shutdown()

@broker.subscriber("notification.telegram")
async def handle_telegram_notification(message: dict):
    if telegram_app:
        chat_id = message.get("telegram_chat_id")
        event_title = message.get("event_title")
        if chat_id and event_title:
            await telegram_app.bot.send_message(chat_id=chat_id, text=f"Reminder: {event_title}")

if __name__ == "__main__":
    asyncio.run(app.run())