'use strict';

const label = document.querySelector('#freshness-label');
const panel = document.querySelector('.freshness');
const publication = document.querySelector('#published').textContent;
let snapshot = null;

function updateFreshness() {
  const now = Date.now();
  const clocks = [snapshot?.published_at, snapshot?.source?.observed_at];
  const stale = !snapshot || snapshot.schema_version !== 1 || snapshot.source?.fetch_status !== 'ok' ||
    !/^[0-9a-f]{40}$/.test(snapshot.source?.revision ?? '') ||
    snapshot.published_at !== publication || clocks.some(clock => {
      const value = Date.parse(clock);
      return typeof clock !== 'string' || !/(Z|[+-]\d{2}:\d{2})$/.test(clock) || !Number.isFinite(value) || now - value > 2700000 || value - now > 120000;
    });
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
  const clock = typeof next === 'string' ? Date.parse(next) : NaN;
  const age = Date.now() - clock;
  const pageClock = Date.parse(publication);
  const pageClockValid = /(Z|[+-]\d{2}:\d{2})$/.test(publication) &&
    Number.isFinite(pageClock) && Date.now() - pageClock >= -120000;
  if (snapshot?.schema_version === 1 && (!pageClockValid || clock > pageClock) &&
      typeof next === 'string' && /(Z|[+-]\d{2}:\d{2})$/.test(next) &&
      Number.isFinite(clock) && age >= -120000 && age <= 2700000 &&
      ['ok', 'unavailable'].includes(snapshot.source?.fetch_status)) {
    try {
      const attemptedClock = Date.parse(sessionStorage.getItem('intent-mc-reload-publication') ?? '');
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
