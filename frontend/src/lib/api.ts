import type { LiveStatus, TankerEvent } from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function getStatus(): Promise<LiveStatus> {
  const res = await fetch(`${API_BASE_URL}/status`);
  return res.json();
}

export async function getEvents(): Promise<TankerEvent[]> {
  const res = await fetch(`${API_BASE_URL}/events`);
  return res.json();
}

export function statusStream(onMessage: (status: LiveStatus) => void): EventSource {
  const source = new EventSource(`${API_BASE_URL}/status/stream`);
  source.onmessage = (event) => onMessage(JSON.parse(event.data));
  return source;
}

export async function exportExcel(): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/exports/excel`, { method: "POST" });
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "tanker_events.xlsx";
  a.click();
  URL.revokeObjectURL(url);
}

