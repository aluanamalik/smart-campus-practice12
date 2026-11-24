# AGENTS.md — Practice #12 Smart Campus

## Project
Compare a code-based and a low-code style Smart Campus room checker.
One fictional room (Room 204). Fixed time 09:00. One booking 10:00–11:00.
No login, no database, no real personal data, no paid subscriptions.

## Acceptance criteria
- AC1: start time must be in the future
- AC2: duration > 0 and <= 120 minutes
- AC3: overlap is unavailable
- AC4: blocked room is unavailable
- AC5: clear decision; do not change existing bookings
- AC6: invalid input gets a clear message

## Structure
- `shared/booking.js` — pure rule `checkAvailability`
- `shared/fixtures.js` — NOW and bookings
- `code/` — code-based UI + Vitest
- `lowcode/` — Appsmith-like free simulation UI
- `index.html` — landing page with both links

## Safe commands
- `npm ci`
- `npm test`
- `npm run build`
- `npm run dev`

## Rules
- Do not invent test results.
- Do not deploy secrets.
- Human reviews the diff before merge.
- Low-code folder is a labeled simulation when a free cloud builder account is not used.
