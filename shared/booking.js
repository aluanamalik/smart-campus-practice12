export const DAY_END = 1440;
export const MAX_DURATION = 120;

export function toMinutes(value) {
  if (typeof value !== 'string' || !/^\d{2}:\d{2}$/.test(value)) return NaN;
  const [h, m] = value.split(':').map(Number);
  if (h > 23 || m > 59) return NaN;
  return h * 60 + m;
}

export function formatMinutes(min) {
  if (!Number.isFinite(min)) return '--:--';
  const h = String(Math.floor(min / 60)).padStart(2, '0');
  const m = String(min % 60).padStart(2, '0');
  return `${h}:${m}`;
}

export function checkAvailability({ start, duration, now, blocked, bookings }) {
  const result = (available, reason, message) => ({ available, reason, message });

  if (!Number.isFinite(start) || !Number.isFinite(duration) || !Number.isFinite(now)) {
    return result(false, 'INVALID_INPUT', 'Enter a valid start time and duration.');
  }
  if (!Array.isArray(bookings)) {
    return result(false, 'INVALID_INPUT', 'Booking list is missing.');
  }
  if (start <= now) {
    return result(false, 'PAST_START', 'Start time must be in the future.');
  }
  if (!(duration > 0 && duration <= MAX_DURATION)) {
    return result(false, 'BAD_DURATION', 'Duration must be greater than 0 and at most 120 minutes.');
  }

  const end = start + duration;
  if (end > DAY_END) {
    return result(false, 'PAST_DAY_END', 'The requested interval goes past 24:00.');
  }
  if (blocked) {
    return result(false, 'BLOCKED', 'Room is blocked.');
  }
  if (bookings.some((b) => start < b.end && end > b.start)) {
    return result(false, 'OVERLAP', 'Requested time overlaps an existing booking.');
  }
  return result(true, 'OK', 'Available');
}
