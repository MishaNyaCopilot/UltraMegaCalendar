import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import EventForm from './components/EventForm';
import EventList from './components/EventList';
import UserConfigForm from './components/UserConfigForm';
import './App.css';

const API_URL = 'http://localhost:8072'; // Your FastAPI backend URL
const USER_ID = 1; // Assuming a single user for now

function App() {
  const [notification, setNotification] = useState(null);
  const [events, setEvents] = useState([]);
  const [userConfig, setUserConfig] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchEvents = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/events/`);
      setEvents(response.data);
    } catch (err) {
      setError(err);
    }
  }, []);

  const fetchUserConfig = useCallback(async () => {
    try {
      const response = await axios.get(`${API_URL}/users/${USER_ID}`);
      setUserConfig(response.data);
    } catch (err) {
      setError(err);
    }
  }, []);

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

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await fetchEvents();
      await fetchUserConfig();
      setLoading(false);
    };
    loadData();
  }, [fetchEvents, fetchUserConfig]);

  const handleAddEvent = async (eventData) => {
    try {
      await axios.post(`${API_URL}/users/${USER_ID}/events/`, eventData);
      fetchEvents();
    } catch (err) {
      setError(err);
    }
  };

  const handleUpdateEvent = async (id, eventData) => {
    try {
      await axios.put(`${API_URL}/events/${id}`, eventData);
      fetchEvents();
    } catch (err) {
      setError(err);
    }
  };

  const handleDeleteEvent = async (id) => {
    try {
      await axios.delete(`${API_URL}/events/${id}`);
      fetchEvents();
    } catch (err) {
      setError(err);
    }
  };

  const handleUpdateUserConfig = async (configData) => {
    try {
      await axios.put(`${API_URL}/users/${USER_ID}`, configData);
      fetchUserConfig();
    } catch (err) {
      setError(err);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

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
      <div className="content">
        <EventForm onSubmit={handleAddEvent} />
        <EventList
          events={events}
          onEdit={handleUpdateEvent}
          onDelete={handleDeleteEvent}
        />
        {userConfig && (
          <UserConfigForm
            onSubmit={handleUpdateUserConfig}
            initialConfig={userConfig}
          />
        )}
      </div>
    </div>
  );
}

export default App;