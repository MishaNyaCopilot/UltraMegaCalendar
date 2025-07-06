# UltraMegaCalendar

This is a cool calendar application with desktop and Telegram notifications.

## Project Status

The initial setup of the project is complete. The following components have been created:

*   **Backend:** A FastAPI application that will serve as the central API for the system. It includes database models for users, events, and reminders, as well as basic CRUD operations.
*   **Telegram Notifier:** A Python application that uses the `python-telegram-bot` library to send notifications to a Telegram chat.
*   **Desktop Notifier:** A Python application that uses `plyer` and `websockets` to send desktop notifications.
*   **Desktop UI:** An Electron application built with React that will serve as the main user interface for the application.

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

This will start all the services and the desktop application. You can then interact with the application through the desktop UI and the Telegram bot.

## Next Steps

*   **Backend:**
    *   Implement RabbitMQ integration for sending notifications.
    *   Add logic for calculating reminder times.
    *   Implement the remaining CRUD operations for events and reminders.
*   **Telegram Notifier:**
    *   Implement RabbitMQ consumer to receive notifications from the backend.
    *   Add more bot commands for interacting with the backend (e.g., creating events, listing events).
*   **Desktop Notifier:**
    *   Implement RabbitMQ consumer to receive notifications from the backend.
*   **Desktop UI:**
    *   Implement functionality for creating, reading, updating, and deleting events.
    *   Add a way for the user to configure their Telegram chat ID.
