import { checkAvailability, formatMinutes, toMinutes } from '../shared/booking.js';
import { NOW, bookings as sourceBookings } from '../shared/fixtures.js';

const bookings = sourceBookings.map((b) => ({ ...b }));
const list = document.getElementById('bookings');
const form = document.getElementById('check-form');
const error = document.getElementById('error');
const result = document.getElementById('result');
const reasonEl = document.getElementById('reason');

function renderBookings() {
  list.innerHTML = bookings
    .map((b) => `<li>${formatMinutes(b.start)}–${formatMinutes(b.end)}</li>`)
    .join('');
}

function renderClock() {
  document.getElementById('now').textContent = formatMinutes(NOW);
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  error.textContent = '';
  result.textContent = '';
  result.className = 'result';
  reasonEl.textContent = '';

  const startValue = document.getElementById('start').value;
  const durationRaw = document.getElementById('duration').value;
  if (!startValue || durationRaw === '') {
    error.textContent = 'Please enter both a start time and a duration.';
    return;
  }

  const duration = Number(durationRaw);
  const before = JSON.stringify(bookings);
  const decision = checkAvailability({
    start: toMinutes(startValue),
    duration,
    now: NOW,
    blocked: document.getElementById('blocked').checked,
    bookings,
  });

  if (JSON.stringify(bookings) !== before) {
    error.textContent = 'Booking data changed unexpectedly.';
    return;
  }

  result.textContent = decision.available ? 'Available' : 'Unavailable';
  result.classList.add(decision.available ? 'ok' : 'no');
  reasonEl.textContent = `${decision.reason}: ${decision.message}`;
  renderBookings();
});

renderClock();
renderBookings();
