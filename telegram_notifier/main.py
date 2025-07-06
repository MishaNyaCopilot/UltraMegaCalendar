import os
from dotenv import load_dotenv
from .bot import create_bot

load_dotenv()

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    app = create_bot(token)
    app.run_polling()

if __name__ == "__main__":
    main()
