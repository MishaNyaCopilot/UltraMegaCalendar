import React, { useState, useEffect } from 'react';

function UserConfigForm({ onSubmit, initialConfig }) {
  const [telegramChatId, setTelegramChatId] = useState('');
  const [desktopDeviceId, setDesktopDeviceId] = useState('');
  const [defaultReminderMinutesBefore, setDefaultReminderMinutesBefore] = useState(15);

  useEffect(() => {
    if (initialConfig) {
      setTelegramChatId(initialConfig.telegram_chat_id || '');
      setDesktopDeviceId(initialConfig.desktop_device_id || '');
      setDefaultReminderMinutesBefore(initialConfig.default_reminder_minutes_before || 15);
    }
  }, [initialConfig]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      telegram_chat_id: telegramChatId || null,
      desktop_device_id: desktopDeviceId || null,
      default_reminder_minutes_before: parseInt(defaultReminderMinutesBefore, 10),
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>User Configuration</h2>
      <label>
        Telegram Chat ID:
        <input
          type="text"
          value={telegramChatId}
          onChange={(e) => setTelegramChatId(e.target.value)}
        />
      </label>
      <label>
        Desktop Device ID:
        <input
          type="text"
          value={desktopDeviceId}
          onChange={(e) => setDesktopDeviceId(e.target.value)}
        />
      </label>
      <label>
        Default Reminder (minutes before):
        <input
          type="number"
          value={defaultReminderMinutesBefore}
          onChange={(e) => setDefaultReminderMinutesBefore(e.target.value)}
        />
      </label>
      <button type="submit">Save Configuration</button>
    </form>
  );
}

export default UserConfigForm;
