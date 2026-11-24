# Smart Campus Practice #12

Compare code-based and low-code style solutions for one fictional room availability checker.

## User story
As a student, I want to check whether Room 204 is free for a future start time and a duration, so I can pick a valid study slot.

## Inputs / outputs
- Inputs: start time, duration (minutes), blocked flag, fictional bookings
- Outputs: availability boolean, reason code, visible message

## Run locally
```bash
npm ci
npm test
npm run dev
```

- Code app: `/code/`
- Low-code simulation: `/lowcode/`

## Tests
Eight shared cases T1–T8 in `code/booking.test.js`.

## Note on low-code
The `lowcode/` app is an Appsmith-like free simulation (visual widgets + expression pane). It uses the same deterministic rules. It is labeled as a simulation because no paid Appsmith/Power Apps subscription was used.
