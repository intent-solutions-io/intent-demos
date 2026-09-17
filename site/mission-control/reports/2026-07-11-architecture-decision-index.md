> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 047-DR-INDEX — Architecture decision log index

> **What this is and why it matters.** Decisions get made, superseded, and forgotten. This is
> the **one index** of every architecture decision affecting Mission Control — what was decided,
> whether it still stands, when, who owned it, and what replaced it if anything. A reader who
> wants "the current rule on X" starts here and follows the pointer to the full record, rather
> than reading every document hoping to find the latest word. It spans two decision systems this
> repo already runs: the numbered **ADRs** in `000-docs/` (the `AT-DECR` records) and the
> append-only **decision-log/** chronicle (the `D##` entries).

- **Program:** Mission Control (constitution: `038-AT-DECR`)
- **Convention:** a decision is **Accepted** (in force), **Superseded** (replaced — see the
  successor), or **Proposed** (awaiting sign-off). Superseded decisions are never deleted.

---

## 1. Mission Control ADRs (the `AT-DECR` records)

| Decision | Record | Status | Date | Owner | Superseded by |
|---|---|---|---|---|---|
| ADR-000 — Intent OS is the Mission Control platform; platform-over-tools; API-first + platform-before-UI binding; the RBAC end-state; integration contract | `038-AT-DECR` | Accepted (binding on roadmap approval) | 2026-07-11 | Jeremy | — |
| Intendants — proactive-agent platform naming, home, Slice-0 supersession | `030-AT-DECR` | Accepted | 2026-07-10 | ISEDC + CEO | — |
| Unify the governed brain — one plugin, two modes | `014-AT-DECR` | Accepted | 2026-06 | Jeremy | — |
| Signed-dogfood publication — gated | `023-AT-DECR` | Accepted | 2026-07-05 | Acting CTO | — |

## 2. Program decisions in the append-only chronicle (`decision-log/`)

| Decision cluster | Record | Status | Date |
|---|---|---|---|
| ADR-000 adoption; ops-vs-conduct split; doc standard delivery-to-feed (D35–D38) | `decision-log/007` | Accepted | 2026-07-10 |
| Mission-control cockpit — the estate cockpit lands (D31–D34) | `decision-log/006` | Accepted | 2026-07-01 |
| Doc-filing disciplined nesting (D5-era) | `decision-log/005` | Accepted | 2026-06-19 |
| Brain readiness + CRO kill | `decision-log/004` | Accepted | 2026-06-18 |
| Foundation + notifications | `decision-log/003` | Accepted | 2026-06-13 |
| Brain-build decisions | `decision-log/002` | Accepted | 2026-06-13 |
| Session decisions (initial) | `decision-log/001` | Accepted | 2026-06-13 |

## 3. Decisions pending Jeremy (Proposed — the Phase-0 exit gate)

These are recorded so they are not lost; they become Accepted entries when Jeremy rules.

| Decision | Where argued | Status | Owner |
|---|---|---|---|
| Runbook merge (docs) + secrets federation | `034`, `037` J1/J1b | Proposed | Jeremy |
| Off-site destination + immutability mechanism | `037` J2, `041` R1 | Proposed | Jeremy |
| Per-stack RPO targets | `037` J8, `043` | Proposed | Jeremy |
[Operational detail retained in the private record]
| Governance ceremony tiering | `037` J13, `039` §7 | Proposed | Jeremy |
| Publish-the-feed posture | `037` J10, `040` C5 | Proposed (default-deny applied) | Jeremy |

## 4. Governance

- Every new `AT-DECR` record or `decision-log/` entry adds a row here in the same change — an
  ADR that isn't indexed is an ADR that will be forgotten.
- When a decision is superseded, set its status here and name the successor; do not delete the
  row (the history is the point).
- This index is reviewed on the annual ADR-review cadence (`050`) to catch decisions that have
  quietly gone stale.
