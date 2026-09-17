'use strict';

const label = document.querySelector('#freshness-label');
const panel = document.querySelector('.freshness');
const publication = document.querySelector('#published').textContent;
let snapshot = null;

function parseClock(value) {
  if (typeof value !== 'string') return NaN;
  const fields = /^(\d{4})-(\d{2})-(\d{2})T([01]\d|2[0-3]):([0-5]\d):([0-5]\d)(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)$/.exec(value);
  if (!fields) return NaN;
  const year = Number(fields[1]);
  const month = Number(fields[2]);
  const day = Number(fields[3]);
  const leap = year % 4 === 0 && (year % 100 !== 0 || year % 400 === 0);
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  if (year < 1 || month < 1 || month > 12 || day < 1 || day > days[month - 1]) return NaN;
  return Date.parse(value);
}

function snapshotClocks(value) {
  if (value?.schema_version !== 1 || typeof value.source?.revision !== 'string' ||
      !/^[0-9a-f]{40}$/.test(value.source.revision)) return null;
  const clocks = [parseClock(value.published_at), parseClock(value.source?.observed_at)];
  return clocks.every(clock => Number.isFinite(clock) && clock - Date.now() <= 120000) ? clocks : null;
}

function updateFreshness() {
  const now = Date.now();
  const clocks = snapshotClocks(snapshot);
  const stale = !clocks || snapshot.source?.fetch_status !== 'ok' ||
    snapshot.published_at !== publication || clocks.some(clock => now - clock > 2700000);
  panel.dataset.state = stale ? 'stale' : 'fresh';
  label.textContent = stale ? 'Stale or unverified snapshot — check the timestamps below.' : 'Recent snapshot · refreshed automatically every 15 minutes';
}

async function loadFreshness() {
  try {
    const response = await fetch('/mission-control/manifest.json', {cache: 'no-store'});
    if (!response.ok) throw new Error('Snapshot unavailable');
    snapshot = await response.json();
  } catch (error) {
    snapshot = null;
  }
  // An ordinary new publication should update an already-open report rather
  // than look like a stalled pipeline. Attempt at most one reload per revision.
  const next = snapshot?.published_at;
  const clocks = snapshotClocks(snapshot);
  const clock = clocks?.[0] ?? NaN;
  const age = Date.now() - clock;
  const pageClock = parseClock(publication);
  const pageClockValid = Number.isFinite(pageClock) && Date.now() - pageClock >= -120000;
  if (clocks && (!pageClockValid || clock > pageClock) && age <= 2700000 &&
      ['ok', 'unavailable'].includes(snapshot.source?.fetch_status)) {
    try {
      const attemptedClock = parseClock(sessionStorage.getItem('intent-mc-reload-publication'));
      if (!Number.isFinite(attemptedClock) || clock > attemptedClock) {
        sessionStorage.setItem('intent-mc-reload-publication', next);
        window.location.reload();
        return;
      }
    } catch (error) {
      snapshot = null; // Storage unavailable: retain the honest unverified label.
    }
  }
  updateFreshness();
}

document.querySelector('#copy-current').addEventListener('click', async () => {
  const digest = document.querySelector('#digest');
  try {
    await navigator.clipboard.writeText(digest.value);
    document.querySelector('#copy-result').textContent = 'Copied the dated snapshot.';
  } catch (error) {
    digest.hidden = false;
    digest.focus();
    digest.select();
    document.querySelector('#copy-result').textContent = 'Select and copy the snapshot below.';
  }
});

loadFreshness();
setInterval(loadFreshness, 60000);
