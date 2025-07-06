# UltraMegaCalendar

This is a cool calendar application with desktop and Telegram notifications.

## Project Status

The core infrastructure and basic functionalities are in place. We have:

*   **Backend:** A FastAPI application with PostgreSQL integration for user configurations, events, and reminders. It now publishes delayed reminder messages to RabbitMQ using FastStream.
*   **Telegram Notifier:** A Python application that consumes messages from RabbitMQ and sends notifications via Telegram. Basic bot commands are implemented.
*   **Desktop Notifier:** A Python application that consumes messages from RabbitMQ and sends desktop notifications, also forwarding them to connected WebSocket clients.
*   **Desktop UI:** An Electron application built with React, capable of connecting to the desktop notifier's WebSocket for real-time notifications.

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

## Next Steps

To complete the project, the following tasks need to be addressed:

*   **Backend:**
    *   Implement the remaining CRUD operations for events and reminders.
    *   Refine the reminder calculation logic to support various user preferences (e.g., different reminder intervals).
*   **Telegram Notifier:**
    *   Implement more comprehensive bot commands for interacting with the backend (e.g., creating, listing, updating, and deleting events).
    *   Improve error handling and user feedback for bot interactions.
*   **Desktop Notifier:**
    *   Enhance desktop notification features (e.g., custom sounds, actions).
*   **Desktop UI:**
    *   Implement a full-fledged user interface for creating, reading, updating, and deleting events.
    *   Add a configuration section for users to set their Telegram chat ID and desktop device ID.
    *   Improve the visual design and user experience.
