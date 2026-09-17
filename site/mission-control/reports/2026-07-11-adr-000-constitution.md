> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 038-AT-DECR — ADR-000: the Mission Control constitution

> **What this is and why it matters.** This is the founding architecture decision record
> (ADR) for the Mission Control program — the document every future epic cites when it
> justifies a design choice. It answers, once, the questions that would otherwise be
> re-litigated in every phase: why Intent OS exists, what "platform-over-tools" means in
> practice, what contract every future product signs up to, which architecture principles
> are binding (not advisory), what the end-state looks like, and how this document itself
> gets amended. Jeremy Longshore's four program-doctrine sections are preserved below as
> standing articles, near-verbatim, so future epics can cite his words rather than a
> paraphrase. If a proposed change contradicts this ADR, either the change is wrong or this
> ADR must be amended first — silently doing both is forbidden.

- **Status:** ADOPTED (Phase-0 deliverable; binding once the Phase-0 PR merges and Jeremy
  approves the revised roadmap)
- **Decision-log pointer:** `decision-log/007-2026-07-10-adr-000-mission-control-constitution.md`
- **Companion standard:** `039-DR-STND-epic-documentation-aar-and-reporting-standard.md`
  (bound by reference — its rules carry ADR-000 authority)
- **Supersedes:** nothing; ADR-000 is the root

---

## 1. Why Intent OS exists

[Operational detail retained in the private record]

**Intent OS is the single place where the company's operations are organized and governed.**
It began as the "home base" repo (doctrine, business plan, system map, decision log). This
ADR promotes it to the **permanent Mission Control platform**: the authoritative operational
control plane for every Intent Solutions product — infrastructure, deployments, monitoring,
incidents, security operations, backups and disaster recovery, and governance.

## 2. The decision

1. **Intent OS is the operational control plane of record.** Operational capabilities,
   registries, standards, and program records live here (or are explicitly federated with a
   pointer from here — never duplicated without an owner).
2. **The program is multi-phase by design** (Phase 0 planning → later implementation
   phases), and each phase is governed by the standing articles in § 6.
3. **The end-state is a product, not a pile of scripts:** an authenticated internal web
   application — the company's Mission Control — described in § 5.
4. **The architecture principles in § 4 are binding.** A deliverable that violates them
   must either be reworked or carry an explicit, Jeremy-approved exception recorded in the
   decision log.

## 3. Platform-over-tools

Open-source tools (monitoring agents, backup engines, dashboards, schedulers) are
**implementation details behind one operational interface** — never the interface itself.

- We adopt a tool because a platform capability needs it, not because the tool is good.
  Capability first, tool second.
- Every capability must survive its tool being swapped. The stable thing is the **service
  interface and its data model**; the tool behind it is replaceable.
- Consequence for evaluations (gap analysis, Phase-2 verdicts): "the tool is excellent" is
  not sufficient; the question is "which capability does it serve, what interface does it
  expose to the platform, and what does it cost the estate (RAM, attention, upgrade
  surface)?"

## 4. Binding architecture principles

### 4.1 API-first

Every capability — backups, incidents, deployments, inventory, monitoring, AI agents —
exposes a **stable internal service interface** (an API, a queryable data model, or at
minimum a documented machine-readable artifact with a stable schema). The future dashboard
is largely a UI layer over the existing platform, never a rewrite. In Jeremy's words
(2026-07-10): *"design API-first. Every capability should expose a stable internal service
interface so the future dashboard is largely a UI layer over the existing platform rather
than a rewrite."*

### 4.2 Platform-before-UI

Where practical, separate **business logic · automation · APIs · data storage ·
presentation**, so a future web interface can be added without significant architectural
rework. No capability is "done" when it only works as a human-invoked script; it is done
when its state is machine-readable by the future portal.

### 4.3 Avoid tight coupling to CLIs and individual components

Avoid designing systems tightly coupled to command-line tools or individual infrastructure
components. Think in terms of **reusable platform services with clearly defined APIs, data
models, and presentation layers.** (Jeremy, 2026-07-10, near-verbatim.)

## 5. The end-state: the Mission Control portal

The long-term objective (Jeremy, 2026-07-10, preserved near-verbatim): Intent OS evolves
into the central operational Command Center — **an authenticated internal web application
that serves as the primary operational interface for the company**, used by Intent Solutions
personnel to monitor, manage, and govern the company's products, infrastructure, and AI
systems. Every operational capability developed throughout this program is evaluated not
only as infrastructure automation but **as a future feature of this internal platform**,
including: infrastructure status, environment health, incident management, monitoring
dashboards, alert management, backup status, restore verification, disaster-recovery
readiness, security posture, deployment management, AI agent management, repository health,
CI/CD status, service catalog, operational runbooks, architecture documentation, change
management, operational metrics, executive dashboards, cost dashboards, audit history, and
compliance reporting.

A future phase introduces the authenticated portal with **role-based access control
(RBAC)**, providing visibility appropriate to a user's responsibilities. Future roles
include: Executive Leadership, Operations, Platform Engineering, Infrastructure Engineering,
Security, AI Engineering, Product Engineering, Customer Support, Incident Commanders,
On-Call Engineers, and Contractors (limited access). Every feature implemented today is
evaluated for how it could eventually appear inside this application.

## 6. Standing articles (Jeremy Longshore, 2026-07-10 — preserved near-verbatim)

These four articles are the program's doctrine. Future epics cite them by article number.

### Article I — Multi-Phase Program Awareness

> This program is intentionally divided into multiple implementation phases. The current
> phase represents only one portion of a much larger long-term architecture. Always assume
> additional phases are coming. Do not optimize only for the current phase. Design every
> decision so it naturally supports future expansion without requiring major architectural
> rewrites. If a short-term implementation would create technical debt or make future
> phases more difficult, recommend a better long-term approach instead. Every architectural
> decision should consider the complete Mission Control vision.

### Article II — Forward Compatibility (the 12-question rubric)

> When making recommendations, continuously ask:
>
> 1. Will this architecture scale to future phases?
> 2. Will this require a rewrite later?
> 3. Can this component become a reusable platform service?
> 4. Can this eventually power the internal Mission Control dashboard?
> 5. Does this support multiple environments?
> 6. Does this support additional products?
> 7. Does this support additional servers?
> 8. Does this support additional AI agents?
> 9. Does this support additional engineering teams?
> 10. Does this support future automation?
> 11. Does this support future APIs?
> 12. Does this support future web interfaces?
>
> Prefer designs that may require slightly more effort today if they significantly reduce
> future complexity.

This checklist is the roadmap's **per-decision rubric**: every epic-level design choice in
the program roadmap (`037-PP-PLAN`) records its answers to these twelve questions, or states
in one line why the rubric doesn't apply.

### Article III — Phase Awareness

> The current implementation phase is only one milestone in a much larger roadmap. Always
> maintain awareness that additional phases will follow. Do not assume that functionality
> omitted from the current phase has been forgotten. Instead, identify dependencies that
> should be established now to make future implementation straightforward. If you discover
> that a future phase should be partially enabled during the current phase (for example, by
> defining interfaces, schemas, APIs, data models, extension points, or repository
> structure), recommend doing so while keeping implementation appropriately scoped. When in
> doubt, optimize for extensibility rather than expediency.

Corollary (program rule): partial enablement is **explicit, never silent**. A phase that
declines to pre-build an interface for a later phase says so in its AAR; a phase that
pre-builds one names the future consumer.

### Article IV — Architectural Responsibility

> Your responsibility is not simply to complete the current phase. Your responsibility is
> to ensure that each completed phase becomes a stable foundation for every phase that
> follows. Treat every architectural decision as if Intent OS will continue evolving for
> many years and eventually become the central operational platform used across all Intent
> Solutions products, infrastructure, services, and engineering teams.

### Article V — Standing Infrastructure Assumption (Jeremy Longshore, 2026-07-11)

> **Binding on every future phase, epic, and technology decision. Change only with Jeremy's
> explicit approval.** Design Mission Control around this operating model.
>
> **Production environment.** Intent Solutions maintains a dedicated production server capable
> of self-hosting operational infrastructure. When evaluating technologies, always assume this
> server is available to host supporting platform services. Do not default to SaaS because it is
> easier — evaluate self-hosted, open-source alternatives first.
>
> **Sufficient-resources assumption.** Assume sufficient production resources to run supporting
> infrastructure. Do **not** reject a high-quality open-source component merely because it uses,
> say, an extra 500 MB of RAM if the production server has the capacity. Optimize first for
> **maintainability, reliability, and long-term architecture**; resource optimization is driven
> by *actual, measured* constraints, never assumed up front. If capacity ever becomes a
> constraint, document it with measurements rather than pre-emptively minimizing every service.
>
> **Evaluation order — for every platform capability, in this order:** (1) an existing capability
> already running in the Intent Solutions estate; (2) existing open-source software that can be
> self-hosted; (3) lightweight commercial software with a self-hosted deployment option; (4) SaaS
> only when it provides significant operational advantage outweighing vendor lock-in, recurring
> cost, operational dependency, data-ownership, security, and loss of platform control. Every SaaS
> recommendation must explicitly justify why it beats an appropriate self-hosted alternative.
>
> **Self-hosted-first principle.** Mission Control must be capable of operating independently of
> third-party vendors whenever reasonably practical. Prefer technologies with: open-source
> licensing, active communities, long-term sustainability, strong documentation, API-first
> architecture, containerized deployment, health monitoring, and backup / upgrade / DR support.
>
[Operational detail retained in the private record]
>
> **Operational philosophy.** Mission Control is the company's long-term operational platform.
> New open-source components become **managed platform services inside Mission Control**, not
> isolated standalone tools, whenever practical. Every adopted dependency ships with a long-term
> operational plan — installation automation, configuration management, health monitoring, backup,
> upgrade, rollback, documentation, ownership, lifecycle management, and AAR requirements. **No
> technology is introduced without a long-term operational plan.**

## 7. The integration contract

Every future product, service, or capability that joins the estate signs up to:

1. **Registered:** its scheduled automations appear in `mission-control/automations.md`
   before the session that creates them ends (machine-enforced today).
2. **Observable:** it emits liveness (two-marker `.beat`/`.ok` protocol or equivalent) and
   routes failures through the notify spine — never a private alerting path.
3. **Recoverable:** its backup/restore story is written and drilled, and its rollback
   procedure exists before it carries production traffic.
4. **Deployable:** it deploys from `origin/main` via CI (never from a mutable working
   tree), with a smoke test and a rollback path.
5. **Tracked:** its work is beads-tracked and mirrored (bead ↔ GitHub ↔ Plane).
6. **Documented:** it complies with `039-DR-STND` (docs as first-class deliverable; AAR at
   epic close; executive package to the reports feed).
7. **Service-shaped (rising bar):** it exposes its state machine-readably per § 4.1 — new
   capabilities from Phase 1 onward must; existing capabilities are brought up to this bar
   per the roadmap, not all at once.
8. **Secret-safe:** secrets ride SOPS/age in-repo, never plaintext; and its documents obey
   the disclosure tiers (no compensation/PII anywhere; public surfaces get the public-tier
   scrub).

## 8. Relationship to doctrine-v1

`doctrine/doctrine-v1.md` governs **conduct** — values, standards, commitments, how the
company behaves. ADR-000 governs **operations** — how the estate is built and run. They are
siblings under the same roof: doctrine says who we are; ADR-000 says how the machines and
programs are organized. Where they touch (disclosure tiers, no-PII-in-the-brain), doctrine
wins on conduct and ADR-000 defers to it explicitly.

## 9. Amendment process

- ADR-000 is amended by **appending a dated amendment section** (never by silent edit),
  landed via PR with Jeremy's approval, plus a decision-log entry.
- An epic that needs an exception records it in the decision log with its scope and expiry;
  two exceptions to the same clause trigger a review of the clause itself.
- Superseding this ADR entirely requires a successor ADR that names everything it inherits
  and everything it retires, per `039-DR-STND` § 1.

## 10. References

- `037-PP-PLAN-mission-control-program-roadmap` — the revised program roadmap governed by
  this ADR
- `039-DR-STND-epic-documentation-aar-and-reporting-standard` — the documentation law
- `031-AA-AACR-estate-automation-remediation-program-2026-07-10` — the estate ground truth
  at ADR adoption
- `003-DR-STND-intent-os-content-schema` + `/doc-filing` v4.4 — where documents live
- Mission Control reports feed: `https://demos.intentsolutions.io/mission-control/`
  (public, scrubbed mirror of program records)

## 11. Alternatives considered (added per audit finding C25)

An ADR records the roads not taken. The Phase-0 discovery and audit weighed these:

- **Keep the estate as bash + cron + markdown, no platform ambition.** Rejected: it is
  operationally excellent but cannot become a queryable, authenticated control surface — the
  service-ability axis (`035` Part A) is where every capability scores low, and no amount of
  more-bash closes it.
- **Adopt an off-the-shelf ops platform (OneUptime, a SaaS status/incident suite).** Rejected
  on evidence (`035` Part B): OneUptime is a 3–6+ GiB monolith whose two unique features cost
  ~0.15 GiB elsewhere; SaaS suites re-introduce the vendor lock-in and cost surface the estate
  just shed with the GCP exodus.
- **Federate the VPS runbook and intent-os permanently (no merge).** Rejected for the docs
  (duplication across ≥4 places was found live-drifting) but **retained for the secrets file**
  (§ amendment 12, J1b) — the strongest architecture merges the prose and federates the crown
  jewels.
[Operational detail retained in the private record]

## 12. Consequences and accepted tradeoffs (added per audit finding C25)

Adopting this constitution commits the estate to real, named downsides:

- **Ceremony cost.** Documentation-as-first-class-deliverable and the AAR/executive-package
  discipline cost operator time. Mitigated by the tiered ceremony (`039` §7 amendment) — but
  the cost is real and accepted.
[Operational detail retained in the private record]

## 13. Amendment 2026-07-11 — corrections from the adversarial audit (`040`)

1. **Ninth integration-contract clause (§7).** Add: *"9. Supported — the capability declares
   its version, its support window, and a named patch owner."* Closes the dependency-lifecycle
   gap (`040` C12).
2. **RPO/RTO + last-drill-date join the §7 contract.** Every data-bearing capability states its
   recovery-point and recovery-time objectives and the date of its last restore drill (`040`
   C2/C3).
3. **Action-audit event schema is a contract requirement.** Any capability that performs
   privileged actions emits an append-only audit event (subject / action / resource / timestamp
   / actor-type / outcome); capture begins in Phase 1, not at portal build (`040` C19).
4. **The end-state role model biases to 3 real roles.** Article 5 keeps the 11-role list as
   illustrative prose; the *implemented* authorization model is 3 roles (admin/operator,
   on-call/member, scoped-read contractor) until a documented user-count trigger justifies
   more. Never encode 11 roles as a schema for a ~3-human estate (`040` C7).
[Operational detail retained in the private record]
6. **Article II's 12-question rubric is enforced in a followable form.** The rubric applies at
   the *epic* level, answered tersely (one line per applicable question, "n/a" allowed with a
   reason) — not as a heavyweight block on every decision. An unfollowed enforcement clause is
   worse than an honest lighter one; the roadmap (`037`) is the reference (`040` C15).
7. **"Never a rewrite" is conditional.** §4.1's promise that the portal is additive over
   platform services holds *iff* every schema has a validating consumer and an additive-only
   evolution rule (`040` C9). Schemas without enforcing consumers do not earn the guarantee.
8. **Federate-the-secrets is the panel's engineering recommendation on the merge** (§11); the
   final call is Jeremy's (J1b) and is recorded either way.
