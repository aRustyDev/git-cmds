# SPEC 00 — Overview and purpose

> **Aspirational.** This SPEC states what should become true. It is not a report on an existing
> system — nothing here is built. See `~/.claude/rules/plans-and-docs.md` for why that distinction
> matters, and *How to read a requirement* below for what the status markers therefore mean.

- **Date:** 2026-08-20 · **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md), ratified before this prose
- **Consumer:** a Software Architect whose first two tasks are to identify the five flows and to
  decide the module shapes. This SPEC specifies **behaviour, not structure** — it names no crate,
  draws no module diagram and proposes no workspace layout, deliberately.

## Introduction

This SPEC specifies a **code-intelligence platform**: a system that parses repositories into a
queryable knowledge graph and serves that graph to humans over a web UI and to AI agents over an
agent protocol, in two deployment shapes — a local CLI named `git-ctx`, and a Kubernetes-native
microservice.

The reusable engine library is written **`<ENGINE>`** throughout and is deliberately unnamed. It is
not a placeholder awaiting a guess: naming it is gated on sync **B6**, because a library name is a
claim about scope and scope is exactly what the seam work decides (`questions/0001`).

## Purpose

### The problem

Codebases exceed what anyone can hold in their head, and the available tools answer the wrong shape
of question. Text search finds string occurrences. A language server answers about the open file.
Neither answers *what breaks if I change this*, *what path connects this route to that write*, or
*which files does my diff actually reach* — because those are questions about a graph, and no graph
exists.

Two consequences follow, and the second is the one that makes this hard:

1. **The questions require a persistent, queryable structure**, built by parsing and cross-file
   resolution, held in stores that suit each access pattern.
2. **The answers must carry their own trustworthiness.** An empty result meaning "nothing is
   affected" and an empty result meaning "the analysis could not see" are the same bytes unless the
   system is built to separate them. A consumer that cannot tell them apart is unsafe, and an agent
   is exactly such a consumer, because it cannot read a prose caveat.

### Target users

Five audiences, specified in full in [`01-personas-and-flows.md`](01-personas-and-flows.md):
developer/engineer · AI agent · platform administrator · non-technical stakeholder · platform
developer or integrator.

The distribution is unusual and drives the design: roughly **20–50 humans and up to ~10 000 agents**,
the agents predominantly read-only. Agents are the majority consumer by request volume and the
minority by request variety.

### Value proposition

- **For a developer:** the change-safety question answered before the change, and unfamiliar code made
  navigable by relationship rather than by filename.
- **For an agent:** a bounded, machine-readable, attributable interrogation surface over a whole
  codebase, with stable identifiers between calls and an explicit inconclusive state.
- **For an administrator:** one deployment serving an unbounded number of repositories, with
  per-principal identity and an audit trail that answers who asked for what.
- **For the organisation:** the capability without a per-seat licence whose unit of measure — a seat —
  has no meaning for the primary consumer.

### Constraints, in brief

Stated fully in [`06-constraints.md`](06-constraints.md). The four that shape every other section:

- **AGPL-3.0**, with linkability and §13 consequences that bear directly on the library/SDK/binary split.
- **Clean room** — no reference-implementation source may be read by any implementer.
- **Deployment duality** — two shapes, one design.
- **Six swappable store slots**, each embedded-or-networked, with no business-logic change.

## How to read a requirement

Every requirement is written:

```text
### <PREFIX>-<n> — <Component> MUST <do X>. *(status)*
```

**The status marker records the strength of the requirement's justification, not implementation
status.** This differs from a graduated spec, where the same marker reports observed reality. The
divergence is deliberate and is stated here so no reader mistakes `(VERIFIED)` for "already working":

| Marker | Means |
|---|---|
| `(VERIFIED)` | The **need** is evidenced by a measurement. Used for the eleven inherited negatives, where a specific failure mode was measured in prior art, and for constraints measured in this estate. |
| `(assumed)` | Requester-asserted, or inferred from another requirement. Nobody measured it. The honest default for a greenfield capability. |
| `(operational)` | Follows from how the system must be run rather than from what it must do. |
| `(satisfied by design)` | The requirement is that no mechanism exist, or it follows necessarily from a decision recorded elsewhere. |

Every requirement additionally carries:

- an explicit **MUST**, **SHOULD** or **WON'T** — RFC-2119 senses, with **WON'T** meaning a
  deliberate, recorded exclusion rather than an omission;
- a **verification method** — how anyone would establish the requirement is met. A requirement nobody
  can test is a wish, and it does not belong here;
- where relevant, an **applies-to** note naming the deployment shape or shapes. Per-requirement
  applicability is tabulated in `analysis/0005-deployment-shape-contrast.md`.

Requirements marked **inherited-negative** exist because a failure was measured, not imagined. The
tag is load-bearing: it tells the architect which requirements are non-negotiable on evidence, and
which are open to being argued down.

### Identifier registry

Global per prefix, sequential, never reused. Numbering gaps are expected and are noted rather than
renumbered.

| Prefix | Carries | File |
|---|---|---|
| `BR-` | Business requirements | this file |
| `FR-` | Functional requirements | `02-functional-requirements.md` |
| `PERF-` | Performance budgets | `03-non-functional-requirements.md` |
| `SCALE-` | Scale targets | `03-non-functional-requirements.md` |
| `COR-` | Correctness properties | `03-non-functional-requirements.md` |
| `OPS-` | Operability, including telemetry | `03-non-functional-requirements.md` |
| `REV-` | Reversibility | `03-non-functional-requirements.md` |
| `IF-` | Interface requirements, all surfaces | `04-interfaces-and-external-systems.md` |
| `EXT-` | External-system and store-slot requirements | `04-interfaces-and-external-systems.md` |
| `SEC-` | Security requirements | `05-security-requirements.md` |
| `CON-` | Design and implementation constraints | `06-constraints.md` |
| `US-A/D/G/N-` | User stories: admin, developer, agent, non-technical | `07-use-cases.md` |
| `UC-` | Stepped use cases | `07-use-cases.md` |
| `QA-` | Testing and documentation requirements | `08-testing-and-documentation.md` |

A functional capability `CAP-0nn` in `analysis/0001-capabilities.md` maps to `FR-0nn` with the same
trailing number. That alignment makes the two-way traceability audit mechanical.

## Business requirements

### BR-1 — The platform MUST deliver the capability without a per-seat licence. *(VERIFIED)*

**MUST.** The primary consumer is an agent fleet of up to ~10 000. Per-seat pricing has no defensible
unit of measure against that population, which is why acquiring the reference implementation's
commercial licence was assessed as a poor fit independent of its cost.

**Verification:** the delivered artefacts are licensed AGPL-3.0 and carry no runtime licence check,
no seat count and no entitlement call. Verified by inspection of the published crates and by the
absence of any network call at start-up other than to configured stores and providers.

### BR-2 — The platform MUST be usable for internal commercial work without a licence negotiation. *(VERIFIED)*

**MUST.** This is the requirement the whole effort exists to satisfy. The reference implementation's
licence enumerates permitted purposes and a for-profit commercial organisation is not among them; its
licensor confirmed that reading in writing.

**Verification:** the licence of every dependency permits internal commercial use. Enforced as a
release gate — see `QA-14` — not as a one-time review.

### BR-3 — The platform MUST NOT be a derivative of the reference implementation. *(VERIFIED)*

**MUST.** PolyForm's *No Other Rights* clause forbids sublicensing, so a derivative work could not be
released under AGPL-3.0 at all. The clean room is therefore what makes the licence choice coherent,
and is a legal requirement rather than a hygiene preference.

**Verification:** the clean-room protocol in `CON-1`, plus the laundering audit recorded in this
plan's handoff. Every implementer attests they have not read reference source.

### BR-4 — The platform MUST serve both a single developer and an organisation from one design. *(assumed)*

**MUST.** Two deployment shapes. The business reason is that adoption starts with one engineer
running a binary and only later becomes a funded service; a design reachable only at the service end
never gets adopted, and one reachable only at the local end never gets funded.

**Verification:** `G9` in the PRD — the local shape ships with no network listener and no
authentication, and the service shape shares its analysis code rather than forking it. Proven by both
shapes passing the same behavioural suite (`QA-9`).

### BR-5 — The platform SHOULD reduce the number of tools that must be operated to cover the capability. *(assumed)*

**SHOULD.** The assessed alternative to building was a composition of three or four permissively
licensed tools — three deployments and a unifying facade — covering roughly two-thirds of the
capability. Consolidation is a real benefit and is worth stating, but it is not worth compromising a
MUST for.

**Verification:** the capability inventory in `analysis/0001` is served by one deployment per shape.
Counted, not asserted.

## Product overview

### How it works

Four stages, named here so later requirements can refer to them without re-describing them. **These
are stages of behaviour, not modules** — where the seams fall is the architect's decision.

1. **Acquisition.** A repository is obtained: found on local disk in the local shape, or fetched from
   a remote in the service shape, with credentials for private remotes.
2. **Ingestion.** Files in scope are detected, parsed per language, and extracted into nodes and
   edges. Cross-file resolution links what single-file parsing cannot. Change detection decides —
   **before** the expensive work — what actually needs redoing.
3. **Derivation and persistence.** Whole-graph computation produces **flows** and **clusters**;
   embeddings and lexical indexes are built; everything is written to the store slots that suit it,
   under an **index generation** marker.
4. **Serving.** Readers arrive over the CLI, the API, the agent protocol or the web UI's contract.
   Every one of them is answered from one internal contract, receives the **index generation** and
   freshness alongside the answer, and — for anything that walks the graph — the **three-state
   result**.

### Key features

Grouped as the capability inventory groups them; each links to its requirements.

| Group | What it provides |
|---|---|
| **Graph and query** | Read-only openCypher-style queries; hybrid search fusing traversal, lexical and semantic ranking, grouped by flow; a 360-degree symbol view; node/edge filtering; N-hop neighbourhoods; counts; sub-directory scoping; read-only structural checks; a generated repository wiki. `FR-020`–`FR-036` |
| **Change analysis** | Reachability with a witness path; depth-bounded transitive blast radius; downstream reachability; diff impact from a working tree, a `base...head` pair, or a **supplied patch with no checkout**. All under the three-state contract. `FR-023`–`FR-028` |
| **Web and API structure** | Route-to-handler and RPC/tool-definition mapping; response-shape conformance against consumer property accesses; a pre-change report for a route handler. `FR-007`, `FR-008`, `FR-034`, `FR-035` |
| **Repositories and groups** | Paginated discovery; repository switching; simultaneous multi-repository serving; groups with a contract registry and cross-repository links, carrying **evidence class**. `FR-040`–`FR-047` |
| **Write operations** | Coordinated multi-file rename — AST-accurate, with mandatory index writeback. `FR-050` |
| **Platform** | Six swappable store slots; embedding-provider selection; queued durable cancellable indexing; per-principal identity, authorisation and audit; telemetry sufficient to verify the budgets; upgrade without reindex. `EXT-*`, `SEC-*`, `OPS-*`, `FR-068`, `FR-071`, `FR-073` |
| **Deferred to v2** | Statement-level **dependence**; persisted **taint** findings and their explanation. Specified as `WON'T` with the seam named. `FR-037`, `FR-038` |

## The deployment duality is a first-class force

**Two shapes, one design.** Not two configurations of one design — two points a single design must
reach. This is stated here, in the overview, because it is the force most likely to be quietly
resolved into "the service shape with flags off", and that resolution would be wrong in both
directions: the local binary would carry a job queue, an authentication stack and a network listener
it has no use for, and the service would inherit assumptions about a current working directory that
do not survive a request arriving over the network.

| Dimension | Local shape | Service shape |
|---|---|---|
| Users | one | ~20–50 humans, up to ~10 000 agents |
| Authentication | none | per-principal, mandatory |
| Stores | embedded, in-process | networked, external, independently operated |
| Network listener | none required | required |
| "Current repository" | resolved from the working directory | **does not exist** — every request names its repository |
| Indexing | may run in the foreground | queued, durable, cancellable, observable |
| Telemetry | optional | required |
| Concurrency | one reader | reads scale with readers per replica |
| Failure of a store | fatal, local, visible | partial, remote, must degrade explicitly |

### CON-2 — Business logic MUST NOT differ between deployment shapes. *(assumed)*

**MUST.** The same question asked of the same index MUST return the same answer in both shapes. The
shapes may differ in what is *reachable*, what is *authenticated* and what is *queued* — never in
what an analysis concludes.

**Verification:** one behavioural conformance suite, run against both shapes, asserting identical
answers for a fixed corpus and query set (`QA-9`). A divergence is a defect in the shape, not a
documented difference.

**The consequence we dislike:** this forbids the cheap optimisation of letting the local shape take
shortcuts the service shape cannot — for example, reading the working tree directly where the service
must consult the index. Those shortcuts are exactly how two implementations of one behaviour appear,
and the prior art demonstrates where that ends: two entry points to nominally the same functionality
with different authentication, different concurrency behaviour and different operation inventories.

### Which stores must be swappable without touching business logic

All six slots (`EXT-1`–`EXT-6`). The graph, vector and relational slots are the ones every deployment
needs; the search, text-search and key-value slots are optional and currently have **no consuming
capability** (`GAP-011`).

House precedent, **cited as precedent and not mandated**: the estate puts all persistence behind a
repository trait with no concrete datastore type in the public API, and uses per-backend feature flags
with an in-memory default so tests need no external engine. Whether that is the right shape here is
sync **B2**'s decision.

## The async question is load-bearing and is not settled here

House convention: *if any candidate backend is async-only, the trait is async and everything above it
inherits that — resolve during screening, not after; retrofitting async through a synchronous trait
is a rewrite.*

**This SPEC does not decide it.** It is filed as `questions/0003` and owned by sync **B7**, and
`analysis/0004-store-capability-matrix.md` records, per candidate, whether it forces the answer. The
requirement here is only procedural:

### CON-3 — The async decision MUST be recorded before the first store implementation is written. *(operational)*

**MUST.** Not before the SPEC is approved, and not after a backend exists — during backend screening.

**Verification:** an ADR exists, with a status of accepted, dated earlier than the first commit
implementing a store backend. Checkable from history.

## Not yet specified

Honest gaps in this file, carried rather than papered over:

- **Which projections blast radius must support** is listed in `FR-024`, but whether they share one
  traversal or several is the module seam and belongs to the architect (`discussions/0001` axis 6).
- **The default edge set** for each analysis capability. Highest-leverage single decision in the
  analysis surface, and it sets both the false-positive rate and the cost. Owned by sync **A5**.
- **The system of record** across the six stores. Sync **B4**.
- **Whether derived identities must be stable across runs** (`questions/0004`). It changes whether
  `FR-018` is a cost requirement or a correctness requirement.

## Verification

### What is proven

- **The vocabulary predates this prose.** [`GLOSSARY.md`](../GLOSSARY.md) was written and ratified
  first, satisfying the A2 hard gate. Checkable from commit order.
- **The status-marker semantics are stated before any requirement uses them**, so no reader can
  mistake `(VERIFIED)` for "implemented".
- **The identifier registry is complete** with respect to the files in this SPEC, and the
  `CAP-0nn`→`FR-0nn` alignment is mechanical.
- **The deployment-duality contrast table is derived from the requester's own two shapes** and names
  a concrete asymmetry — the absence of a "current repository" in the service shape — that the
  capability list assumed away.

### What is NOT proven

- **That the business requirements are the requester's business requirements.** `BR-1`–`BR-5` are the
  requirements author's reconstruction from the licensing verdict and the stated scale profile.
  Nobody has confirmed them. Sync **A1** is where they are tested.
- **That both shapes are reachable from one design.** This is the central architectural bet of the
  document and it is asserted, not demonstrated. It cannot be demonstrated before there is a design.
- **That the n95 budget in `03` is achievable** at the scale target. No measurement exists; there is
  nothing built to measure. `GAP-004` records that the budget is currently unverifiable at all,
  because there is no telemetry.
- **That the local shape genuinely needs no authentication.** Asserted from "single user on their own
  machine". If the local shape ever serves the web UI on a listening socket, that assertion fails and
  `SEC-*` applicability changes.

## Amendments

- **2026-08-20** — Created, after the glossary and the capability inventory, in that order.

## Related

- [`../PRD.md`](../PRD.md) — problem, goals, out-of-scope by name, and how we will know we were wrong.
- [`../GLOSSARY.md`](../GLOSSARY.md) — ratified vocabulary.
- `analysis/0005-deployment-shape-contrast.md` — per-requirement applicability across the two shapes.
- `questions/0003-the-async-decision.md` — the decision this file deliberately does not take.
