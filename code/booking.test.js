import { readFileSync } from 'node:fs';
import { describe, test, expect } from 'vitest';
import { checkAvailability, toMinutes } from '../shared/booking.js';
import { NOW, bookings as fixtureBookings } from '../shared/fixtures.js';

function run(start, duration, overrides = {}) {
  const bookings = fixtureBookings.map((b) => ({ ...b }));
  const before = structuredClone(bookings);
  const decision = checkAvailability({
    start,
    duration,
    now: NOW,
    blocked: false,
    bookings,
    ...overrides,
  });
  expect(bookings).toEqual(before);
  return decision;
}

describe('Practice 12 identical cases T1–T8', () => {
  test('T1 valid free interval -> Available', () => {
    const d = run(660, 60);
    expect(d.available).toBe(true);
    expect(d.reason).toBe('OK');
  });

  test('T2 overlap -> Unavailable', () => {
    const d = run(630, 60);
    expect(d.available).toBe(false);
    expect(d.reason).toBe('OVERLAP');
  });

  test('T3 blocked room -> Unavailable', () => {
    const d = run(660, 60, { blocked: true });
    expect(d.available).toBe(false);
    expect(d.reason).toBe('BLOCKED');
  });

  test('T4 duration = 0 -> validation error', () => {
    const d = run(660, 0);
    expect(d.available).toBe(false);
    expect(d.reason).toBe('BAD_DURATION');
  });

  test('T5 duration = 121 -> validation error', () => {
    const d = run(660, 121);
    expect(d.available).toBe(false);
    expect(d.reason).toBe('BAD_DURATION');
  });

  test('T6 past start -> validation error', () => {
    const d = run(480, 30);
    expect(d.available).toBe(false);
    expect(d.reason).toBe('PAST_START');
  });

  test('T7 adjacent non-overlapping -> Available', () => {
    const d = run(570, 30);
    expect(d.available).toBe(true);
    expect(d.reason).toBe('OK');
  });

  test('T8 booking data unchanged after checks', () => {
    const bookings = fixtureBookings.map((b) => ({ ...b }));
    const snapshot = structuredClone(bookings);
    for (const args of [
      { start: 660, duration: 60 },
      { start: 630, duration: 60 },
      { start: 660, duration: 0 },
      { start: 480, duration: 30, blocked: true },
    ]) {
      checkAvailability({ now: NOW, blocked: false, bookings, ...args });
    }
    expect(bookings).toEqual(snapshot);
  });
});

describe('helpers', () => {
  test('toMinutes rejects impossible clock values', () => {
    expect(toMinutes('09:00')).toBe(540);
    expect(toMinutes('09:60')).toBeNaN();
    expect(toMinutes('24:00')).toBeNaN();
  });

  test('fixtures stay shared', () => {
    const app = readFileSync(new URL('./app.js', import.meta.url), 'utf8');
    expect(NOW).toBe(540);
    expect(fixtureBookings).toEqual([{ start: 600, end: 660 }]);
    expect(app).toContain("from '../shared/fixtures.js'");
  });
});

