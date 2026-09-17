# Mission Control public reporting and recovery

## Incident and boundary

On September 17, 2026 at 19:37 UTC, the public URL returned HTTP200 but Last-Modified
was July 11. Its copy button, embedded payload, agent index, feed and “current” link all
described the original design-only snapshot. The served directory's README explicitly
said “no cron”: publishing required manually running two unmanaged scripts. The newer
catalog deployment intentionally preserved that independent directory, so deploying
the catalog never refreshed Mission Control. This was a publishing/lifecycle failure;
the successful HTTP probe did not detect it.

This surface is public reporting, not the private operational console. It publishes
only reviewed component labels with source-presence states, revision and successful
observation clocks, plus checks of three already-public website endpoints. It never
publishes arbitrary private documents, issue titles, operational topology or secrets.
Source presence proves implementation is in main, not deployment or phase completion.
Website checks prove single-location endpoint reachability, not functional/game-data
freshness, worldwide availability or internal dependency readiness.

Historical public copies have explicit redaction annotations; operational posture,
credential locations and private topology are retained only in the original private backup.

## Reconciliation and freshness

The immutable installed publisher runs every15minutes. It fetches main into a dedicated
bare source cache, queries only the fixed component path allowlist, and probes the public
endpoints with timeouts. A failed source fetch retains the previous revision and successful
observation clock and publishes `unavailable`; it never restamps old source as current.
Publication and source observation older than45minutes are stale. Missing, malformed or
future timestamps and mismatched HTML/manifest revisions fail the outside-in check.
The browser checks the same45minute window and warns when the snapshot cannot be verified.
Old browser tabs are warned when a newly published manifest differs from their page.

Publication takes a kernel-released lock, builds and validates a complete release, then
atomically replaces the served symlink. An interrupted owned candidate is recoverable.
The most recent96releases are retained for rollback; the original directory is separately
preserved unchanged outside the public tree as `~/.local/state/intent-mc-public/legacy-feed`.
No recurring process-local timer owns the publisher: persistent systemd calendar timers
recover on reboot, and user lingering must be enabled and verified.

## Install and verification

Install only from a reviewed, merged, clean commit. Existing company Git credentials must
allow the dedicated cache to read the private source main; do not publish those credentials.

```bash
bash scripts/install_mission_control.sh publisher
loginctl show-user "$USER" -p Linger
systemctl --user list-timers intent-mc-public-publish.timer
python3 scripts/mission_control.py check
```

The installer extracts committed files into a revision-named private executable directory,
records the revision, verifies an artifact digest manifest, and installs a user timer. The
public releases remain under the existing Caddy-readable demos tree; private state stays
outside it. Later publisher/template changes require reinstalling the new reviewed commit.
Source main is fetched anew at each run, independently of local developer worktrees.

On the independent Buzz host, install the same verified packaged release with
`sudo bash scripts/install_public_monitors.sh`. This creates system-level services and
persistent timers: Mission Control outside-in every5minutes and Tons of Skills regional
HTTPS/content/TLS checks hourly, for both hostnames from eight countries. System units
survive reboot without relying on a user login. Jobs run as an unprivileged service user;
code is root-owned and digest-verified. The installer references the existing protected
company notifier environment, never prints it or copies it into the artifact.

Failures use the existing governed `sys-automation` transport. A bad sample returns1
only after accepted alert dispatch; transport or integrity errors return2 and trigger a
separate native execution-failure alert. Native timeouts likewise trigger failure alerting.
Missing country probes, Globalping outages and rate limits are unverified failures, not
proof of product outage. Regional checks cover cloud probes of the homepage, not every
ISP, browser or deep link. The routine16probes/hour are below the documented
250anonymous probes/hour limit (https://globalping.io/credits); other clients sharing
the monitoring host egress may consume that budget. Investigate the reported country/path/error independently.

```bash
systemctl status intent-mc-public-check.timer tonsofskills-regional.timer
sudo cat /var/lib/intent-mc-public-check/check.log
sudo cat /var/lib/tonsofskills-regional/regional.log
```

On the publishing host use its existing `~/bin/lib/alert-floor.sh` transport. The installer
does not invent a direct messaging fallback. Keep `/mission-control/*` responses under
Caddy `Cache-Control: no-store` so page, copy payload and agent snapshots are revalidated.
Back up and validate Caddy as its service user before reloading; preserve other sites.

## Diagnosis, recovery, rollback

```bash
systemctl --user status intent-mc-public-publish.service
cat ~/.local/state/intent-mc-public/publish.log
python3 scripts/mission_control.py check
```

Check source authentication/network failure first when fetch is unavailable; an old
source timestamp is expected, not something to renew manually. A failed build preserves
the served release. Fix the reported cause and start the publisher service to reconcile.
Unexpected deployment candidates are refused, while the publisher's owned interrupted
symlink is recoverable. Do not delete the original directory or clear a private Git cache
to disguise a stale source.

For rollback, stop the publisher timer, identify a verified prior directory in
`~/demos/.mission-control-releases/`, create a replacement symlink and atomically rename
it over `~/demos/mission-control`. Revert the executable `current` symlink to the prior
revision artifact if code caused the failure. Preserve alerting: a rollback snapshot may
properly be labeled stale until a repaired publisher runs. To restore the original July
feed instead, stop publication, move only the managed symlink aside and restore the
captured `legacy-feed` directory; that is recovery of historical output, not freshness.

## Tests

```bash
python3 -m unittest discover -s scripts -p 'test_mission_control.py' -v
python3 scripts/verify_site.py
python3 scripts/browser_smoke.py
# Independently published production MC, without asserting an unrelated catalog revision:
DEMOS_BASE_URL=https://demos.intentsolutions.io python3 scripts/browser_smoke.py --mission-control-only
```

The tests cover July HTTP200 stale output, bad/missing/future clocks, successful and failed
fetch clocks, private-text non-export, equivalent human/copy/machine artifacts, invalid
HTTP200 bodies, timeouts, migration, republish/restart, abandoned candidates and failed
build preservation. Browser smoke covers desktop/mobile layout and visible stale/unknown
states. Runtime receipts and deployment evidence live in the tracked incident bead.
