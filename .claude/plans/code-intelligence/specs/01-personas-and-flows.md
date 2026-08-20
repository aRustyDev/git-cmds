# SPEC 01 — Personas and the five flows

> **Aspirational.** Vocabulary as ratified in [`GLOSSARY.md`](../GLOSSARY.md).

- **Date:** 2026-08-20
- **Why this file exists:** the architect's first task is to identify the flows for Users, Admins,
  Agents, Data and Developers. This file is that deliverable. **The data flow and the developer flow
  are the two most often skipped**, so they are the two longest sections here.
- **Deliberately absent:** any statement about which component performs a step. Steps name
  *behaviour* and the stage it belongs to (acquisition · ingestion · derivation · serving), never a
  module.

## Personas

### P1 — Developer / engineer

The primary human user. Works in one repository at a time, occasionally two. Arrives with either a
name (a symbol, a file, a route) or a description ("the thing that retries failed webhooks"), and
leaves with either navigation or a change-safety verdict.

- **Volume:** low; tens of queries a day.
- **Latency sensitivity:** high. Anything above a second breaks flow and the tool stops being used.
- **Trust posture:** will read a caveat, but will not read two. A "nothing affected" that was really
  "could not determine" costs them a production incident.
- **What they will not do:** learn a graph query language, or configure a store backend.

### P2 — AI agent

The primary consumer by volume. Up to ~10 000, predominantly read-only.

- **Volume:** very high; many bounded reads per task, across a session.
- **Latency sensitivity:** moderate per call, severe in aggregate — a slow call multiplied by a fleet
  is a capacity problem, not an annoyance.
- **Trust posture:** **cannot read prose.** Every caveat it must respect has to be a field. An
  inconclusive result presented as a clean negative will be acted on.
- **Distinctive needs:** output budgeting; stable identifiers it can hold between calls; explicit
  freshness; an advertised inventory it can build an allowlist from; and attribution, so that when
  one of ten thousand agents does something surprising, it can be identified.

### P3 — Platform administrator

Runs the service shape. The only persona whose profile is write-dominated.

- **Owns:** repository acquisition and credentials; repository groups; store backends; the identity
  and authorisation integration; the AI-provider policy; index capacity and reindex scheduling.
- **Trust posture:** needs to know what the system is doing and what it decided not to do. A silent
  escalation from an incremental run to a full rebuild is, for this persona, the difference between a
  capacity plan and a surprise.
- **Failure modes matter most:** their mistakes take everyone else down.

### P4 — Non-technical stakeholder

Product, programme and engineering-management readers.

- **Wants:** the repository wiki; the cluster map as a picture; "which areas does this change touch";
  counts and trends.
- **Will not:** write a query, name a symbol precisely, or interpret a depth bound.
- **Consequence for the design:** every capability this persona touches needs a presentation that
  survives the removal of all graph vocabulary. That is a web-UI contract obligation, not a separate
  analysis capability.

### P5 — Platform developer / integrator

Builds on `<ENGINE>` directly, adds a language, or embeds the capability in another tool. A real user
before any other persona exists, because they are the ones who make the first three possible.

- **Wants:** a stable public contract; an extraction contract they can implement for a new language
  without forking; a conformance suite that tells them whether their store backend is correct; and
  an in-memory default so their tests need no external engine.
- **Constraint they inherit:** AGPL-3.0. Linking `<ENGINE>` means accepting it (`CON-4`,
  `questions/0005`).

## Flow U — the user flow

Five journeys, each ending in a state the user can act on.

### U1 — Find something described, not named

1. User expresses intent in natural language, scoped to a repository (and optionally a
   sub-directory).
2. **Serving** answers with hybrid search: graph traversal, lexical ranking and semantic ranking,
   fused by the single rank-fusion implementation, grouped by **flow**.
3. Results carry, per item: its location, the **flow** it participates in, and why it matched — which
   lane or lanes contributed.
4. User picks a result and continues into U2.

**Failure to handle:** the semantic lane is unavailable because no embedding provider is configured.
The result must degrade to the remaining lanes **and say so**, not silently return lexical-only
results as though they were hybrid.

### U2 — Understand a symbol

1. User names a symbol, or arrives from U1.
2. **Serving** returns the 360-degree view: categorised references (callers, callees, implementors,
   overriders, tests), and the flows the symbol participates in.
3. User filters by node type or edge class, or expands to an N-hop neighbourhood with N of their
   choosing.
4. User may scope the whole view to a sub-directory.

### U3 — Decide whether a change is safe

1. User has uncommitted work, or names a `base...head` pair.
2. **Serving** computes **diff impact**: the change set maps to symbols, and blast radius runs
   upstream under a stated edge set and depth bound.
3. Result is one of **affected** (with projections: symbols, files, flows, routes, tests, downstream
   repositories), **none affected**, or **undetermined**.
4. Every result states the edge set, the depth bound, whether the bound was a **correctness statement
   or a budget**, and the **index generation** it was computed against.
5. User may request a **witness path** for any individual reach.

**The requirement that makes this flow worth having:** step 3 must never present *undetermined* as
*none affected*. This is where the prior art's measured failure lands — a count-based verdict that
reported low risk for a symbol belonging to no precomputed grouping, however many direct callers it
had.

### U4 — Read the codebase as a document

1. User requests the repository wiki.
2. **Serving** generates it from the knowledge graph.
3. User navigates it without graph vocabulary. This is the P4 path as much as the P1 path.

**Open:** the wiki's output contract is the vaguest item in the capability list — static artefact,
live pages, or generated prose. Filed as `questions/0011`.

### U5 — Rename across files

1. User names a symbol and a new name, and requests a preview.
2. **Serving** determines the edit set from the graph, **AST-accurately** — never by text match — and
   returns the proposed edits.
3. User confirms. Edits are applied, **and the index is updated in the same operation.**
4. If any part fails, the user is told which, loudly. A partially-applied rename that reports success
   is the failure mode being designed out.

## Flow A — the admin flow

### A1 — Bring a repository under analysis

1. Admin supplies a repository location; for a private remote, a credential.
2. **Acquisition** obtains or updates it. The credential never appears in a process argument list, a
   log, or an error message.
3. Admin submits it for indexing. An **indexing job** is created, with an identity.
4. Job status is observable: admitted, running, complete or failed, with progress. It is **cancellable**.
5. Submitting a second repository concurrently **queues** it. It is not rejected.
6. The job survives a restart of the serving process — its state is durable, not in memory.

### A2 — Keep indexes fresh

1. Admin sees, per repository, the index generation, its freshness, and when it was built.
2. On request or on schedule, an update runs. **Change detection decides what to redo before the
   expensive work starts.**
3. If the run escalates to a full rebuild, **every condition that caused the escalation is reported**.
   A silent escalation is indistinguishable from incrementality that does not work.

### A3 — Choose and swap backends

1. Admin selects, per store slot, an embedded or a networked implementation.
2. The choice is configuration. **No business logic changes.**
3. Each backend passes the same conformance suite, so "swappable" is a tested property.

### A4 — Configure identity and authorisation

1. Admin integrates an external authentication provider (OAuth2 or JWT).
2. Admin optionally integrates an external authorisation decision point (RBAC, ABAC or ReBAC).
3. Every request thereafter carries exactly one **principal**.
4. If authorisation cannot be established, the request is **denied**. Unset configuration authorises
   nothing.

### A5 — Set the AI-provider policy

1. Admin configures the embedding and AI providers from deployment configuration.
2. Admin decides whether runtime configuration from the web UI is permitted at all.
3. When it is not permitted, the runtime path is **absent**, not merely hidden from the UI.

### A6 — Answer "who did that?"

1. Admin queries the audit trail for a principal, a target or a time range.
2. Every mutating and every security-relevant action is present, naming its principal.

### A7 — Manage repository groups

1. Admin lists configured groups.
2. Admin rebuilds a group's **contract registry** and its cross-repository links.
3. Cross-repository answers thereafter distinguish **observed** from **inferred** edges.

## Flow G — the agent flow

Structurally similar to Flow U and different in every detail that matters.

### G1 — Establish identity and discover the surface

1. Agent authenticates **as itself** — not as a shared deployment credential.
2. Agent retrieves the advertised inventory of operations. **The callable set equals the advertised
   set**, so an allowlist built from the advertisement is complete.
3. Agent discovers indexed repositories, paginated by limit and offset.

### G2 — Interrogate within a budget

1. Agent issues a bounded read, naming its repository explicitly. There is no ambient "current
   repository" in the service shape.
2. Response is truncated to an output budget where necessary, and **truncation is a field**, not a
   trailing ellipsis.
3. Response carries the **index generation** and freshness.
4. Identifiers in the response are stable enough to be used in the agent's next call. Which
   identifiers those are, for derived structures, is `questions/0004`.

### G3 — Analyse a change it has not checked out

1. Agent supplies a **patch** for a repository, without a working tree and without the service ever
   having cloned it — or supplies a `base...head` pair.
2. Diff impact returns the three-state result with projections.
3. The agent branches on the state field. `undetermined` is a distinct branch from `none affected`;
   this is the whole point.

### G4 — Perform the one write it has

1. Agent requests a rename preview.
2. Agent applies it. The index is updated in the same operation.
3. The action appears in the audit trail, attributed to that agent.

### G5 — Behave under load

1. Many agents read the same replica concurrently.
2. Throughput scales with readers. Concurrent independent reads do not serialise into a queue.
3. A read during an active index run either succeeds against a consistent generation, or fails
   explicitly. **It never observes a torn read.**

## Flow D — the data flow

The flow the capability list does not describe at all, and the one sync **B4** exists to settle. What
follows is the **requirements** view: what must be true of the data's movement. Which store owns what
is `B3`'s placement decision, and the system of record is `B4`'s.

### D1 — Source enters

Source arrives either from local disk (local shape) or from a remote (service shape). In both cases
the *only* authority for what the code says is the source itself; every downstream structure is
derived from it.

### D2 — Ingestion produces the graph

```text
source files
  → in-scope file set                (detection)
  → syntax trees                     (parsing, per language)
  → nodes + edges, single-file       (extraction, to a stated depth)
  → nodes + edges, cross-file        (resolution: imports, inheritance, overrides, wiring)
  → graph
```

**The correctness tension, stated plainly:** cross-file resolution needs data from files that did not
change. That is what makes naive per-file incrementality wrong, and it is why `FR-011` specifies that
the incremental decision is taken **before** the expensive work rather than that the work is
per-file. The requirement is that the *compute* set be decidable, not that it be one file.

### D3 — Derivation produces structures that are not in any file

```text
graph
  → clusters      (whole-graph partitioning)
  → flows         (execution chains)
  → embeddings    (per embeddable node, via the embedding provider)
  → lexical index (per indexed text)
```

**Two properties of this stage drive requirements:**

- **Clusters and flows are global.** One added node can change a partition that no changed file
  touches. If their identifiers are part of the query surface, recomputation changes *answers*
  (`questions/0004`, `GAP-007`).
- **Embeddings and lexical indexes are derived and droppable**, but only if something can rebuild
  them. They must never be the only copy of anything.

### D4 — Persistence and the generation marker

All outputs of one analysis run are written under one **index generation**. The requirement is not a
particular transaction model — it is that a reader can tell which generation it read, and cannot see
two at once.

| Data kind | Class | Consequence |
|---|---|---|
| Graph nodes and edges | authoritative or derived, per `B4` | If derived from source, rebuildable; if authoritative, must be migrated on upgrade |
| Clusters and flows | derived — but with externally-visible identities | Rebuildable in principle; **not** freely rebuildable if identities are held by consumers |
| Embeddings | derived | Rebuildable, at the cost of a provider call per node |
| Lexical index | derived | Rebuildable from stored text |
| Repository registry, group registry, job state, audit records | **authoritative** | Cannot be reconstructed from source. Must survive upgrade and must be backed up. |

**The audit trail and the job state are the only data in the system that no amount of reindexing can
recover.** That is a load-bearing asymmetry and it is easy to miss when the graph is what everyone is
thinking about.

### D5 — Writes ordered across stores

Two stores updated non-atomically will diverge. The requirements are:

1. **Delete-before-orphan.** A vector, a lexical entry or a derived structure whose subject no longer
   exists is a **wrong answer**, not a leak. Removal ordering must make that unreachable.
2. **Divergence must be detectable** — by generation marker, checksum, or a reconciliation pass. Which
   is `B4`'s choice; that one exists is a requirement.
3. **A reader sees one generation.** Never a mixture (`COR-4`).

### D6 — Invalidation

```text
change detection  →  what changed  →  what must be recomputed  →  what must be deleted
```

Deletion is the half that gets forgotten. A symbol removed from source must lose its node, its edges,
its embedding, its lexical entries, and its membership of every derived structure — or it will be
returned by a search that has no idea it is gone.

### D7 — What crosses a network hop, and what that costs

| Hop | Local shape | Service shape |
|---|---|---|
| Reader → serving | in-process | network |
| Serving → graph store | in-process | network |
| Serving → vector store | in-process | network |
| Serving → relational store | in-process | network |
| Ingestion → embedding provider | network (unless a local runtime) | network |
| Acquisition → git remote | network | network |

**Consequence for the budgets:** a single logical read that touches three stores is one in-process
call in the local shape and three network round trips in the service shape. `PERF-2` states the
budget for the shape that has to pay for them, and `analysis/0005` records that this is why the two
shapes have different budgets rather than one shared number.

## Flow E — the developer flow

The other commonly-skipped flow. This is the experience of P5, and it is the flow that decides whether
the extensibility requirements are real.

### E1 — Build and test without an external engine

1. Developer clones, builds, and runs the test suite.
2. **No external store, no network, no credential, and no model download is required** for the
   default suite to pass.
3. The default store backend is in-process. House precedent, cited not mandated: per-backend feature
   flags with an in-memory default.

**Why it is a requirement and not a nicety:** a test suite that needs a networked engine is a test
suite that runs in CI and nowhere else, and the conformance suite that makes the stores genuinely
swappable is exactly the suite most likely to be skipped.

### E2 — Add a language

1. Developer implements the extraction contract for a new language.
2. They register it. **No fork, and no change to any existing language's code.**
3. A conformance suite tells them what depth of extraction they have achieved, per capability, rather
   than pass or fail.
4. Where a language is **declarative** — infrastructure and configuration formats — most of a
   general-purpose extraction contract is meaningless, and a lighter path must exist. Requiring
   inheritance resolution from a configuration format is how that support never gets built.

**Open (sync C1):** whether a second, language-server-backed analysis path exists at all. It is not a
configuration flag — an extraction contract shaped around syntax-tree access cannot be satisfied by a
language server, so this is a second architecture and must be decided as one.

### E3 — Add a store backend

1. Developer implements the capability profile for one slot.
2. They run **one conformance suite** that every backend for that slot must pass.
3. Passing it is what makes the slot swappable. Failing one case means the backend is not usable,
   not that the case is optional.

**The requirement this creates:** the conformance suite must be part of the published contract, not an
internal test. A backend author outside this repository has to be able to run it.

### E4 — Consume `<ENGINE>` from another tool

1. Developer depends on the engine library and calls it directly.
2. The public contract mentions **no concrete datastore type** — so the caller is not forced into a
   backend choice by a type signature.
3. The caller accepts AGPL-3.0 by linking. That is a licence consequence, stated up front, and it is
   the reason `questions/0005` exists.

### E5 — Understand a failure

1. Something returns `undetermined`, or a job fails, or a store diverges.
2. Telemetry says which stage, which store, which repository, which generation, and which principal.
3. Without this, the concurrency property, the latency budget and staleness are all unverifiable —
   which is why telemetry is the one engineering-practice concern that blocks requirements
   (`GAP-004`, sync **D1**).

## Cross-flow observations for the architect

Recorded here because they fall out of the flows and are exactly the input to module decomposition —
without proposing a decomposition.

1. **Flows U and G traverse the same capabilities and differ in presentation, budgeting and identity.**
   One internal contract with thin per-surface projections is the shape that keeps them consistent;
   per-surface implementations are how they diverge. Sync **B5** decides; the prior art shows the
   failure mode — two entry points to nominally the same functionality with different authentication,
   different concurrency behaviour and different operation inventories.
2. **Flow A barely intersects Flows U and G.** Admin capabilities share almost no state with read
   capabilities: different stores, different consumers, different change rate. This is the cleanest
   seam visible from the flows.
3. **Flow D's authoritative/derived split does not follow the store split.** Job state and audit
   records are authoritative and relational; the graph may be derived. Any clustering that groups
   "everything relational" together will merge concerns with opposite durability requirements.
4. **Flow E's conformance suites are a deliverable, not a test artefact.** Two of them — extraction
   depth and store-slot conformance — are how two different extensibility requirements are verified,
   and both must be externally runnable.
5. **The read/write asymmetry is visible in every flow.** 27 read capabilities against 5 writes, with
   ~10 000 read-heavy consumers against a handful of writers. `discussions/0002` develops this.

## Verification

### What is proven

- **All five flows required by the architect are present** — U, A, G, D, E — and the data and
  developer flows are the two longest, which was the stated risk.
- **Every flow step maps to a capability in `analysis/0001`.** Checked by walking the flows against
  the inventory; no step depends on a capability that is not inventoried.
- **The persona set covers the four user-story audiences** in `07-use-cases.md` — admin, developer,
  agent, non-technical — plus P5, who is not a story audience but is a real consumer.
- **The network-hop table is derived from the store slots and the two shapes**, so it cannot drift
  from `EXT-1`–`EXT-6` without one of them changing.

### What is NOT proven

- **That these are the flows the requester recognises.** They are reconstructed from the capability
  list and the two deployment shapes. Sync **A1** tests them.
- **That P4's needs are satisfiable by a web-UI contract alone.** Asserted. If presenting cluster and
  flow information without graph vocabulary turns out to need a distinct analysis capability, a
  capability is missing from `analysis/0001` and this is where it will surface.
- **Flow D's ordering requirements are stated without a chosen mechanism.** Deliberate — `B4` owns
  the mechanism. But it means D5 is currently unverifiable: there is no way to test "divergence is
  detectable" before deciding how it is detected.
- **The volumes and latency sensitivities per persona are estimates**, not measurements. They come
  from the requester's ~20–50 humans and ~10 000 agents, and everything finer-grained is inference.
- **Flow E has no user.** No external backend author or language author exists yet, so every claim
  about their experience is untested. The first real one will find things this section got wrong.

## Amendments

- **2026-08-20** — Created.

## Related

- [`00-overview.md`](00-overview.md) — the stages the flow steps refer to, and the deployment duality.
- `analysis/0001-capabilities.md` — the capabilities every step maps to.
- `discussions/0002-read-write-asymmetry.md` — cross-flow observation 5, developed.
- [`07-use-cases.md`](07-use-cases.md) — these flows as numbered user stories and stepped use cases.
