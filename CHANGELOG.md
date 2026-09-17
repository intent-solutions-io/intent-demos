# Changelog

## 2026-09-17 — Restore current Mission Control public reporting

- Replace the unmanaged July 11 “current state” page with a timestamped public source
  inventory and recent endpoint checks. Preserve all 11 report URLs as explicitly
  historical documents, redact operational details, and retain originals privately; keep their existing URLs and the machine-readable feed routes.
- Read only approved component presence from the private repository's main revision.
  Never copy private report bodies, issue titles, topology, credentials, or personal data.
  Distinguish source implementation from deployment and endpoint reachability from
  functional freshness. A failed fetch keeps its original successful observation clock.
- Add bounded immutable publication, recurring systemd timers, outside-in timestamp and
  HTML/revision checks, governed failure alerting, browser stale-state detection, and
  regression tests for stale HTTP200 responses, failed builds, and restart recovery.
- Add bounded regional HTTPS/content/TLS diagnostics for both Tons of Skills hostnames.
  Missing country results and unavailable measurement infrastructure fail visibly; a
  successful cloud-probe sample does not claim every browser or ISP is healthy.

- Production verification added independent Mission Control browser scope while preserving
  unrelated live catalog additions. Regional diagnostic failures retain the country even
  when the probe returns null TLS/body fields; these never become successful samples.

- Native synthetic stale checks proved accepted alert delivery. Harden execution-failure
  services with a writable private temporary directory required by the governed notifier.
  Browser freshness also refuses timestamps without an explicit timezone.

- Refresh already-open reports when a newer valid publication arrives, with a per-publication
  reload guard and honest fallback warning. Browser replay verifies the page timestamp and
  copy payload advance together; ordinary publication no longer leaves an old tab frozen.

- Validate snapshot revisions and semantic zoned calendar timestamps before recording a
  browser refresh attempt. A malformed newer manifest cannot block its corrected revision.
