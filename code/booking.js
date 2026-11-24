export {
  DAY_END,
  MAX_DURATION,
  toMinutes,
  formatMinutes,
  checkAvailability,
} from '../shared/booking.js';

import { checkAvailability } from '../shared/booking.js';

export function canBook({ start, end, now, blocked, bookings }) {
  if (![start, end, now].every(Number.isFinite)) return false;
  return checkAvailability({
    start,
    duration: end - start,
    now,
    blocked,
    bookings,
  }).available;
}
