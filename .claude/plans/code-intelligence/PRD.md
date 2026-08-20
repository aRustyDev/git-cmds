# PRD — code intelligence (`git-ctx` and `<ENGINE>`)

> **Aspirational.** States what should become true, not what is. Drafted 2026-08-20. Unapproved.
> Vocabulary is as ratified in [`GLOSSARY.md`](GLOSSARY.md). `<ENGINE>` is a deliberate placeholder
> and is not to be resolved before sync B6.

## Problem

Engineers and — increasingly — fleets of agents work on codebases they cannot hold in their heads,
and the tools they have answer the wrong shape of question. Text search finds occurrences of a
string. A language server answers questions about the file you have open. Neither answers the
questions that actually gate a change:

- *If I change this function, what breaks?*
- *What is the path from this HTTP route to that database write?*
- *Which of these 400 files does my diff actually reach?*
- *Where does this behaviour live, when I can only describe it in a sentence?*

Those are **graph** questions. Answering them means parsing a repository into a queryable knowledge
graph of symbols and their relationships, and then serving that graph to two very different
consumers: humans, who want to look at it, and agents, who want to interrogate it thousands of times
an hour under a token budget.

The second half of the problem is that **an answer nobody can trust is worse than no answer.** An
empty result that means "nothing is affected" and an empty result that means "the walk could not see"
are indistinguishable unless the system is built to distinguish them — and an agent acting on the
first when the truth was the second will confidently ship a breaking change.

## Why now

**A capable reference implementation exists and cannot be used.** It is licensed PolyForm
Noncommercial 1.0.0; its licensor confirmed in writing that internal use at a for-profit company
requires a paid commercial licence. That closed the path this effort originally took, and the
alternatives were: buy the licence, compose three or four permissively-licensed tools that together
cover perhaps two-thirds of the capability, or stop.

A clean-room reimplementation under this repository's **AGPL-3.0** licence is a fifth option, and the
only one that keeps every capability without a recurring licence or a fragmented multi-tool
composition. It is expensive, and the honest comparison is not "free versus paid" — it is "build,
versus buy, versus accept a materially smaller capability set."

Two things make now the right time rather than a year ago:

1. **The agent fleet is the new primary consumer, and no surveyed prior art was designed for it.**
   Everything available was built for a human at a keyboard, then had an agent protocol bolted on.
   Machine-readable confidence, stable identifiers across runs, budget-aware truncation and batch
   queries are not features anyone retrofits well.
2. **The grounding is already done.** A prior effort measured the reference implementation's
   behaviour in detail before the licence verdict landed. That produced a set of **measured failure
   modes** — see *Inherited negatives* below — which is a far better starting point than a blank
   page, and which expires in usefulness the longer it sits unused.

## Users

- **Developer / engineer (primary human user).** Wants to understand unfamiliar code and to know what
  a change reaches before making it. Judges the product on whether the answer arrives fast enough to
  stay in flow, and on whether it can be trusted when it says "nothing".
- **AI agent (primary consumer by volume).** Up to ~10 000, predominantly read-only. Needs terse,
  machine-readable, budget-bounded answers; stable identifiers it can hold between calls; and an
  explicit signal when a result is inconclusive. Cannot read prose caveats.
- **Platform administrator.** Runs the service shape. Owns repository acquisition and credentials,
  repository groups, the store backends, the identity integration, the AI-provider policy, and index
  capacity. Their failure modes are the ones that take everyone else down.
- **Non-technical stakeholder.** Product, programme and engineering-management readers who want the
  wiki, the cluster map, and "which teams does this change touch" — without a graph query language.
- **Platform developer / integrator.** Builds on `<ENGINE>` directly, adds a language, or embeds the
  capability in another tool. A real user even before anyone else exists.

## Goals and success criteria

| # | Goal | Done when |
|---|---|---|
| **G1** | A repository becomes a queryable graph | A repository of at least the scale target in `specs/03` indexes to completion, and node and edge counts are reportable by type. |
| **G2** | The four analysis questions are answerable, and distinguishable | Reachability, blast radius and diff impact each return the **three-state result**, with the edge set and depth bound stated in the response. No projection can report a clean negative that was actually a truncation. |
| **G3** | Diff impact works for a pull request | A supplied patch, for a repository the service has never checked out, yields a diff-impact answer. No local working tree involved. |
| **G4** | Agents are first-class, not adapted | The agent surface returns the same answers as the human surface from **one internal contract**, with per-principal identity, budget-bounded output, and stable identifiers across index generations. |
| **G5** | Reads scale with readers | On one replica, N concurrent independent reads complete in wall-clock materially better than N times a single read, with no monotone latency staircase. Measured, not asserted. |
| **G6** | Indexing is queued work, not a lock | Two repositories can be submitted for indexing concurrently; neither is rejected; both are observable, cancellable and durable across a restart. |
| **G7** | Incrementality is decided before the cost is paid | For a one-file change in a large repository, the work performed is proportional to the change. Verified by instrumenting what was skipped, not by wall-clock alone. |
| **G8** | The stores are genuinely swappable | Every store slot passes one conformance suite against at least two implementations, one embedded and one networked, with **no change to business logic**. |
| **G9** | Both deployment shapes exist from one design | The local shape is a single binary with embedded stores, no authentication and no network listener. The service shape is authenticated, externally-stored and horizontally scalable. Neither is a fork of the other. |
| **G10** | The web UI meets its budget as a contract | A defined query set returns within the n95 budget in `specs/03`, measured at the contract boundary the UI consumes — so the budget is the crates' obligation, not the frontend's. |
| **G11** | Identity answers "who asked for this" | Every request carries exactly one principal, and every mutating action produces an audit record naming it. Not answerable in principle is not acceptable. |
| **G12** | A version upgrade does not force a reindex | Upgrading across a schema change migrates the index. A full reindex on upgrade is a defect, not a release note. |

## Must / should / won't (v1)

- **Must:** G1–G12. The three-state result contract. Per-principal identity in the service shape.
  AST-accurate rename with index writeback. One implementation of rank fusion. Queued, durable,
  cancellable indexing. Freshness on every analysis answer. All six store slots specified as
  capability profiles, with at least the graph, vector and relational slots implemented in both an
  embedded and a networked form.
- **Should:** the search index and text-search index slots implemented rather than merely specified
  (no required capability consumes them today — see `GAP-011`). Declarative
  infrastructure-and-configuration analysis at useful depth. Runtime AI-provider configuration from
  the web UI. A terminal surface, if `questions/0009` decides for it.
- **Won't (v1):** statement-level **dependence** and persisted **taint** findings — deferred by the
  requester on 2026-08-20, with the contract seam named in `specs/02` so they insert rather than force
  a redesign. Also won't: a hosted multi-organisation offering; write operations beyond coordinated
  rename; a graph query language of our own design; source-code editing beyond rename; anything that
  requires exposing the service outside the organisation (see the AGPL §13 constraint).

## Constraints

- **AGPL-3.0, with two consequences that shape the module split.** Internal consumers must accept
  AGPL to **link** the libraries, and §13 binds if the service is ever exposed beyond the
  organisation. Full statement in `specs/06-constraints.md`; `questions/0005` carries the open half.
- **Clean room.** No source of the reference implementation may be read by anyone implementing this.
  The requirements author who read the grounding research is tainted and must not implement. This is
  not hygiene: PolyForm's *No Other Rights* clause forbids sublicensing, so a derivative work could
  not be released under AGPL-3.0 **at all**, and the clean room is what makes the licence coherent.
- **Two deployment shapes, one design.** Not two configurations — two points a single design must
  reach. The local shape has one user, no authentication and no network hop; the service shape has
  ~20–50 humans, up to ~10 000 agents, external stores and authenticated per-principal access.
- **Six store slots, each embedded-or-networked, with no business-logic change.** The single most
  consequential seam in the system, and nothing in the requester's module sketch owns it.
- **The async decision is forced by the store abstraction and must be taken during backend
  screening.** House rule: if any candidate backend is async-only, the trait is async and everything
  above it inherits that. Retrofitting async through a synchronous trait is a rewrite. Filed as
  `questions/0003`; sync **B7** owns it.
- **The web UI is a downstream consumer, specified by contract.** Its implementation technology is
  deliberately unchosen, and its performance budget is an obligation on the crates beneath it.
- **House Rust conventions bind** and pre-answer several questions: persistence behind a repository
  trait with no concrete datastore type in the public API; per-backend feature flags with an
  in-memory default so tests need no external engine; typed errors in libraries.
- **`git-ctx` is the CLI name and is decided.** The engine library is deliberately unnamed until sync
  B6, because a library name is a claim about scope and scope is what the seam work decides.

## Inherited negatives — the most valuable thing this project inherits

Eleven requirements exist because a specific failure mode was **measured** in the reference
implementation, not because anyone imagined it. Reproducing them would waste the whole exercise, so
each is written as a positive requirement with a verification method, and each is marked
`(VERIFIED)` — meaning the *need* is evidenced, not that the solution is built.

| # | The requirement | Because, measured |
|---|---|---|
| 1 | Concurrent reads scale with readers per replica (`PERF-1`) | Every API read funnelled through one process-wide mutex against a single open database handle, producing a clean FIFO latency staircase under concurrent load. |
| 2 | Simultaneously-served repositories are bounded by capacity, not a constant (`SCALE-3`) | Resident repositories capped at a small integer with LRU eviction, where eviction cost a full database reopen. |
| 3 | Indexing is queued, durable and cancellable (`FR-068`) | One repository's index run rejected every other repository's, in memory, with no queue and no durable job state. |
| 4 | Incrementality is decided before the expensive work (`FR-011`) | The full parse-and-analyse pipeline always ran to completion; only *then* was the incremental-versus-full decision taken, and only the database write was incremental. |
| 5 | Global partitioning does not force full recomputation, and derived identities are stable (`FR-018`) | Whole-graph partitioning and derived-flow extraction were recomputed wholesale every run, while their identifiers were primary keys of the query surface — so recomputation changed *answers*, not just cost. |
| 6 | Identity is per-principal, never a shared secret (`SEC-1`, `SEC-3`) | The only credential was one static shared token with no claims and no expiry, validated at an edge proxy that stripped it before the upstream hop — making "which agent asked for this?" unanswerable *in principle*. |
| 7 | Authorisation fails closed (`SEC-7`) | An unset token authorised every request, and a contended global registry lock degraded to unlocked with a logged warning and a possible lost update. |
| 8 | Rename is AST-accurate and updates the index (`FR-050`) | Rename was a whole-file word-boundary regex that rewrote comments and string literals, wrote nothing back to the graph, and silently swallowed its search tool's failure. |
| 9 | Rank fusion has exactly one implementation (`FR-071`) | Result fusion was implemented three times, with divergent effective constants and different join keys — so the same query answered differently depending on which surface asked. |
| 10 | A version upgrade does not force a full reindex (`FR-073`) | A schema-fingerprint change disabled incrementality entirely, and the parse cache was keyed on the package version — so every release reindexed everything. |
| 11 | The advertised inventory equals the callable inventory (`IF-4`) | Three callable operations never appeared in the advertised tool list, so an allowlist built from the advertisement silently missed them. |

## User flows

Summarised here; specified in full, for all five audiences, in `specs/01-personas-and-flows.md`.

**Flow A — human comprehension.** Developer names a symbol or describes behaviour → hybrid search or
symbol view → navigates references and flow participation → optionally scopes to a sub-directory.

**Flow B — change safety.** Developer or agent supplies a change set → diff impact under a stated
edge set and depth → three-state result with projections → optionally a witness path for any
individual reach.

**Flow C — agent interrogation.** Agent authenticates as itself → discovers repositories → issues
many bounded reads across a session → receives stable identifiers and explicit freshness on each.

**Flow D — administration.** Admin acquires a repository, submits it for indexing, watches the job,
configures store backends and identity, sets the AI-provider policy, and reviews the audit trail.

**Flow E — data.** Source enters ingestion, becomes graph plus derived structures plus vectors plus
lexical indexes, is served to readers, and is invalidated by change detection. Which store owns what,
what is authoritative versus derived, and the write ordering across stores are sync **B3**/**B4**
decisions; the requirement is that exactly one system of record exists and is named.

## Dependencies

- Rust stable. The workspace layout, crate boundaries and dependency set are **the architect's
  deliverable**, deliberately not proposed here.
- A parsing strategy with a per-language extraction contract, and a decision on whether a second,
  language-server-backed analysis path exists at all (sync **C1**).
- Six store slots, each with at least one embedded and one networked implementation. Candidate
  products are compatibility targets, marked `presumed`, in `specs/04` and `analysis/0004`.
- An embedding provider, with the vector-width policy settled (`questions/0008`).
- An identity provider for the service shape — OAuth2 or JWT — and optionally an external
  authorisation decision point (RBAC, ABAC or ReBAC).
- Telemetry, without which G5, G7, G10 and index staleness are unverifiable. Sync **D1**; `GAP-004`.
- A structural-diff decision (sync **C3**) before diff impact's input contract is fixed, because
  mapping a *line* diff onto symbols is lossy exactly when the change was a move.

## Out of scope

Named, not categorised — a scope statement that only describes categories lets a component be
silently dropped and later called "never in scope".

- **Statement-level dependence and taint** in v1. Deferred, with the seam named. Revisit trigger:
  a consumer asks for source-to-sink reasoning that blast radius cannot answer.
- **A hosted, multi-organisation offering.** The service shape is single-organisation. Multi-tenancy
  beyond repository-scoped authorisation is not specified.
- **Exposing the service beyond the organisation.** Not a capability decision — an AGPL §13 one.
- **Source editing beyond coordinated rename.** No codemods, no mechanical migrations, no
  refactoring suggestions in v1. `GAP-006` holds the opportunity; sync **A4** owns it.
- **A query language of our own.** The graph query surface is openCypher-shaped because that is what
  the requester asked for and what candidate stores speak.
- **Deployment manifests, Helm charts and cluster plumbing.** Explicitly out of scope for this plan.
- **The web UI's implementation.** Contract and budget only.
- **A backlog system.** None exists (`questions/0002`); `GAPS.md` carries acceptance criteria inline
  until one does.

## How we will know we were wrong

Written in advance, so the failure is recognisable rather than rationalised:

- **Two components in the final design both walk the graph to answer an impact-shaped question.**
  That is exactly the split that produced two incompatible mechanisms sharing one name in the prior
  art, and `discussions/0001` exists to prevent it.
- **The capability inventory stops growing under scrutiny.** It grew by nine platform capabilities and
  three net-new requirements in one pass. An inventory that survives sync A1 unchanged was written
  from the capability list rather than from thinking about the system.
- **The store abstraction has exactly one implementation per slot at v1.** Then it is not a seam, it
  is a wrapper, and the swappability requirement was satisfied on paper only. Two implementations per
  slot is what proves it.
- **Someone reads a prose field to learn whether a result was conclusive.** The three-state contract
  has then been collapsed, and every agent consuming it is unsafe.
- **The local shape turns out to be the service shape with features disabled.** The duality was then
  treated as configuration, and the local binary will carry authentication, job queues and network
  listeners it has no use for.
- **The async question is still open when the first store implementation lands.** House rule says that
  is a rewrite, and the rule exists because it has happened.
- **Nobody hits the incrementality work.** If the roadmap makes G7 look easy, the difference between
  "the write is incremental" and "the *compute* is incremental" has not been understood — and it is
  the single largest piece of engineering in this document.
- **An agent reports high confidence on a stale index.** Freshness was then an annotation rather than
  a first-class part of the answer.

## Amendments

- **2026-08-20** — Created. Records the requester's four v1 scope decisions of the same date:
  dependence and taint deferred to v2; pull-request-shaped diff input required in v1; all seven
  previously-omitted capabilities wanted; store slots specified as capability profiles with
  `presumed` candidate products.

## Related

- [`GLOSSARY.md`](GLOSSARY.md) — ratified vocabulary; every term here is defined there.
- `specs/` — the requirements this document motivates.
- [`FEATURES.md`](FEATURES.md) — the flat feature list, traceable both ways to the SPEC.
- [`SYNCS.md`](SYNCS.md) · [`GAPS.md`](GAPS.md) — the two standing mechanisms.
- `discussions/0001-what-impact-analysis-means.md` — why "impact analysis" is not a capability.
