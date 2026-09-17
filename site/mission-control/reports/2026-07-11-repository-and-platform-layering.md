> Historical July 11, 2026 planning record. Public copy redacted September 17, 2026 to remove operational details; original retained privately. This is not current operational status.

# 046-AT-ARCH — Repository and platform layering, and the repo-split decision criteria

> **What this is and why it matters.** Two things in one document, both about structure. First,
> **one picture** of how Mission Control is layered — from the Intent OS repository at the top
> down to the AI services at the bottom — so anyone can see how the pieces stack and which
> layer a given concern belongs to. Second, a **decision rule for growth**: when a new thing
> should become its own repository versus a service, a package, or just a module in what already
> exists. Without that rule, a growing platform sprawls into dozens of repos nobody can hold in
> their head. This is the anti-sprawl charter.

- **Program:** Mission Control (constitution: `038-AT-DECR`)
- **Companion:** `034-AA-AUDR` (the runbook-merge recommendation this generalizes), `037` (roadmap)

---

## 1. The layered stack (one picture)

Each layer depends only on the layer below it; the portal and AI services sit on top of the
platform, never beside it. This is the shape ADR-000's "platform-before-UI" principle produces.

```mermaid
graph TD
    IOS["Intent OS — the repository and control plane of record"]
    OPS["Operations — deploy, backup, monitoring, incident, security procedures"]
    MC["Mission Control — the capability layer (each capability = a service)"]
    SCH["Schemas — the canonical data contracts (Service/Host/Environment, incident, alert, audit)"]
    RB["Runbooks — how a human or agent operates and recovers each capability"]
    AUTO["Automation — the scheduled jobs, sweeps, watchdogs, and deploy pipelines"]
[Operational detail retained in the private record]
    PORTAL["Portal — the authenticated RBAC web application (a UI over the services)"]
    AI["AI Services — governed agents, the brain, LLM-assisted operations"]

    IOS --> OPS
    OPS --> MC
    MC --> SCH
    SCH --> RB
    RB --> AUTO
    AUTO --> INFRA
    PORTAL -.->|"reads the platform services, never bypasses them"| MC
    AI -.->|"governed actors that call platform services under the same contract"| MC
```

**What to notice.** The portal and AI services attach with dashed edges *into the capability
layer* — they are consumers of the platform, not new foundations. Schemas sit directly under
the capabilities because every capability exposes its state through a schema (the API-first
principle). Infrastructure is at the bottom: everything above it is how we operate it, not what
it is.

## 2. Where a concern belongs (which layer)

| If the concern is… | it lives in the… | example |
|---|---|---|
| how the company is governed / the record of decisions | Intent OS repo (top) | ADR-000, this doc |
| a procedure a person/agent follows to run or recover something | Runbooks | RESTORE, break-glass |
| a scheduled job that runs unattended | Automation | liveness sweep, backup |
| a data contract other things read/write | Schemas | the incident record |
| a named capability with an interface | Mission Control | backups, incidents, deploys |
| the machines and networks themselves | Infrastructure | the VPS, the tailnet |
| a screen a human looks at | Portal | the executive dashboard |
| an autonomous actor | AI Services | a governed agent |

## 3. The growth decision: repo vs service vs package vs module

When something new needs a home, walk this in order and stop at the first "yes":

1. **A module** (a file/directory inside an existing repo or service) — the default. Choose it
   when the new thing shares the owner, release cadence, and deployment of its host, and is not
   independently reusable. *Most new work is a module. Bias here.*
2. **A package** (a versioned library, published or vendored) — choose it when the same code is
   needed by **two or more** independent consumers and benefits from its own version. A package
   is not a service; it has no runtime of its own. Example: a shared schema-validation library.
3. **A service** (its own runtime behind an interface, same repo or a new one) — choose it when
   the thing has an **independent lifecycle at runtime**: it scales, deploys, fails, or is
   secured separately from its neighbors, and exposes an API. Example: the read-only platform
   API, the incident service.
4. **A new repository** — the highest bar. Choose it **only** when at least two hold:
   - a **different access boundary** is required (e.g. secrets that must not co-locate with
     agent-read or public-adjacent content — the reason `034` federates the secrets file);
   - a **different owner or contributor set** with different permissions;
   - a **genuinely independent release cadence and CI** that would fight the host repo's gates;
   - it is a **shippable external product** (like the platform marketplace) with its own users.

   If none of those hold, it is a directory in Intent OS, not a repo. Repo count is a cost —
   every repo needs its own CI, governance, and mental model.

## 4. Applying the rule to today's estate

- The VPS runbook **merges into Intent OS** (`034`) — same owner, same cadence, no independent
  access boundary for the *docs* → a subtree, not a separate repo. Its **secrets file stays
  federated** — a genuinely different access boundary → the one justified split.
- The **schemas** (`037` Epic 1.4) are a directory (module) now; they become a **package** only
  if a second independent consumer needs them versioned.
- The **portal** is a **service** (its own runtime) in Intent OS, not a new repo, until it needs
  a different contributor set.
- The **platform marketplace** (`claude-code-plugins`) stays its **own repository** — a shipped
  external product with its own users and cadence. Correct by this rule.

## 5. Governance

- Any proposal to create a new repository cites this document and states which of §3.4's
  conditions it meets; if none, it is not a repo.
- The layering diagram is updated when a new layer or cross-layer edge appears — never let the
  picture drift from reality (the same discipline `033` applies to the infrastructure map).
