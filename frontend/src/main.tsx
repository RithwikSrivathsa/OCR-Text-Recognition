import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Camera, Download, RefreshCw, ShieldCheck } from "lucide-react";
import { exportExcel, getEvents, getStatus, statusStream } from "./lib/api";
import type { LiveStatus, TankerEvent } from "./types/api";
import "./styles.css";

function App() {
  const [status, setStatus] = useState<LiveStatus | null>(null);
  const [events, setEvents] = useState<TankerEvent[]>([]);

  useEffect(() => {
    getStatus().then(setStatus);
    getEvents().then(setEvents);
    const stream = statusStream(setStatus);
    const interval = window.setInterval(() => getEvents().then(setEvents), 5000);
    return () => {
      stream.close();
      window.clearInterval(interval);
    };
  }, []);

  const active = status?.active_tankers ?? [];

  return (
    <main className="app">
      <header className="topbar">
        <div>
          <h1>Water Tanker Monitor</h1>
          <p>{status?.camera.site_name ?? "Loading site"}</p>
        </div>
        <button className="iconButton" onClick={() => getEvents().then(setEvents)} title="Refresh events">
          <RefreshCw size={18} />
        </button>
      </header>

      <section className="statusGrid">
        <Metric icon={<Camera />} label="Camera" value={status?.camera.connected ? "Connected" : "Offline"} tone={status?.camera.connected ? "good" : "bad"} />
        <Metric icon={<ShieldCheck />} label="Active tankers" value={String(active.length)} />
        <Metric label="Last frame" value={status?.camera.last_frame_at ? new Date(status.camera.last_frame_at).toLocaleString() : "No frame"} />
        <Metric label="Updated" value={status?.updated_at ? new Date(status.updated_at).toLocaleTimeString() : "-"} />
      </section>

      <section className="workArea">
        <div className="panel">
          <div className="panelHeader">
            <h2>Current Tankers</h2>
          </div>
          <div className="list">
            {active.length === 0 ? <div className="empty">No active tanker tracks</div> : active.map((track) => (
              <div className="row" key={track.track_id}>
                <strong>{track.track_id}</strong>
                <span>{Math.round(track.confidence * 100)}%</span>
                <span>{track.bbox.join(", ")}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="panel">
          <div className="panelHeader">
            <h2>Configuration</h2>
          </div>
          <div className="configGrid">
            <label>Camera ID<input readOnly value={status?.camera.camera_id ?? ""} /></label>
            <label>Camera Name<input readOnly value={status?.camera.camera_name ?? ""} /></label>
            <label>Connection<input readOnly value={status?.camera.connected ? "Healthy" : status?.camera.last_error || "Disabled"} /></label>
            <label>Site<input readOnly value={status?.camera.site_name ?? ""} /></label>
          </div>
        </div>
      </section>

      <section className="panel history">
        <div className="panelHeader">
          <h2>Historical Events</h2>
          <button className="textButton" onClick={exportExcel}><Download size={16} />Excel</button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Track</th><th>State</th><th>Entry</th><th>Exit</th><th>Duration</th><th>Kannada</th><th>English</th><th>OCR</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event) => (
              <tr key={event.id}>
                <td>{event.tracker_id}</td>
                <td>{event.state}</td>
                <td>{fmt(event.entry_time)}</td>
                <td>{fmt(event.exit_time)}</td>
                <td>{event.duration_seconds ? `${Math.round(event.duration_seconds)}s` : "-"}</td>
                <td>{event.text_kn || "-"}</td>
                <td>{event.text_en || "-"}</td>
                <td>{event.ocr_confidence ? event.ocr_confidence.toFixed(2) : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

function Metric({ icon, label, value, tone }: { icon?: React.ReactNode; label: string; value: string; tone?: "good" | "bad" }) {
  return <div className={`metric ${tone ?? ""}`}>{icon}<span>{label}</span><strong>{value}</strong></div>;
}

function fmt(value: string | null) {
  return value ? new Date(value).toLocaleString() : "-";
}

createRoot(document.getElementById("root")!).render(<App />);

