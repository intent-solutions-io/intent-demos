# 044-DR-STND — Definitions of Done: bead, epic, phase, program

> **What this is and why it matters.** "Done" means different things at different altitudes,
> and conflating them is how work looks finished when it isn't. A **bead** (one task) is done
> when its change works and is documented. An **epic** (a cluster of beads delivering one
> capability) is done when the capability is operable, recoverable, and has its after-action
> report. A **phase** is done when its epics are done *and* leadership has signed off. The
> **program** is done — years from now — when the platform reaches its end-state. This document
> writes each level's checklist so a stranger can tell, objectively, whether something is
> complete. It pairs with the per-epic acceptance tests in the roadmap (`037`) and the
> documentation law (`039`).

- **Program:** Mission Control (constitution: `038-AT-DECR`)
- **Companion:** `039-DR-STND` (documentation/AAR standard), `037-PP-PLAN` (per-epic acceptance tests)

---

## 1. Definition of Done — a bead (one task)

A bead is done when **all** are true:

- [ ] The change works, verified by exercising it — not just "it should work."
- [ ] Its acceptance criteria (if it has any) are met, with evidence linked (CI run, log,
      transcript) — "verified" without a link does not count.
- [ ] Any doc the change touches is updated in the same change; stale docs are not left behind.
- [ ] It passes the repo gates (disclosure, beads-validate, lint, secret scan).
- [ ] It is closed via `bd-sync` with an evidence reason, mirroring to its GitHub/Plane issue.
- [ ] If it created or changed a scheduled automation, the automations registry row exists.

## 2. Definition of Done — an epic (one capability)

An epic is done when **all** are true:

- [ ] Every child bead is done (§1) or explicitly deferred with a written reason and a bead.
- [ ] The epic's roadmap **acceptance test** (`037`) passes, with the evidence linked.
- [ ] The capability is **operable from its documentation** by someone who has not seen it:
      architecture/design doc, operating guide/runbook, install/upgrade/migration notes,
      rollback + recovery procedure, security considerations, known limitations (`039` §2).
- [ ] It meets the ADR-000 §7 **integration contract**: registered, observable, recoverable,
      deployable, tracked, documented, service-shaped (for Phase-1-onward capabilities),
      secret-safe — and declares its version + patch owner + RPO/RTO where applicable.
- [ ] Its **KPIs** (`043`) have a data source, or one is filed as a Phase-signal bead.
- [ ] A **9-section AAR** is filed (full lane) or the lightweight lane is justified per `039` §7.
- [ ] The GitHub cluster issue and Plane issue are settled via `bd-sync`.

## 3. Definition of Done — a phase

A phase is done when **all** are true:

- [ ] Every epic in the phase is done (§2), or deferred with written justification carried into
      the next phase's scope.
- [ ] The phase's **exit checklist** (Phase 0's is `051`; later phases get their own) is fully
      ticked.
- [ ] The **risk register** (`041`) and **risk heat map** (`045`) are reviewed and updated —
      risks retired, new risks added, owners current.
- [ ] The roadmap (`037`) is updated to reflect what actually shipped vs planned (superseded
      sections marked, not deleted).
- [ ] A **phase-close AAR** + the **10-part executive package** are filed and published to the
      reports feed (governance/planning layer; security detail held back).
- [ ] **Executive (Jeremy) sign-off** is recorded in the decision log — a phase is not done on
      the engineer's say-so.

## 4. Definition of Done — the program

The program is done when **all** are true (this is the far horizon, stated so it is not
forgotten):

- [ ] The end-state in ADR-000 §5 exists: an authenticated internal web application with
      role-based access control, over stable platform services — not a pile of scripts.
- [ ] Every capability domain in the KPI catalog (`043`) is service-shaped, observed, and meets
      its target on its cadence.
- [ ] Disaster recovery is proven, not asserted: an off-site immutable backup, a measured RTO
      within target, and a passing recovery drill on the standing quarterly cadence.
- [ ] Zero tribal knowledge: any competent engineer or AI can operate, troubleshoot, and extend
      the estate from Intent OS alone (the documentation law's whole point).
- [ ] The governance cadence (`050`) runs on its own rhythm without heroics, and the ADR log
      (`047`) is current.
- [ ] The program can absorb a new product, server, environment, agent, or team member by
      following the integration contract — no rewrite required (ADR-000 Article IV).

## 5. Why the four are not identical

A bead can be done while its epic is not (the capability isn't operable yet). An epic can be
done while its phase is not (leadership hasn't signed off, or a sibling epic is open). A phase
can be done while the program is decades from done. Keeping the levels distinct is what stops
"all the tasks are closed" from being mistaken for "the platform is finished."
