# UltraMegaCalendar

This is a cool calendar application with desktop and Telegram notifications.

## Project Status

The project is now complete! We have:

*   **Backend:** A FastAPI application with PostgreSQL integration for user configurations, events, and reminders. It now publishes delayed reminder messages to RabbitMQ using FastStream. All CRUD operations for `UserConfig`, `Event`, and `Reminder` are implemented. Reminder calculation now uses `default_reminder_minutes_before` from `UserConfig`.
*   **Telegram Notifier:** A Python application that consumes messages from RabbitMQ and sends notifications via Telegram. It now includes a `/link` command to associate a Telegram chat ID with a user in the backend, and commands to create (`/create_event`), list (`/list_events`), update (`/update_event`), and delete (`/delete_event`) events.
*   **Desktop Notifier:** A Python application that consumes messages from RabbitMQ and sends desktop notifications, also forwarding them to connected WebSocket clients.
*   **Desktop UI:** An Electron application built with React, capable of connecting to the desktop notifier's WebSocket for real-time notifications. It now includes forms for creating and updating events, a list to display events, and a form for managing user configurations (Telegram chat ID, desktop device ID, and default reminder minutes).

## How to Run

To run the application, you will need to:

1.  **Start the backend server:**
    *   Navigate to the `backend` directory.
    *   Make sure you have a PostgreSQL server running and have updated the `.env` file with the correct connection string.
    *   Run `uvicorn main:app --reload`.

2.  **Start the Telegram notifier:**
    *   Navigate to the `telegram_notifier` directory.
    *   Update the `.env` file with your Telegram bot token.
    *   Run `python main.py`.

3.  **Start the desktop notifier:**
    *   Navigate to the `desktop_notifier` directory.
    *   Run `python main.py`.

4.  **Start the desktop UI:**
    *   Navigate to the `desktop_ui` directory.
    *   Run `npm run electron:start`.

Alternatively, you can use the `run.bat` script in the root directory to start all services simultaneously.


