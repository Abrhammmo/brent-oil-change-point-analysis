import { useState, useEffect } from "react";

const Filters = ({ onFilterChange, onEventSelect, events = [] }) => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showDatePicker, setShowDatePicker] = useState(false);

  useEffect(() => {
    // Set default date range (last 5 years)
    const now = new Date();
    const fiveYearsAgo = new Date(now.getFullYear() - 5, now.getMonth(), now.getDate());
    setStartDate(fiveYearsAgo.toISOString().split("T")[0]);
    setEndDate(now.toISOString().split("T")[0]);
  }, []);

  const handleApplyFilters = () => {
    onFilterChange({
      startDate: startDate || null,
      endDate: endDate || null
    });
  };

  const handleEventSelect = (event) => {
    const eventData = {
      date: event.date,
      title: event.title
    };
    setSelectedEvent(eventData);
    if (onEventSelect) {
      onEventSelect(eventData);
    }
  };

  const handleReset = () => {
    const now = new Date();
    const fiveYearsAgo = new Date(now.getFullYear() - 5, now.getMonth(), now.getDate());
    setStartDate(fiveYearsAgo.toISOString().split("T")[0]);
    setEndDate(now.toISOString().split("T")[0]);
    setSelectedEvent(null);
    onFilterChange({ startDate: null, endDate: null });
    if (onEventSelect) {
      onEventSelect(null);
    }
  };

  const quickRanges = [
    { label: "Last 1 Year", getValue: () => {
      const now = new Date();
      const yearAgo = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
      return { start: yearAgo.toISOString().split("T")[0], end: now.toISOString().split("T")[0] };
    }},
    { label: "Last 3 Years", getValue: () => {
      const now = new Date();
      const yearsAgo = new Date(now.getFullYear() - 3, now.getMonth(), now.getDate());
      return { start: yearsAgo.toISOString().split("T")[0], end: now.toISOString().split("T")[0] };
    }},
    { label: "Last 5 Years", getValue: () => {
      const now = new Date();
      const yearsAgo = new Date(now.getFullYear() - 5, now.getMonth(), now.getDate());
      return { start: yearsAgo.toISOString().split("T")[0], end: now.toISOString().split("T")[0] };
    }},
    { label: "Full Range", getValue: () => ({ start: "", end: "" })}
  ];

  return (
    <div className="card" style={{ marginBottom: 24 }}>
      <div className="card-header">
        <h3>🔍 Filters & Analysis</h3>
        <button 
          onClick={() => setShowDatePicker(!showDatePicker)}
          style={{
            background: showDatePicker ? '#1e3a5f' : 'transparent',
            color: showDatePicker ? 'white' : '#1e3a5f',
            border: '1px solid #1e3a5f',
            padding: '6px 12px',
            borderRadius: 6,
            cursor: 'pointer',
            fontSize: '0.85rem'
          }}
        >
          {showDatePicker ? 'Hide Filters' : 'Show Filters'}
        </button>
      </div>
      
      {showDatePicker && (
        <div className="card-body fade-in">
          {/* Quick Range Buttons */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
            {quickRanges.map((range, idx) => (
              <button
                key={idx}
                onClick={() => {
                  const { start, end } = range.getValue();
                  setStartDate(start);
                  setEndDate(end);
                }}
                style={{
                  background: '#f0f0f0',
                  border: 'none',
                  padding: '8px 16px',
                  borderRadius: 6,
                  cursor: 'pointer',
                  fontSize: '0.8rem',
                  transition: 'all 0.2s'
                }}
              >
                {range.label}
              </button>
            ))}
          </div>

          {/* Date Inputs */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: 16, marginBottom: 16 }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 500, marginBottom: 4 }}>
                Start Date
              </label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid #e9ecef',
                  borderRadius: 6,
                  fontSize: '0.9rem'
                }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 500, marginBottom: 4 }}>
                End Date
              </label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid #e9ecef',
                  borderRadius: 6,
                  fontSize: '0.9rem'
                }}
              />
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8 }}>
              <button
                onClick={handleApplyFilters}
                style={{
                  background: '#1e3a5f',
                  color: 'white',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: 6,
                  cursor: 'pointer',
                  fontWeight: 500
                }}
              >
                Apply
              </button>
              <button
                onClick={handleReset}
                style={{
                  background: 'transparent',
                  color: '#6c757d',
                  border: '1px solid #e9ecef',
                  padding: '10px 16px',
                  borderRadius: 6,
                  cursor: 'pointer'
                }}
              >
                Reset
              </button>
            </div>
          </div>

          {/* Event Selection */}
          {events.length > 0 && (
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 500, marginBottom: 8 }}>
                Highlight Event
              </label>
              <select
                value={selectedEvent?.date || ""}
                onChange={(e) => {
                  const event = events.find(ev => ev.date === e.target.value);
                  handleEventSelect(event || { date: e.target.value, title: "Custom Date" });
                }}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid #e9ecef',
                  borderRadius: 6,
                  fontSize: '0.9rem',
                  background: 'white'
                }}
              >
                <option value="">Select an event...</option>
                {events.map((event, idx) => (
                  <option key={idx} value={event.date}>
                    {event.date} - {event.title}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Selected Event Display */}
          {selectedEvent && (
            <div 
              style={{
                marginTop: 16,
                padding: 12,
                background: '#fff3cd',
                borderRadius: 6,
                border: '1px solid #ffc107'
              }}
            >
              <strong>📍 Selected Event:</strong> {selectedEvent.title} ({selectedEvent.date})
              <button
                onClick={() => {
                  setSelectedEvent(null);
                  if (onEventSelect) onEventSelect(null);
                }}
                style={{
                  float: 'right',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '1.2rem'
                }}
              >
                ×
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Filters;
