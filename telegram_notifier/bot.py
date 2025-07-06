import logging
import httpx
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime

from .config import settings
from .schemas import EventCreate

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Your chat ID is {update.effective_chat.id}",
    )

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Links the Telegram chat ID to the user in the backend."""
    chat_id = update.effective_chat.id
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(f"{settings.backend_url}/users/1", json={
                "telegram_chat_id": str(chat_id)
            })
            response.raise_for_status()
        await update.message.reply_text(f"Your chat ID {chat_id} has been linked to the backend.")
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"Failed to link chat ID: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        await update.message.reply_text(f"An error occurred while requesting: {e}")

async def create_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Creates a new event in the backend."""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /create_event <title> <start_time> [description] [end_time] [location]\nExample: /create_event \"\"\"Meeting\"\"\" \"\"\"2025-07-08 10:00\"\"\" \"\"\"Team sync\"\"")
        return

    title = args[0]
    start_time_str = args[1]
    description = args[2] if len(args) > 2 else None
    end_time_str = args[3] if len(args) > 3 else None
    location = args[4] if len(args) > 4 else None

    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M") if end_time_str else None

        event_data = EventCreate(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.backend_url}/users/1/events/", json=event_data.dict())
            response.raise_for_status()
        await update.message.reply_text("Event created successfully!")
    except ValueError:
        await update.message.reply_text("Invalid date/time format. Please use YYYY-MM-DD HH:MM")
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"Failed to create event: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        await update.message.reply_text(f"An error occurred while requesting: {e}")

async def list_events_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all events from the backend."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.backend_url}/events/")
            response.raise_for_status()
        events = response.json()
        if events:
            message_text = "Your events:\n"
            for event in events:
                message_text += f"- {event['title']} (ID: {event['id']})\n"
                message_text += f"  Start: {event['start_time']}\n"
                if event.get('end_time'):
                    message_text += f"  End: {event['end_time']}\n"
                if event.get('description'):
                    message_text += f"  Description: {event['description']}\n"
                if event.get('location'):
                    message_text += f"  Location: {event['location']}\n"
            await update.message.reply_text(message_text)
        else:
            await update.message.reply_text("No events found.")
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"Failed to fetch events: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        await update.message.reply_text(f"An error occurred while requesting: {e}")

async def update_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Updates an existing event in the backend."""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /update_event <event_id> <field> <value>\nExample: /update_event 1 title \"New Title\"")
        return

    event_id = args[0]
    field = args[1]
    value = " ".join(args[2:])

    try:
        update_data = {field: value}
        if field == "start_time" or field == "end_time":
            update_data[field] = datetime.strptime(value, "%Y-%m-%d %H:%M")

        async with httpx.AsyncClient() as client:
            response = await client.put(f"{settings.backend_url}/events/{event_id}", json=update_data)
            response.raise_for_status()
        await update.message.reply_text("Event updated successfully!")
    except ValueError:
        await update.message.reply_text("Invalid date/time format. Please use YYYY-MM-DD HH:MM")
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"Failed to update event: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        await update.message.reply_text(f"An error occurred while requesting: {e}")

async def delete_event_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deletes an event from the backend."""
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /delete_event <event_id>")
        return

    event_id = args[0]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{settings.backend_url}/events/{event_id}")
            response.raise_for_status()
        await update.message.reply_text(f"Event {event_id} deleted successfully!")
    except httpx.HTTPStatusError as e:
        await update.message.reply_text(f"Failed to delete event: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        await update.message.reply_text(f"An error occurred while requesting: {e}")

def create_bot(token: str) -> Application:
    """Create the Telegram bot."""
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("link", link))
    application.add_handler(CommandHandler("create_event", create_event_command))
    application.add_handler(CommandHandler("list_events", list_events_command))
    application.add_handler(CommandHandler("update_event", update_event_command))
    application.add_handler(CommandHandler("delete_event", delete_event_command))

    return application

