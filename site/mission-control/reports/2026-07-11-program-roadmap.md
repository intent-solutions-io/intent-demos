> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 037-PP-PLAN — Mission Control program roadmap (post-audit revision)

> **What this is and why it matters.** This is the implementation roadmap for turning Intent
> OS into the Mission Control platform. It is the **post-audit revision** — a first draft was
> deliberately put through a ten-agent adversarial audit (`040-AA-AUDR`), scored 6/10, and
> rewritten around what the audit found. The draft's fatal flaw, in the panel's words, was
> being "well-argued essays, not an executable plan": it under-specified its two load-bearing
> moves (off-site backup, the runbook merge) in exactly the ways they fail under real
> conditions, silently dropped two catastrophic single points of failure its own discovery
> had ranked, and shipped with no measurable exit criteria. This version reframes the whole
> program **from "observe the estate" to "harden the estate,"** carves the one
> irreversible-loss fix out as a hotfix that ships before roadmap sign-off, gives every epic a
> one-line acceptance test, and answers the audit's structural findings. Phases 1–3 beads are
> cut only after Jeremy approves this document (the Phase-0 exit gate).

- **Program:** Mission Control (constitution: `038-AT-DECR` / ADR-000)
- **Status:** the filed post-audit revision; supersedes the pre-audit draft (`ws6-roadmap-draft`, not filed). **Rev. 2026-07-11 (CTO pass):** Jeremy proposed Phase-1 ops epics (1.14–1.18), Phase-2 platformization (2.6–2.15) forward, and a standing **Phase X**. CTO ruling applied same day — 1.14/1.17/1.18 kept as real work, **1.15 downgraded to a review norm** (gate deferred behind a contributor-count trigger), **1.16** confirmed largely-delivered; of the 10 Phase-2 platform epics only 2.13 + 2.6 were first kept committed. **Rev. 2026-07-11 (glory build — Jeremy's principal call, `decision-log/009`, supersedes the DL-008 D41 trim):** *"we build for glory"* — **all ten platform epics committed** (full data model, full API fleet, event bus, registries, asset graph, search, reporting engine, plugin architecture) **+ tracing (2.16) + central logs (2.3) promoted + a full RBAC portal** (3.6 roles, 3.7 fan-out, 3.8 cost dashboards, 3.9 compliance un-deferred). CTO keeps the *build order* (producer-driven model, contract-first API, hardening-floor-first) as competence, and states the **true bill** in new §9b (dedicated capacity + a second box + floor-first). Phase X adopted. Rationale: `decision-log/008` + `009`. **Rev. 2026-07-11 (Phase 2.5 inserted, `decision-log/010`):** a **Platform Technology Selection & Reference Architecture** phase (§5b, epics 2.5.1–2.5.12) inserted between Phase 2 and Phase 3 as the *final gate before implementation* — every technology (auth, authz, workflow, event bus, search, notifications, reporting, storage, AI agents, portal framework) is formally evaluated (multi-candidate, scored, ADR + rejected-alternatives) before any Phase-3 epic hard-codes it; prefer self-hostable OSS. Inserted as a decimal (no renumber). Dependency graph + Phase-3 gate updated.
- **Inputs:** `033`–`036` (discovery), `040` (adversarial audit), `041` (risk register),
  `031-AA-AACR` (2026-07-10 remediation ground truth), `002-AA-AUDR` (brain readiness)
- **Audit corrections folded:** all 26 roadmap corrections in `040` §3; the 16 missing epics
  (E1–E16) in `040` §4; the risk register (`041`) owns the tracking

---

## 1. What changed — from the brief, and from the pre-audit draft

**From Jeremy's original brief (discovery corrections):**

[Operational detail retained in the private record]
2. Most of proposed Phase 1 already exists and is drilled. Phase 1 is **harden + verify +
   document + fill residual gaps**, not greenfield.
3. Two Phase-2 candidates are rejected on evidence: OneUptime (heavy monolith) and Tempo
   (nothing emits traces). See `035` Part B.

**From the pre-audit draft (audit corrections — the substantive ones):**

[Operational detail retained in the private record]
8. **Every epic now has a measurable acceptance test and a phase go/no-go gate;** the one
   irreversible-loss fix is carved out ahead of roadmap sign-off.

## 2. Jeremy's decision points (the roadmap's gates)

The audit deduped these across all ten lenses (`040` §7). Recommendation is the panel's; the
final call is Jeremy's.

| # | Decision | Recommendation | Blocks |
|---|---|---|---|
| J1 | Merge the VPS runbook into intent-os? | **Merge the docs** (unsquashed subtree under `ops/`), but see J2b for secrets | Epic 1.3 |
| J1b | Secrets on merge | **Keep `[encrypted secrets file]` federated** in a tighter-membership boundary (submodule / separate repo + CODEOWNERS), OR accept blast-radius collapse with recorded compensating controls. Jeremy's lean is full merge; the panel's engineering rec is federate | Epic 1.3 |
[Operational detail retained in the private record]
| J3 | Phase-2 per-tool verdicts | Accept `035` Part B: trio integrate-later, OneUptime skip, Tempo skip, keep borg + off-site, adopt Ansible; **add Watchtower** (J7) | Phase 2 scope |
[Operational detail retained in the private record]
| J6 | Status page wanted at all? | If yes, Gatus (~20 MB); if the real need is incident state, build the incident model (Epic 1.4b) instead | Phase 2 |
[Operational detail retained in the private record]
| J10 | Publish the reports feed publicly at all? | **Default-deny**: publish only a separately authored, sanitized executive summary; keep SPOF/topology/deploy internals private, OR gate the whole feed behind the tailnet. **Applied already** (see §9) — Jeremy confirms or overrides | Phase 0 |
[Operational detail retained in the private record]
| J13 | Governance ceremony tiering | Approve the lightweight lane for routine epics vs full AAR for phase-closes/incidents | `039` amendment |
| J14 | Carve Epic 1.1 as a pre-roadmap hotfix? | **Yes** — ship off-site + immutability the day J2 is answered, before approving the full roadmap | Epic 1.1 |
| J15 | Approve the reframed roadmap as the Phase-0 exit gate | — | Phase 1 beads |

## 3. Epic 1.0 / 1.1 — the pre-roadmap hotfixes (ship before full sign-off)

The audit's sharpest structural point: **do not hold the only irreversible-loss fix behind a
15-epic review.** Two epics are authorized by their own decision gate and ship immediately.

[Operational detail retained in the private record]
- **Epic 1.1b — Independent repository recovery.**
  [Operational detail retained in the private record]

## 4. Phase 1 — harden the estate (verify, prove, service-shape)

Goal: prove the estate survives a real disaster, close the ranked SPOFs, and make the existing
fabric documented and machine-readable. Every epic is independently shippable; order within the
phase is by risk. **Phase-1 exit gate = every epic's acceptance test green AND a Jeremy
go/no-go.**

[Operational detail retained in the private record]
- **Epic 1.4 — Service-shape foundations (the API-first down payment).** Land, in a new
  `schemas/` dir, versioned JSON Schemas with a **canonical Service/Host/Environment entity
  (schema v0) FIRST** — every leaf schema references its stable ID. Then: NDJSON `notify.log`,
  a JSON liveness-sweep artifact, a `pnpm mc` JSON snapshot, the alert label schema, an
  **action-audit event schema** (subject/action/resource/timestamp/actor-type/outcome) with
  capture beginning in Phase 1, and an **authorization model** dimension (subject/resource/
  action) so authz is not a Phase-3 retrofit. *Acceptance: each schema has a CI-wired validator
  AND its producing script fails the build on non-conforming output; each names an owner and an
  additive-only evolution rule. No schema lands without an enforcing consumer.*
  - **Epic 1.4b — Incident process + producer (before the incident schema is "done").** Define
    severities and a declare/ack/resolve lifecycle on one page; the notify spine (which already
    classifies severity) opens an incident on high/urgent; a Slack slash-command/emoji acks.
    *Acceptance: a real alert opens an incident record; an ack transitions it.*
[Operational detail retained in the private record]
- **Epic 1.10 — Dependency-lifecycle / CVE / EOL / license track (cross-cutting).** Image + dep
  CVE scanning (Trivy/Grype/renovate) routed through the notify spine; a written patch-cadence
  SLA; a committed EOL register; a one-page license register (rule: **Grafana/Loki are AGPLv3 —
  stay unmodified and internal-only; any modification or external offering triggers legal
[Operational detail retained in the private record]
  registers exist.*
- **Epic 1.11 — Bus-factor drill.** [the CTO] executes a from-scratch restore + a manual deploy with
  no Jeremy and no AI, timed, findings filed. *Acceptance: a second human completes recovery;
  the gaps found become beads.*
- **Epic 1.12 — Reports-feed publish gate (default-deny).** Replace the token-blocklist scrub
  with an allowlist + a hard-fail publish gate; the public feed carries only sanitized
  executive summaries (SPOF tables, dependency graphs, topology, deploy internals, hostnames,
  IPs, personal identifiers stay private). *Acceptance: the gate rejects a full discovery doc
  and passes a sanitized summary. Landed in Phase 0 already (§9) — this epic hardens it.*
- **Epic 1.13 — SLI catalog + per-stack RPO decision (J8).** A minimal SLI catalog (per-domain
  uptime, backup freshness, restore-drill recency, alert-path liveness — most already exist as
  sweep rows) + a conscious per-stack RPO. *Acceptance: every customer stack has a stated RPO
  and a "healthy" definition; RPO/RTO + last-drill-date are added to the ADR-000 §7 contract.*
  **(Merged with Epic 1.14 below — the SLI catalog is the collection half of the metrics
  implementation.)**

### Phase-1 operationalization epics (Jeremy, 2026-07-11)

> **Framing — read this first.** Phase 0's completion round already *defined* the metrics
> (`043`), the Definitions of Done (`044`), the repository architecture (`046`), and the
> governance calendar + RACI (`050`). These four epics are the **implementation** of those
> definitions — turning documents into live collection, enforced gates, and scheduled jobs.
> They are scoped as "operationalize/enforce/extend the Phase-0 artifact," not "author it
> again," and each cites the document it makes live. Where an item is already delivered by a
> Phase-0 doc, that is stated rather than re-scoped as new work.

- **Epic 1.14 — Platform success-metrics collection (implements `043`).** Absorbs Epic 1.13's
  SLI catalog. Build the *collection* the KPI catalog defines: wire each metric to a source
  (uptime probes, backup logs, incident records, deploy results, coverage scans), emit the
  metric values as structured data (JSON, alongside the `037` Epic 1.4 schemas), and compute the
  three **composite scores** added to `043` — a reliability score, a documentation score, and a
  platform-maturity score. Every metric gets its owner, collection method, review cadence, and
  success threshold (already tabulated in `043`; this epic makes them true). *Acceptance: each
  KPI in `043` has a live data source emitting structured values; the three composite scores
  compute from real inputs; nothing is "manual" that a cheap job could collect.*
- **Epic 1.15 — Definition-of-Done as a review norm (implements `044`; gate deferred).** *CTO
  ruling, 2026-07-11:* the four DoD checklists (`044`) are adopted **now as a review norm** — the
  closing PR/AAR must show the DoD lines satisfied, checked by the reviewer, not by a built gate.
  A **machine gate** (a `bd`-close preflight or CI check that blocks close on a missing AAR/sign-
  off) is real engineering that also fights the bd rapid-write flow, and at two contributors the
  norm doesn't drift enough to justify it. **Trigger to build the gate:** contributor count
  crosses ~4, **or** an audit finds ≥2 epics closed out of DoD compliance. *Acceptance now: every
  epic-closing PR demonstrates its `044` DoD in the AAR; the gate is a backlog item behind the
  stated trigger, not Phase-1 build work.*
- **Epic 1.16 — Repository architecture (largely delivered — `046`).** The layered stack, the
  future services/packages/repositories/APIs/schemas map, and the repo-split/merge + module/
  service-boundary criteria are **already documented in `046-AT-ARCH`**. This epic is therefore
  a thin standing item: keep `046` current as the estate grows (a governance-calendar review,
  `050`), and — the one genuinely new piece — extend it with the concrete future-services and
  future-schemas map produced by the Phase-2 data-model and API epics (2.6/2.13). *Acceptance:
  `046` reflects the Phase-2 platform structure once those epics land; no fresh authoring
  needed now — the criteria exist.*
- **Epic 1.17 — Program governance, operationalized (implements `050`).** The governance
  calendar, review schedules (architecture/security/dependency/DR/roadmap/quarterly planning),
  and RACI matrix are **authored in `050`**. This epic wires the recurring items into actual
  scheduled jobs/reminders (each with its automations-registry row) so governance is
  *operational, not ad hoc* — the weekly backup check and page-regen, the monthly dependency
  and doc-freshness reviews, the quarterly DR/architecture/security reviews. *Acceptance: every
  recurring `050` activity is a scheduled, registered job or a calendared reminder with an owner;
  none rely on "when someone remembers."*
- **Epic 1.18 — Ownership matrix, extended (implements `050` §2).** `050` already carries a
  RACI over Jeremy/[the CTO]/agents. This epic **extends** it to per-capability ownership across the
  ten areas Jeremy named (infrastructure, repositories, documentation, services, runbooks,
  monitoring, security, backups, incident response, AI agents), and assigns each **critical
  capability a named owner** at its ADR-000 §7 contract sign-up. RACI stays the default; DACI
  is offered where a single decider matters more than a single accountable. *Acceptance: every
  critical capability has one identified owner; the matrix covers all ten areas.*

## 5. Phase 2 — observability, then platformization

Gated on Phase 1's schemas existing (tools land on contracts, not ad hoc) and on the RAM budget
re-stated against committed RSS (J4).

[Operational detail retained in the private record]
- **Explicitly skipped** (rationale recorded so future phases don't relitigate blind):
  OneUptime, Tempo, Restic.

### Phase-2 platformization epics — ALL COMMITTED (Jeremy: "we build for glory", 2026-07-11)

> **Decision (Jeremy, principal call — supersedes the same-day CTO restraint recommendation).**
> The one genuinely-his portfolio question — build Mission Control as a *product-grade platform*,
> or keep it operationally-humble and spend the capacity on revenue — is **answered: we build the
> full platform.** All ten of Jeremy's platformization epics are **committed Phase-2 work**, not a
> demand-triggered backlog. Recorded in `decision-log/009-2026-07-11` (D45); it reverses DL-008
> D41 (the trim), which is now marked superseded.
>
> **What the CTO keeps even in glory mode — because it is competence, not restraint:** the *order*
> below is load-bearing. Building all ten is the mandate; building them in the wrong order is how
> a big platform collapses under its own weight. So: the data model is built **producer-order**
> (each entity lands as its emitter is built — but every emitter *is* built), and the API is built
> **contract-first** (one convention ADR, then the full endpoint fleet conforms to it). These are
> sequencing discipline, not scope cuts — the destination is the whole thing.

**Dependency-ordered build (the critical path through Phase 2's platform tier):**

- **Epic 2.13 — Operational data model [committed, full].** The canonical schemas for **every**
  platform entity — Service, Host, Environment, Incident, Backup, Deployment, Automation, Agent,
  Runbook, Metric, Alert, Event, User, Role, Permission — extending the Epic 1.4 entity. Each
  versioned with a validating consumer (the `035`/`040` anti-drift rule). *Built in producer
  order (an entity ships when its emitter ships), but all producers are in scope. Acceptance:
  every platform entity is modelled, versioned, and has a live producer by Phase-2 exit.*
- **Epic 2.6 — Internal API platform [committed, full fleet].** The API-convention ADR + skeleton
  **first** (auth via tailnet + 2.4 RBAC, versioning, error shape, pagination, read/write split,
  mandatory audit log), then the **full capability API fleet** over the 2.13 model — inventory,
  monitoring, backups, deployments, incidents, agents, services, schemas, audit. **No UI or
  automation touches infrastructure directly; everything calls the API.** *Acceptance: every
  capability exposes a documented, RBAC'd, audited API; the portal is a pure client.*
- **Epic 2.7 — Event bus [committed].** Event-driven fabric — deployment-completed, backup-failed,
  restore-succeeded, incident-opened, service-unhealthy, repository-updated, security-alert,
  agent-started (Event entity, 2.13). *Automations consume events, not polls; the notify spine and
  incident producer publish. Acceptance: the estate's automations are event-driven end to end.*
- **Epic 2.9 — Service registry [committed].** Every service self-describes from data — identity,
  owner, health, dependencies, endpoints, version, environment, runbook, SLO (Service entity,
  2.13) — retiring the markdown `self-hosted-services.md`. *Acceptance: "what services exist?" is
  answered from data.*
- **Epic 2.10 — Automation registry v2 [committed].** Every automation class in one registry —
  scheduled, event-driven, AI agents, background workers, hooks, webhooks (Automation/Agent
  entities, 2.13), extending today's scheduled-only registry. *Acceptance: every automated process
  in the estate is discoverable in one place.*
- **Epic 2.8 — Asset graph [committed].** The relationship graph across hosts, services,
  containers, repositories, agents, schemas, databases, incidents, dependencies — for real
  **impact analysis**. *Acceptance: any node's blast radius ("if this dies, what breaks?") is
  answered from the graph.*
- **Epic 2.14 — Search platform [committed].** One query surface over runbooks, services,
  incidents, AARs, ADRs, docs, schemas, repositories. *Acceptance: "where is the runbook / ADR /
  incident for X" is one query, not a grep.*
- **Epic 2.15 — Executive reporting engine [committed].** Auto-generate the weekly/monthly/
  quarterly summaries `039` + `043` define, from the data model, feeding the reports feed. *No
  human assembles a report by hand. Acceptance: reporting is generated, consistent, scheduled.*
- **Epic 2.11 — Plugin architecture [committed].** Products integrate **without patching the
  core** — registration, versioning, capability discovery, lifecycle, permissions, configuration;
  the ADR-000 integration contract as a runtime extension point. *For a multi-product platform
  this is foundational, not deferred. Acceptance: a product joins by registering, not by a patch.*
- **Epic 2.16 — Distributed tracing [committed — glory addition].** The audit skipped Tempo
  because *nothing emits traces*. Glory build reverses that: **instrument the services so traces
  exist**, then land Tempo + the trace pipeline. *Don't skip the telemetry for lack of data —
  build the data. Acceptance: request flows across the platform are traceable end to end.*
- **Epic 2.3 — Central logs [committed, promoted from need-gated].** Loki + promtail with a
  day-one retention policy — no longer waiting for an incident to hurt. *Acceptance: central logs
  exist before the incident that needs them.*

**Portal design system (Jeremy's 2.12)** builds with the first portal screens in **Phase 3 (Epic
3.0)** — a UI system is built *with* the UI, which is sequencing, not a cut; the commitment to
build it is total.

**Scope reality (the true bill — no shortcuts on the honesty either).** This is a **~14-epic
Phase 2** plus a full Phase 3 portal. That is a genuine multi-quarter engineering program, and
the CTO owes the principal three hard requirements the glory build actually needs — see the new
**§9b Capacity & the true bill**. Committing to glory means committing to those, not just to the
epic list.

## 5b. Phase 2.5 — Platform Technology Selection & Reference Architecture (Jeremy, 2026-07-11)

> **Why this phase exists (and why it's the right call).** The roadmap as written transitions
> straight from platform foundations (Phase 2) into implementation (Phase 3), and several Phase-3
> epics quietly *assume* technology choices — an auth system, an event-bus engine, a workflow
> runner, a portal framework — that were never formally evaluated. That is precisely what ADR-000's
> platform-first / **evaluate-don't-assume** doctrine forbids: never hard-code an implementation
> technology before deliberately evaluating it. Phase 2.5 closes that gap. It is inserted as a
> **decimal (2.5), not a renumber** — chosen over renumbering Phase 3→4 because renumbering would
> break every existing bead ID, ADR reference, and cross-link for zero benefit.

**This is not an implementation phase — its output is engineering decisions, not software.** It is
the **final gate before implementation.** Every Phase-3 implementation epic must reference an ADR
produced here; **no Phase-3 epic may hard-code a technology not selected in Phase 2.5**, and Phase-3
epics *implement previously-approved architecture — they never make technology decisions.*

**Deliverables:** ADRs · Technology Evaluation Reports · Reference Architectures · Dependency
Inventories · an Open Source Bill of Materials (OSBOM) · SaaS Evaluation Reports · version /
upgrade / fork policies · Security Review docs · Compatibility Matrices · Operational Ownership ·
Lifecycle docs.

**Per-evaluation-epic rubric (every 2.5.x epic must produce):** Business objective · functional +
non-functional requirements · candidate technologies · a scored comparison matrix (license,
community health, release cadence, security history, resource consumption, operational complexity,
migration difficulty, vendor lock-in, long-term sustainability, cost) · integration / API / upgrade
/ rollback / replacement strategy · a **recommendation with every rejected alternative and the
reason it was rejected** · an **ADR** · acceptance criteria · future-phase hooks.

**Selection principle (binding):** prefer **open-source, self-hostable, internally-governable**
software; adopt SaaS only where it delivers a clear operational advantage outweighing cost, vendor
dependency, security, and maintenance burden. Mission Control must remain **operable independently
of any single commercial vendor** wherever reasonably achievable.

**Standing infrastructure assumption — now ADR-000 Article V (Jeremy, 2026-07-11; binding on every
phase/epic/tech decision, not just 2.5.x; change only with Jeremy's explicit approval).** Intent
Solutions runs a **dedicated production server capable of self-hosting operational infrastructure**
— assume it is available to host supporting platform services. Do **not** default to SaaS because
it's easier. **Assume sufficient production resources:** never reject a high-quality OSS component
for an extra ~500 MB of RAM if the box has capacity — optimize first for maintainability,
reliability, and long-term architecture; resource optimization is driven by *measured* constraints,
documented, never assumed up front.

- **Mandatory evaluation order (self-hosted-first ladder):** (1) an **existing capability already
  running in the estate**; (2) **existing OSS that can be self-hosted**; (3) **lightweight
  commercial software with a self-hosted deployment option**; (4) **SaaS — only** when it provides
  significant operational advantage outweighing vendor lock-in, recurring cost, operational
  dependency, data-ownership, security, and loss of platform control. **Every SaaS recommendation
  must explicitly justify why it beats an appropriate self-hosted alternative.**
- **Estate awareness (integrate before introducing new tech):** assume the platform already
[Operational detail retained in the private record]
  integrate with these **before** adding anything new.
- **Preferred technology traits:** OSS licensing, active community, long-term sustainability, strong
  docs, API-first, containerized deployment, health monitoring, backup + upgrade + DR support.
- **Managed-service, not standalone-tool:** new OSS components become **managed platform services
  inside Mission Control**, not isolated tools.
- **No adoption without a long-term operational plan.** Every adopted dependency ships with
  installation automation, configuration management, health monitoring, and a backup / upgrade /
  rollback / documentation / ownership / lifecycle / AAR plan (this is the 2.5.12 OSBOM row for it).

**Sequencing note (a refinement Phase 2.5 forces — CTO, 2026-07-11).** "Between Phase 2 and Phase
3" is right for the *net position*, but a few Phase-2 epics are **engine-dependent**: 2.7 event bus,
2.14 search, 2.15 reporting, 2.10 automation cannot have their *runtime engine* built before it's
*selected*. So Phase 2.5 **interleaves**: the vendor-neutral Phase-2 work (2.13 data model, 2.6 API
contract, the event *schemas/catalog*, the service *metadata model*) proceeds first and is what 2.5
evaluates against; then 2.5 selects the engines; then the engine-dependent *build* of 2.7/2.10/2.14/
2.15 completes against its ADR. This is wired in beads (2.7→2.5.5, 2.14→2.5.6, 2.15→2.5.8,
2.10→2.5.4) so no epic builds a runtime before its engine is chosen.

**The epics (each produces an ADR):**

- **Epic 2.5.1 — Platform Technology Governance [foundational — do first].** The evaluation
  methodology itself: evaluation criteria, scoring framework, ADR template, technology-lifecycle
  policy, approval workflow, sunset policy. *Every other 2.5.x epic uses this. Children: 2.5.1a–f.*
- **Epic 2.5.2 — Identity & Authentication.** Evaluate Auth.js · Authentik · Keycloak · Zitadel ·
  SuperTokens · Better Auth (+ future). Selects the platform's identity substrate (feeds Phase-2
  identity 2.4 + the portal's auth).
- **Epic 2.5.3 — Authorization & Policy Engine.** Evaluate built-in RBAC · Cerbos · Open Policy
  Agent · Permit.io · Casbin. → ADR.
- **Epic 2.5.4 — Workflow & Automation Platform.** Evaluate Temporal · Trigger.dev · Windmill ·
  BullMQ · n8n · Inngest · native. Decides what belongs to Mission Control vs an external engine
  (feeds automation 2.10 + the 3.1 automation framework).
- **Epic 2.5.5 — Event Bus.** Evaluate NATS · Redis Streams · RabbitMQ · Kafka · native. → ADR
  (feeds Phase-2 event bus 2.7).
- **Epic 2.5.6 — Search Platform.** Evaluate Meilisearch · Typesense · OpenSearch · Postgres FTS ·
  hybrid (feeds Phase-2 search 2.14).
- **Epic 2.5.7 — Notification Platform.** Evaluate Slack · email · future Teams/Discord/SMS/push —
  delivery providers, SDKs, retry, templates, operational ownership (feeds the 3.1 Slack + email +
  notification-router frameworks).
- **Epic 2.5.8 — Reporting Platform.** Evaluate tech for weekly/monthly/quarterly/annual reports,
  executive dashboards, PDF generation, email delivery, chart generation, historical reporting
  (feeds Phase-2 reporting 2.15).
- **Epic 2.5.9 — Storage Architecture.** Evaluate Cloudflare R2 · Backblaze B2 · Wasabi · local ·
  Dolt · PostgreSQL · Redis; assign each a responsibility; document backup, DR, and lifecycle
  (feeds the off-site-backup decision, roadmap Epic 1.1).
- **Epic 2.5.10 — AI Agent Platform.** Evaluate OpenAI Agents SDK · LangGraph · CrewAI · AutoGen ·
  Mastra · native orchestration; document where AI agents belong in Mission Control (feeds Phase-3
  agent management 3.4). *(Note: Google ADK appears in Jeremy's list; flag it against the standing
  no-GCP constraint during evaluation.)*
- **Epic 2.5.11 — Portal Framework.** Evaluate Next.js · React · shadcn/ui · Tailwind · component
  libraries · state management · charting · auth integration · admin framework (feeds Phase-3
  portal 3.0/3.7).
- **Epic 2.5.12 — Open Source Governance / OSBOM [foundational].** For every adopted dependency:
  upstream repo, fork/mirror, license, version, owner, adoption reason, security-advisory feed,
  releases monitoring, Dependabot/Renovate policy, upgrade cadence, monthly/quarterly/annual review,
  compatibility matrix, rollback + replacement strategy, sunset criteria. **Produces the
  authoritative Mission Control OSBOM** (implements roadmap Epic 1.10 + governance 050).

## 6. Phase 3 — the full portal (vertical-slice-first as method, full surface as destination)

**Glory build (Jeremy, 2026-07-11):** the destination is the **complete authenticated RBAC
portal** — every surface in the ADR-000 end-state. The audit's "one vertical slice first" is kept
as the **build *method*** (prove the pattern end-to-end before fanning out, so the fan-out rides a
proven spine) — **not** as a scope cap. The deferred-behind-demand items below are **un-deferred
and committed.** Read/embed surfaces still ride Grafana where Grafana is genuinely the better tool
(that's leverage, not a shortcut); bespoke build is reserved for write + orchestration surfaces.

> **Phase-2.5 gate (binding on every Phase-3 epic).** No Phase-3 epic makes a technology decision.
> Each **references the ADR** produced in Phase 2.5 for every technology it uses, and may **not
> hard-code** a technology not selected there: identity/auth → 2.5.2/2.5.3, workflow/automation →
> 2.5.4, event bus → 2.5.5, search → 2.5.6, notifications → 2.5.7, reporting → 2.5.8, storage →
> 2.5.9, AI agents → 2.5.10, portal framework → 2.5.11, and every dependency is entered in the
> 2.5.12 OSBOM. A Phase-3 epic that needs a technology with no Phase-2.5 ADR is **blocked** until
> that evaluation is done.

- **Epic 3.0 — Portal design system (Jeremy's 2.12, relocated here):** layout, navigation,
  component library, accessibility, responsiveness, color system, notification UX — built as the
  first portal work so screen one is consistent, **not a phase ahead of any UI**. Precedes 3.1.
- **Epic 3.1 — The incident vertical slice (the MVP):** schema (2.13) → **first capability API
  built on the 2.6 contract** → auth (2.4) → UI (3.0), built end-to-end. This is the portal's
  first user story, and the first real consumer that any capability API is written against.
- **Epic 3.2 — Action Security Model:** the portal **enqueues** actions the existing
  force-command paths execute — never standing shell creds; every action append-only audited
  (the 1.4 action-audit schema). Deploy/kill/rollback are designed here or not at all.
- **Epic 3.3 — Read surfaces on Grafana:** dashboards/health/metrics as Grafana datasource +
  panel config, not bespoke code.
- **Epic 3.4 — AI-agent management:** agents modeled as a **subtype of the automations
  registry** (not a parallel system); wrap RemoteTrigger; data model first, control verbs
  second.
- **Epic 3.5 — Service catalog:** the portal surface over the 2.9 service registry, keyed on the
  canonical Service entity — owner, health, deps, runbook, SLO per service.
- **Epic 3.6 — Full RBAC role model [committed, un-deferred].** The complete role hierarchy from
  the ADR-000 end-state — Executive Leadership → On-Call Engineer → scoped Contractor and the
  roles between — not the 3-role Phase-2 floor. Every surface authorizes against it. *Acceptance:
  each portal capability enforces role-scoped access; roles map to the 2.13 Role/Permission model.*
- **Epic 3.7 — Horizontal portal fan-out [committed].** Once 3.1 proves the vertical-slice
  pattern, fan out the remaining surfaces on it — infra/environment status, monitoring, alerts,
  backup + restore-verification, DR readiness, security posture, deployments, AI-agent management,
  repo health, CI/CD, service catalog, runbooks, architecture, change management, operational
  metrics, audit history. *Each surface is a client of a 2.6 API. Acceptance: the ADR-000 surface
  list is live in the portal.*
- **Epic 3.8 — Executive + cost dashboards [committed, real build].** Not the YAML ledger
  rendered as-is — a real cost + executive-metrics surface over the data model and the 2.15
  reporting engine. *Acceptance: leadership reads operational + cost health from a live dashboard.*
- **Epic 3.9 — Compliance + audit surface [committed].** Stood up proactively — audit-history
  browse, change-management records, the append-only action log (3.2) as a queryable compliance
  view — rather than waiting for a named external obligation. *Acceptance: any privileged action
  is reconstructable from the portal's audit surface.*

## 6b. Phase X — Continuous Improvement (the standing operational phase)

> **What this is (Jeremy, 2026-07-11).** Not an implementation phase — the **standing phase that
> begins after Phase 3 and never ends.** It acknowledges that Mission Control is a long-lived
> operational platform, not a project with a finish line. Phase X is where the governance
> cadence (`050`) actually lives once the platform is built: it *owns* the recurring reviews
> rather than each being a one-off. It has no "done" — it has a rhythm.

Phase X owns, on the cadence defined in `050`:

- Quarterly architecture reviews (is the layering `046` still true?).
- Annual roadmap refreshes (this document is re-checked against reality, superseded sections
  marked).
- Dependency modernization + the CVE/EOL pipeline (`037` Epic 1.10 becomes a standing cadence).
- Technical-debt and operational-debt reduction (the `043` trend KPIs drive it).
- Platform performance optimization and cost optimization.
- Security-posture reviews (quarterly, `050`).
- Disaster-recovery exercises (quarterly game-day, `037` Epic 1.3 becomes recurring).
- AI-assisted codebase audits and documentation-quality audits.
- Mission Control **maturity assessments** (the platform-maturity score, `043`, tracked over
  time).

*Acceptance (ongoing, not one-time): each item runs on its `050` cadence with an owner and a
logged output; a cycle that produces nothing is either working — say so — or being skipped —
fix it. Phase X's health is itself a KPI.*

## 7. Cross-cutting tracks (every phase)

- **Brain ingestion + disclosure filter** (`spine-c67`, Gap 2/3 of `002-AA-AUDR`): the
  capture→propose→review bridge and the **code-enforced** no-comp/no-PII filter at ingest,
  reusing `ci/disclosure-gate.sh` server-side. Its own epic, scheduled with Phase 1–2.
- **Teaching-tool packaging** with the incident/runbook-class exception from `039` (operational
  docs get a one-line purpose header, not a teaching preamble).
- **Documentation law** (`039`, tiered): full 9-section AAR for phase-closes/incident-bearing
  epics; the lightweight lane (What/Why/Verification/Rollback/Next) for routine epics; the
  action-audit + RPO/RTO fields required.

## 8. Dependency order and the critical path

1.0 (dev-box hardening) and 1.1 (off-site+immutable) ship first, as hotfixes. 1.2 (Ansible) and
1.4 (schemas, Service entity FIRST) start in parallel. 1.3 (DR game-day) needs 1.1 + 1.2 + key
escrow. 1.5 (alert floor), 1.6 (deploy safety), 1.10 (CVE), 1.14 (SLI/RPO + metrics) are
independent. 1.7 (merge) is gated J1 and sequenced after 1.0 + 1.1. **Phase 2 (glory build,
DL-009 — all epics committed):** the data-model spine is 2.13 (producer-driven, needs 1.4) → 2.6
(API, needs 2.13 + 2.4) → {2.7 events, 2.9 registry, 2.10 automation, 2.14 search, 2.15
reporting}; 2.8 graph needs 2.9; 2.1/2.2 observability + 2.4 identity run alongside. **Phase 2.5
(NEW gate) sits between Phase 2 and Phase 3:** it needs Phase 2's foundation to evaluate against
(you evaluate an event-bus engine knowing the 2.7 event model, an auth system knowing the 2.4
identity need), and **2.5.1 governance methodology is done first** because every other 2.5.x
evaluation uses its scoring framework + ADR template; 2.5.12 OSBOM runs throughout. **Phase 3 now
depends on Phase 2.5** — no Phase-3 epic starts until its technologies have an approved ADR (3.1
core → 2.5.2/2.5.3 auth, 2.5.4 workflow, 2.5.5 events, 2.5.7 notifications, 2.5.11 portal; 3.4
agents → 2.5.10; etc.) — plus 2.13 + 2.6 + 2.4 + 3.2 (action security). J5 (identity) is decided
at Phase-1 exit, then *ratified against the 2.5.2 evaluation* before the portal consumes it.

## 9. Solo-operator capacity and ceremony (the reality check)

[Operational detail retained in the private record]

1. **Tiered ceremony** (`039` amendment): full AAR + executive package only for phase-closes
   and incident-bearing epics; a lightweight lane for routine epics.
2. **Per-epic sizing + a minimum Phase 1.** Each epic below carries a t-shirt size and a
   "needs-Jeremy vs agent-unattended" flag; the declared **minimum Phase 1** (the non-negotiable
   floor) is: Epic 1.0, 1.1, 1.3, 1.5 — dev-box hardening, off-site+immutable, DR game-day, and
   the alert floor. Everything else is valuable but deferrable if capacity is short.

| Epic | Size | Autonomy |
|---|---|---|
| 1.0 dev-box hardening | S | needs Jeremy (SSH lockout risk) |
| 1.1 off-site + immutable | M | needs Jeremy (J2) then agent |
| 1.2 Ansible | L | agent, Jeremy reviews |
| 1.3 DR game-day + DB dumps | L | needs Jeremy (J8/J9) then agent |
| 1.4 schemas + Service entity | M | agent |
| 1.4b incident process | S | agent |
| 1.5 alert floor | S | agent |
| 1.6 deploy safety | M | agent |
| 1.7 runbook merge | M | needs Jeremy (J1/J1b) then agent |
| 1.8 verify+document | L | agent |
| 1.9 secrets evolution | M | needs Jeremy (J12) then agent |
| 1.10 CVE/EOL/license | M | agent |
| 1.11 bus-factor drill | S | needs [the CTO] |
| 1.12 publish gate | S | agent (done in Phase 0) |
| 1.13 SLI + RPO | S | needs Jeremy (J8) then agent |

## 9b. Capacity & the true bill (glory build — Jeremy, 2026-07-11)

The full build is the decision. The CTO's job is not to re-argue it — it is to state, plainly,
the three things glory **requires**, so "we build" is a commitment to the bill, not just the epic
list. None of these is a reason not to build; each is a thing that must be true for the build to
succeed instead of stall.

1. **Dedicated engineering capacity — glory needs people, not slack time.** ~14 Phase-2 epics + a
   full RBAC portal is a **multi-quarter dedicated program**, not a nights-and-weekends effort on
   top of four other company arms. This must be resourced one of two ways: (a) protected,
   scheduled engineering time from Jeremy + [the CTO] + agents, with the revenue opportunity cost
   accepted **on the record**; or (b) a hire/contractor whose time is *not* fungible with billable
   work. The single biggest risk to glory is not architecture — it is a full roadmap funded with
   spare capacity that spare capacity never materializes for. **Decision Jeremy owns:** which of
   (a)/(b), and the protected-time budget. *(Compensation/hiring terms are Jeremy-private — not
   this repo; this line only flags that the decision exists.)*
[Operational detail retained in the private record]
3. **The Phase-1 floor still ships first — the one shortcut glory cannot take.** Building for
   glory does **not** mean building the event bus before the off-site immutable backup exists. The
   irreversible-loss protections and the hardening floor (Epics **1.0, 1.1, 1.3, 1.5**) precede
   **all** platform work, non-negotiable. Correct glory sequence: **harden (Phase 1 floor) →
   foundation (data model + API contract + identity + observability) → platform tier (events,
   registries, graph, search, reporting, plugins, tracing, logs) → full portal (Phase 3) → Phase
   X.** Chasing the portal before the estate is safe is the single sequencing mistake that turns
   an ambitious build into a fragile one. We build big **and** we build in order.

**Bottom line:** the vision is fully committed. Its success is gated on (1) resourced capacity and
(2) dedicated infra being decided at Phase-2 entry, and on (3) the hardening floor going first.
Say yes to the bill, not just the blueprint.

## 10. What this roadmap refuses to do

- No tool adoption without a capability owner and an ADR-000 §7 contract signature.
- No OneUptime/Tempo/Restic re-litigation without new facts.
- No schema without an enforcing consumer (the anti-drift rule applied to itself).
- No portal UI before the API layer; no portal write-action without the Action Security Model.
- No public feed entry that is not a sanitized executive summary through the default-deny gate.
- No Phase 1–3 beads until Jeremy approves this roadmap (Phase-0 exit criterion) — **except**
  the two carved hotfixes (Epic 1.0, 1.1), which ship on their own gates.
