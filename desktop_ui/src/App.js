import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [notification, setNotification] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8765');

    ws.onmessage = (event) => {
      setNotification(event.data);
      setTimeout(() => {
        setNotification(null);
      }, 5000);
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>UltraMegaCalendar</h1>
      </header>
      {notification && (
        <div className="notification">
          <p>{notification}</p>
        </div>
      )}
    </div>
  );
}

export default App;
