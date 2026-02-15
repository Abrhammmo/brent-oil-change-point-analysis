import { useEffect, useState } from "react";
import API from "../services/api";

const EventTimeline = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        const response = await API.get("/events");
        const payload = response.data;
        // normalize payload into an array
        const asArray = Array.isArray(payload)
          ? payload
          : Array.isArray(payload?.data)
          ? payload.data
          : Array.isArray(payload?.events)
          ? payload.events
          : payload
          ? [payload]
          : [];
        setEvents(asArray);
        setError(null);
      } catch (err) {
        console.error("Error fetching events:", err);
        setError("Failed to load events");
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  if (loading) {
    return (
      <div className="events-grid">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="skeleton" style={{ height: 80 }}></div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-state">
        <div className="error-icon">⚠️</div>
        <p>{error}</p>
      </div>
    );
  }

  if (!events || events.length === 0) {
    return (
      <div className="error-state">
        <div className="error-icon">📭</div>
        <p>No events found</p>
      </div>
    );
  }

  // Get unique events and limit to most relevant
  const uniqueEvents = events.reduce((acc, current) => {
    const existing = acc.find(item => item.title === current.title);
    if (!existing) {
      return acc.concat([current]);
    }
    return acc;
  }, []).slice(0, 12);

  const groupedByDecade = uniqueEvents.reduce((acc, event) => {
    const year = Number(String(event.date || "").slice(0, 4));
    if (Number.isNaN(year)) return acc;
    const decade = `${Math.floor(year / 10) * 10}s`;
    if (!acc[decade]) acc[decade] = [];
    acc[decade].push(event);
    return acc;
  }, {});

  const decadeOrder = Object.keys(groupedByDecade).sort();

  return (
    <div>
      {decadeOrder.map((decade) => (
        <div key={decade} style={{ marginBottom: 16 }}>
          <h4 style={{ marginBottom: 8 }}>{decade}</h4>
          <div className="events-grid">
            {groupedByDecade[decade].map((event, idx) => (
              <div
                key={`${decade}-${idx}`}
                className="event-card fade-in"
                style={{ animationDelay: `${idx * 0.05}s` }}
              >
                <div className="event-date">{event.date}</div>
                <div className="event-title">{event.title}</div>
                {event.description && (
                  <div className="event-description">{event.description}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default EventTimeline;
