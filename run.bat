@echo off

echo Starting UltraMegaCalendar...

REM Start Backend
start "Backend" cmd /c "cd backend && uvicorn main:app --reload"

REM Start Telegram Notifier
start "Telegram Notifier" cmd /c "cd telegram_notifier && python main.py"

REM Start Desktop Notifier
start "Desktop Notifier" cmd /c "cd desktop_notifier && python main.py"

REM Start Desktop UI
start "Desktop UI" cmd /c "cd desktop_ui && npm run electron:start"

echo All services are starting in separate windows.
