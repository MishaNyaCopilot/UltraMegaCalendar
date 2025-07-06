import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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

def create_bot(token: str) -> Application:
    """Create the Telegram bot."""
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    return application
