> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 050-DR-STND — Program governance cadence and RACI ownership matrix

> **What this is and why it matters.** A platform stays healthy only if certain things happen on
> a rhythm — backups get validated, dependencies get patched, the disaster-recovery drill
> actually runs, the roadmap gets re-checked against reality. A regular cadence and
> ownership matrix say, for each activity, who is Responsible, Accountable, Consulted, and
> Informed. It is deliberately sized for a solo operator plus AI agents — light enough to
> actually run.

- **Program:** Mission Control (constitution: `038-AT-DECR`)
- **Companions:** `043` (the KPIs these reviews check), `041`/`045` (risks), `039` (doc law)

---

## 1. The governance calendar

Each activity names what happens, why, and where its output goes. "Agent-run" means an AI agent
can execute it unattended and surface only exceptions; "Jeremy" means it needs his judgement.

### Weekly

| Activity | Purpose | Runner | Output |
|---|---|---|---|
| Backup-success check | confirm every scheduled backup ran and verified | agent-run | exception → Slack; KPI `043` |
| Automation-registry reconcile | catch orphaned/ghost automations (already automated) | agent-run | drift → two-strikes → bead |
| Mission-control page regen | keep the generated status pages fresh (kills the stale-page failure) | agent-run | `pnpm mc` |
| Roadmap glance | is in-flight work still on the critical path? | Jeremy (5 min) | re-order if needed |

### Monthly

| Activity | Purpose | Runner | Output |
|---|---|---|---|
| Restore drill | prove data restores (not just that backups exist) | agent-run + review | transcript; KPI `043` |
[Operational detail retained in the private record]
| KPI review | read the reliability/backup/delivery/coverage KPIs; note trends | Jeremy | debt-trend beads |
| Documentation freshness | any capability whose doc drifted from reality? | agent-run | fix beads |

### Quarterly

| Activity | Purpose | Runner | Output |
|---|---|---|---|
| **Disaster-recovery game-day** | rebuild-from-nothing, measure RTO | Jeremy + agent | RTO record; `037` Epic 1.3 |
| Architecture review | is the layering (`046`) still true? new coupling/drift? | Jeremy | ADR or bead |
| Risk-register + heat-map review | retire/add risks, refresh owners and review dates | Jeremy | `041`/`045` update |
| Security review | secrets rotation status, access audit, attack-surface changes | Jeremy | security beads |
| Bus-factor check | can a second person still recover the estate? | Jeremy + [the CTO] | `037` Epic 1.11 |

### Annual

| Activity | Purpose | Runner | Output |
|---|---|---|---|
| ADR review | walk the ADR index (`047`); retire stale decisions | Jeremy | supersede records |
| Glossary + non-goals review | keep the vocabulary and scope honest | Jeremy | amendments |
| KPI-target ratchet | raise floors that have been met all year | Jeremy | `043` targets |
| Governance-calendar review | is this cadence still right-sized? | Jeremy | amend this doc |

## 2. RACI ownership matrix

**R**esponsible (does it) · **A**ccountable (owns the outcome, one per row) · **C**onsulted
(input) · **I**nformed (kept in the loop). At today's scale the roles are Jeremy (principal),
[the CTO] (CTO/DevOps), and the AI agents; the matrix scales to real roles as the team grows.

| Area | Jeremy | [the CTO] | AI agents | Notes |
|---|---|---|---|---|
| Program direction / roadmap approval | A/R | C | I | the exit-gate authority |
| Architecture decisions (ADRs) | A | R/C | C | Jeremy accountable, [the CTO] proposes |
| Deploys | A | R | R | agents deploy under CI; [the CTO] owns prod |
| Backups + DR | A | R | R | agents run drills; [the CTO] owns recovery |
| Monitoring + incidents | A | R | R | agents detect + open incidents |
| Security + secrets | A | R | I | Jeremy accountable for secret decisions |
| Documentation + AARs | A | C | R | agents draft; Jeremy accountable for truth |
| Dependency / CVE patching | A | R | R | agents scan + propose; [the CTO] applies |
| Governance cadence execution | A | C | R | agents run the scheduled reviews |
| Brain / knowledge governance | A | C | R | the no-comp/no-PII rule is Jeremy's line |
[Operational detail retained in the private record]
| Repositories | A | R | R | agents open PRs; [the CTO] owns merge posture |
| Services (the running apps) | A | R | R | per-service owner assigned at ADR-000 §7 sign-up |
| Runbooks | A | C | R | agents draft; [the CTO] validates operability |
| Incident response | A | R | R | [the CTO] is incident commander; agents detect + open |
| AI agents | A | C | R | Jeremy owns the governance line; agents self-report |

**Per-capability ownership (roadmap Epic 1.18):** the rows above are the *area* owners; every
**critical capability** additionally names one owner at its ADR-000 §7 contract sign-up (recorded
in the service registry, `037` Epic 2.9). RACI is the default; **DACI** (Driver / Approver /
Contributor / Informed) is used instead where a single *decider* matters more than a single
*accountable* — e.g. an irreversible one-way-door decision.

## 3. Governance of the governance

- Every recurring activity above becomes a scheduled automation as it is built; each gets its
  **automations registry row** before its session ends (the enforced rule), and its owner in this
  matrix.
- A review that produces no output for two cycles is either working (say so) or being skipped
  (fix it) — silence is not success.
- This document is itself on the annual "governance-calendar review" line — the cadence is
  allowed to change, but only deliberately.
- **These recurring reviews are owned by Phase X — Continuous Improvement** (`037` §6b), the
  standing operational phase that begins after Phase 3. Until then, the cadence runs as soon as
  each item's implementing epic lands (roadmap Epic 1.17 wires them into scheduled jobs).
