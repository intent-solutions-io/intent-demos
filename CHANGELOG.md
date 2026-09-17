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
