// Helpers to convert between ISO datetimes (what the API uses) and the value an
// <input type="datetime-local"> expects ("YYYY-MM-DDTHH:mm" in local time).

function pad(n: number): string {
  return String(n).padStart(2, "0");
}

export function toDatetimeLocalValue(iso?: string): string {
  const d = iso ? new Date(iso) : new Date();
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export function datetimeLocalToISO(local: string): string {
  return new Date(local).toISOString();
}

export function formatDateTime(iso: string): string {
  return new Date(iso).toLocaleString();
}
