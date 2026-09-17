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
