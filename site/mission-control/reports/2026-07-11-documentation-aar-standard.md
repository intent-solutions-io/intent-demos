# 039-DR-STND — Epic documentation, AAR, and reporting standard

> **What this is and why it matters.** This document turns a working habit into program law:
> at Intent Solutions, **documentation is a first-class deliverable — an implementation is not
> complete until its documentation exists.** It codifies three things every epic and major
> milestone must produce: (1) operating documentation another engineer can run the system
> from, (2) a formal **after-action report (AAR)** in a fixed 9-section format, and (3) an
> **executive reporting package** readable by technical leadership without opening the
> codebase. It exists because operational knowledge that lives only in one person's head — or
> one chat session's context — is a liability: it cannot be reviewed, handed off, audited, or
> taught. This standard is bound into ADR-000 (the Mission Control constitution) and applies
> to every phase of the Mission Control program, starting with Phase 0 itself.

- **Status:** Standing standard (Phase-0 deliverable; ratified by inclusion in the Phase-0 PR)
- **Applies to:** every epic, major milestone, and significant decision in the Mission Control
  program; recommended for all Intent Solutions repos
- **Authority:** Jeremy Longshore's documentation doctrine (2026-07-10), codified here;
  bound by reference into `038-AT-DECR` (ADR-000)
- **Filing:** all documents follow `/doc-filing` v4.4 (`NNN-CC-ABCD-description.md` in the
  repo's `000-docs/`, flat by default)

---

## 1. The rule

**Implementation is not complete until its documentation exists.** "Done" for any epic, bead
cluster, or significant decision includes the documentation listed below, written so that
another engineer can **operate, troubleshoot, and extend the work without tribal knowledge**.
Intent OS is the authoritative source of operational knowledge; a change that isn't
documented there hasn't finished landing.

Three corollaries:

1. **Docs stay synchronized with implementation.** A follow-up change updates its documents
   in the same PR, or the PR states explicitly why not (and files a bead).
2. **Superseded documents are explicitly marked** — a banner at the top naming the successor
   ("Superseded by `NNN-…` on YYYY-MM-DD"), never silently deleted or left ambiguous.
3. **Teaching-tool trait.** Every document opens with a plain-English "what this is and why
   it matters" paragraph and expands estate shorthand on first use. Documents double as
   teaching material for the education arm; write for a competent engineer who has never
   seen this estate.

## 2. What every epic must document

Produce the subset that applies — but the decision to skip a row is made out loud (one line
in the AAR's "Scope" section), never by omission:

| Document | Contents |
|---|---|
| Architecture & design | what was built, how it fits the existing estate, interfaces exposed |
| Operational guide / runbook | how to operate it day-to-day; playbooks for its failure modes |
| Install / upgrade / migration | how to stand it up again from nothing; how to move versions |
| Rollback & recovery | how to undo it; how to recover its data; validated, not theoretical |
| Security considerations | secrets touched, access paths, attack surface added or removed |
| Testing & validation results | what was verified and the evidence (linked runs/logs, not "verified") |
| Known limitations | what it deliberately does not do |
| Future improvements | deferred work, filed as beads and referenced by ID context, not bare IDs |

## 3. The AAR — 9-section template (mandatory at epic close)

Every epic and major milestone ends with a formal AAR filed as `NNN-AA-AACR-…` per
/doc-filing v4.4. The copy-pasteable canonical skeleton is
`000-AA-TMPL-after-action-report.md` (flat root of `000-docs/`, per the v4.4 rule that
`000-*` canonical files never nest) — /doc-filing names that file in its canonical tree but
ships no content, so the intent-os copy is the canonical source. The nine sections, in
order — none optional, "n/a" must be argued:

```markdown
# NNN-AA-AACR — <epic name> after-action report

> Plain-English opening: what this epic was and why it mattered.

## 1. Summary and business value
What shipped, in two paragraphs. What the company can now do that it could not before.

## 2. Scope — planned, completed, deferred
The original scope; what actually completed; what was deferred and WHERE it went
(bead/issue references). Explicitly list documentation rows skipped per §2 and why.

## 3. Architecture and tradeoffs
What was built and the shape it took. Every real alternative considered and why it lost
("chose X over Y because Z"). Interfaces/schemas exposed for future phases.

## 4. Verification evidence
What was tested/drilled and the LINKED evidence — CI runs, drill transcripts, logs,
before/after measurements. "Verified" without a link does not count.

## 5. Issues and root causes
What went wrong during the work, each traced to a root cause — not the proximate symptom.

## 6. Lessons learned
What we'd do differently; which of these became standing rules (and where they now live).

## 7. Operational impact, including cost
New/changed automations (with their automations.md registry rows), RAM/disk/runtime
footprint, money cost delta, on-call/attention burden delta.

## 8. Rollback procedure and validation
How to undo this epic's changes, and the evidence the rollback path was actually
exercised or why exercising it is impractical.

## 9. Next steps
The recommended follow-on work, dependency-ordered, each with its bead/issue reference.
```

## 4. The executive reporting package (mandatory at epic close)

Every epic/milestone also produces an **executive package** — professional Markdown readable
by technical leadership without inspecting the codebase. Ten parts:

1. Executive summary (one page: what, why, outcome)
2. Technical summary (what changed, at the architecture level)
3. Architecture updates (diagrams or deltas, if any)
4. Progress versus roadmap (where the program now stands)
5. Risks (new, changed, retired)
6. Blockers (what is stuck and on whom)
7. Decisions (made this epic; open and waiting, with the owner named)
8. Verification results (the evidence roll-up)
9. The AAR (linked, or inlined if short)
10. Recommended next steps

**Delivery (amended 2026-07-10 by Jeremy; hardened 2026-07-11 after the adversarial audit):**
the package is **published to the Mission Control reports feed** at
`https://demos.intentsolutions.io/mission-control/` — an append-on-top, newest-first
documentation feed whose entries are plain markdown, fetchable by third-party LLMs. It is
**not emailed** (the original doctrine said email; the feed supersedes it).

**The publish gate is default-deny (this is a security control, not a courtesy scrub).** The
adversarial audit (`040-AA-AUDR`, finding C5) established that a "scrubbed but complete"
operational document is reconnaissance: a public, LLM-crawlable SPOF map, dependency graph,
deploy topology, or threat model hands an attacker the estate. Therefore:

- **What may be published is an allowlist, not a blocklist.** Only a *separately authored,
  sanitized executive summary* goes to the public feed. The full discovery documents (SPOF
  analysis, dependency graphs, deploy internals, infrastructure topology, risk register with
  live mitigations) stay in the private repo and are **never** published, even scrubbed.
- **A hard-fail publish gate** rejects anything that is not an approved summary, and strips
  hostnames, public and tailnet IPs, secret names, credential paths, and any personal-device
  or individual identifiers as a backstop — but the primary control is the allowlist, because
  a blocklist cannot anticipate every sensitive fact.
- The authoritative unscrubbed versions stay in `intent-os/000-docs/`; the feed is a
  sanitized shop window, not a mirror. The feed directory's README carries the procedure.
- **Alternative Jeremy may choose (J10):** gate the entire feed behind the tailnet / the
  future RBAC portal, in which case full documents may be served to authenticated readers and
  the allowlist relaxes. Until he decides, the default-deny public posture holds.

## 5. Where documents live

Per `/doc-filing` v4.4 and this repo's content schema (`003-DR-STND`):

- **Dated records** (AARs, audits, plans, decision records, this standard) → `000-docs/`,
  flat, next free `NNN`.
- **Living documents** (runbooks, system maps, registries) → the named topical directory
  that owns them (`mission-control/`, `system-map/`, or the VPS runbook while it remains a
  separate repo).
- **Decisions** additionally get a `decision-log/` pointer entry (append-only, blessed
  `NNN-YYYY-MM-DD` scheme).
- Any new scheduled automation gets its row in `mission-control/automations.md` **before the
  session ends** (machine-enforced by the weekly reconcile + drift-check section E).

## 6. Compliance

- The PR closing an epic's last bead links the AAR and the executive package; reviewers
  treat a missing AAR exactly like a failing CI gate.
- Phase 0 of the Mission Control program is the first epic bound by this standard; its
  deliverables (`032`–`041`) and feed publication are the reference implementation.
- This standard is amended the same way ADR-000 is amended (see `038-AT-DECR` § amendment
  process): by a dated superseding section, never by silent edit.

## 7. Amendment 2026-07-11 — corrections from the adversarial audit (`040`)

The 10-agent audit produced six corrections to this standard; the default-deny publish rewrite
(§4) is the largest and already applied above. The rest:

1. **RPO/RTO/DR-drill clause in the AAR template.** Section 8 (rollback) and a new line in the
   operational-impact section must state the epic's effect on the estate's recovery-point and
   recovery-time objectives and cite the last relevant restore-drill date. Backups and DR are
   not "verified" without a measured RTO and a dated drill. (`040` C3.)
2. **Incident/runbook-class exception to the teaching-tool preamble.** Operational documents
   read during an incident — runbooks, playbooks, restore procedures — carry a **one-line
   purpose header**, not a teaching preamble. The teaching-tool trait (§1.3) applies to
   analysis, plans, and audits; it is a liability in a document someone reads at 02:00 while a
   stack is down. Author judges by class. (`040` C26.)
3. **Tiered ceremony (capacity control).** The full 9-section AAR + 10-part executive package
   is mandatory for **phase-closes and incident-bearing epics**. Routine epics use a
   **lightweight lane**: What · Why · Verification (with evidence) · Rollback · Next. This
   mirrors the estate's existing lightweight-vs-full PR lanes and prevents documentation-about-
   the-work from consuming the capacity to do the work on a solo-operator estate. (`040` C15.)
4. **Doc-freshness CI gate.** A blocking check fails when a generated page's snapshot date
   exceeds its declared SLA (the mission-control pages were 9 days stale against a 3-day SLA
   during discovery — the anti-drift program drifting on itself). The no-hook rule is amended
   to permit a scheduled `pnpm mc` regeneration or a CI freshness gate. (`040` C20.)
5. **A governed Estate Operator Day-1 runbook is required.** Onboarding knowledge that lives
   only in CLAUDE.md files (four of which sit outside intent-os and cannot be merged) becomes
   *referenced* from a single governed operator runbook, not canonical in scattered files.
   (`040` C26.)
6. **Every epic's AAR verification section targets its acceptance test.** Because the roadmap
   (`037`) now gives every epic a one-line measurable acceptance test, the AAR's §4 evidence
   is checked against that test — not against a prose goal. (`040` C11.)
