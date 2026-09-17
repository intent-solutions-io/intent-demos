> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 043-DR-STND — Mission Control success metrics and KPIs

> **What this is and why it matters.** A roadmap says what will be built; this says **how we
> know it worked.** It defines the key performance indicators (KPIs) for the Mission Control
> platform — the numbers that tell leadership whether the estate is healthy and whether the
> program is making the estate healthier over time. Each metric has a plain-English
> definition, how it is measured, a target, and where it will come from once the service-shape
> work (`037` Epic 1.4) exists. Until then, several are measured by hand; the metric exists now
> so the data model is built to serve it, not retrofitted. This is also the seed list for the
> future executive dashboard.

- **Program:** Mission Control (constitution: `038-AT-DECR`)
- **Status:** the KPI catalog; targets are the panel's proposal, subject to Jeremy's sign-off
- **Feeds:** the executive dashboard (`037` Phase 3), the ADR-000 §7 integration contract,
  the AAR verification section (`039`)

---

## 1. How to read this

Every metric has: a **definition** (what it counts), a **source** (where the number comes
from — "manual" means no automated feed exists yet), a **target** (the value that counts as
[Operational detail retained in the private record]

## 2. Reliability KPIs

| KPI | Definition | Source | Target | Cadence |
|---|---|---|---|---|
| **Platform availability** | % of time each customer-facing domain serves a healthy response | uptime probes per stack (`037` Epic 1.13); Netdata | ≥ 99.5% / domain / month | monthly |
| **Mean time to detect (MTTD)** | median minutes from a failure occurring to an alert firing | alert-history NDJSON (`037` Epic 1.4) vs incident open | ≤ 15 min (≤ 5 min for customer-facing down) | monthly |
| **Mean time to recover (MTTR)** | median minutes from alert to service restored | incident record open→resolved timestamps | ≤ 60 min for a single-stack outage | monthly |
| **Incident response time** | median minutes from alert to human acknowledgement | incident record open→ack | ≤ 30 min waking hours | monthly |

## 3. Backup and disaster-recovery KPIs

| KPI | Definition | Source | Target | Cadence |
|---|---|---|---|---|
| **Backup success rate** | % of scheduled backup runs that complete and verify | borg/backup logs + health monitor (`037` Epic 1.1) | 100% (any miss pages) | weekly |
| **Restore success rate** | % of restore drills that fully recover and pass an integrity/query check | monthly drill transcripts | 100% | monthly |
| **Recovery-drill success %** | % of scheduled DR game-days that hit their RTO target | quarterly DR exercise (`037` Epic 1.3) | 100%, RTO within target | quarterly |
| **Recovery point (RPO), per stack** | max data-age lost in a worst-case restore | per-stack backup frequency (`037` J8) | stated per stack; ≤ 24h default | quarterly |
| **Recovery time (RTO)** | measured wall-clock to rebuild-from-nothing | DR game-day stopwatch | a stated, decreasing number | quarterly |

## 4. Delivery KPIs

| KPI | Definition | Source | Target | Cadence |
|---|---|---|---|---|
| **Deployment success %** | % of deploys that pass smoke without manual intervention | deploy-workflow results | ≥ 95% | monthly |
| **Rollback success %** | % of failed deploys that auto-revert cleanly | deploy wrapper (`037` Epic 1.6) | 100% | monthly |

## 5. Coverage KPIs (the platform's own maturity)

| KPI | Definition | Source | Target | Cadence |
|---|---|---|---|---|
| **Documentation coverage** | % of live capabilities with a current operating doc + rollback note | doc audit vs capability list | 100% of production capabilities | quarterly |
| **Automation coverage** | % of registered automations that are observed (liveness + failure alert) | automations registry vs liveness sweep | 100% | monthly |
| **Service coverage** | % of estate services present in the canonical Service catalog | Service entity (`037` Epic 1.4) vs `docker ps` | 100% | monthly |

## 6. Trend KPIs (direction, not a single number)

| KPI | Definition | Source | Target | Cadence |
|---|---|---|---|---|
| **Technical debt trend** | count of open technical-debt beads, weighted by severity, over time | beads labelled `tech-debt` | flat or falling | monthly |
| **Operational debt trend** | count of open operational-gap beads (unobserved jobs, stale docs, manual toil) | beads labelled `ops-debt` | flat or falling | monthly |

## 6b. Composite scores (added 2026-07-11 — roadmap Epic 1.14)

Three roll-up scores compress the tables above into single numbers leadership can track over
time. Each is a weighted 0–100 computed from KPIs already defined here — they add no new data
source, only a formula. They are computed by the metrics-collection epic (`037` Epic 1.14).

| Score | Rolls up | Target |
|---|---|---|
| **Reliability score** | platform availability, MTTD, MTTR, deployment + rollback success, backup + restore success | ≥ 90 and rising |
| **Documentation score** | documentation coverage, doc-freshness (no page past its SLA), % capabilities with a rollback note + AAR | ≥ 90 |
| **Platform-maturity score** | service-ability coverage (how many capabilities expose an API/schema), automation + service coverage, % capabilities meeting the ADR-000 §7 contract | rising each quarter |

The **platform-maturity score** is the program's headline number: it measures how far the
estate has moved from "bash + cron + markers" to "service-shaped platform," and is the metric
Phase X (continuous improvement) tracks as the maturity assessment.

## 7. The executive-dashboard metric set

The future portal's leadership view renders, at minimum: platform availability (per domain and
rolled up), the most recent backup + restore-drill status with dates, open incidents by
severity, deployment success % this month, documentation/automation/service coverage, and the
two debt trends. Every one of these is defined above, so the dashboard is a rendering of this
catalog — not a new specification.

## 8. Governance

- These KPIs are reviewed on their stated cadences per the governance calendar (`050`).
- A KPI without a data source is a **Phase-1 signal**: build the source (usually a schema in
  `037` Epic 1.4) rather than dropping the metric.
- Targets ratchet: when a target is met three review periods running, propose the next floor.
- New capabilities add their KPI here as part of their ADR-000 §7 contract sign-up.
