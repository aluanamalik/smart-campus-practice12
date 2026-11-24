import { checkAvailability, formatMinutes, toMinutes } from '../shared/booking.js';
import { NOW, bookings as sourceBookings } from '../shared/fixtures.js';

const bookings = sourceBookings.map((b) => ({ ...b }));

function render() {
  document.getElementById('now').textContent = formatMinutes(NOW);
  document.getElementById('bookings').innerHTML = bookings
    .map((b) => `<tr><td>${formatMinutes(b.start)}</td><td>${formatMinutes(b.end)}</td></tr>`)
    .join('');
}

document.getElementById('run').addEventListener('click', () => {
  const error = document.getElementById('error');
  const result = document.getElementById('result');
  const reason = document.getElementById('reason');
  error.textContent = '';
  result.textContent = '';
  result.className = 'result';
  reason.textContent = '';

  const startValue = document.getElementById('start').value;
  const durationRaw = document.getElementById('duration').value;
  if (!startValue || durationRaw === '') {
    error.textContent = 'Please enter both a start time and a duration.';
    return;
  }

  const before = JSON.stringify(bookings);
  const decision = checkAvailability({
    start: toMinutes(startValue),
    duration: Number(durationRaw),
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
  reason.textContent = `${decision.reason}: ${decision.message}`;
  render();
});

render();
