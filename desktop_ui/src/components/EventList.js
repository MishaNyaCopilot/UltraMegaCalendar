import React from 'react';

function EventList({ events, onEdit, onDelete }) {
  return (
    <div>
      <h2>Your Events</h2>
      {events.length === 0 ? (
        <p>No events found.</p>
      ) : (
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              <h3>{event.title}</h3>
              <p>Description: {event.description}</p>
              <p>Start: {new Date(event.start_time).toLocaleString()}</p>
              {event.end_time && <p>End: {new Date(event.end_time).toLocaleString()}</p>}
              {event.location && <p>Location: {event.location}</p>}
              <button onClick={() => onEdit(event.id)}>Edit</button>
              <button onClick={() => onDelete(event.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default EventList;
