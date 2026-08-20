# Analysis 0004 — Store capability matrix and the async screening record

- **Date:** 2026-08-20 · **Status:** input to syncs **B2**, **B3** and **B7**
- **Purpose:** two jobs in one document, because they must be answered together. First, the six store
  slots as a comparison matrix — what each must do, what an embedded and a networked implementation
  each look like. Second, **the async screening record**, because `EXT-9` requires it and sync **B7**
  cannot run without it.
- **Vocabulary:** [`GLOSSARY.md`](../GLOSSARY.md). Product names here are `presumed` compatibility
  targets (`questions/0010`), not selections.

## Why one document

The storage seam is described in `PROMPT.md` as the single most consequential one, and the async
question is the decision that seam forces. House rule: *if any candidate backend is async-only, the
trait is async and everything above it inherits that — resolve during screening, never after.*
Separating the matrix from the screening is how a slot gets chosen on capability grounds and then
discovered to force a rewrite.

## The six slots

### Capability profile per slot

| # | Slot | Required operations | Optional | Consumers |
|---|---|---|---|---|
| 1 | **Graph** | typed directed edges between typed nodes with properties; openCypher-shaped read queries; bounded variable-length paths; filter by node type and edge class **in** the query; bulk load; delete a subgraph by identity; generation isolation for reads | lexical ranking; vector search | 24 read capabilities, 12 write |
| 2 | **Vector** | store fixed-width float vectors keyed by node identity; nearest-neighbour by cosine distance with a limit and a distance threshold; delete by key; count | payload filtering; multiple named vectors per key | 2 read, 2 write |
| 3 | **Relational** | transactional read and write; unique and foreign-key constraints; ordered pagination; append-only insert; durable job records | — | 11 read, 7 write |
| 4 | **Search** | index documents with fields; query with filters; ranked results with scores; **plus everything from the retired slot 5: tokenise and index text per document, lexical ranking, a stemming policy, delete by document, and per-document update** | aggregations; phrase and proximity queries | **1 read, 2 write** — `FR-017`, `FR-021`'s lexical lane |
| 5 | ~~**Text-search**~~ | **slot dropped 2026-08-20.** Profile merged into slot 4; `EXT-5` is now a recorded `WON'T` | — | — |
| 6 | **Key-value** | get; set with expiry; delete | compare-and-set | **none** |

### Embedded versus networked, per slot

| # | Slot | Embedded looks like | Networked looks like | Required in v1? |
|---|---|---|---|---|
| 1 | Graph | in-process property-graph engine, single file or directory | separate openCypher-speaking service | **yes, both** (`REV-2`) |
| 2 | Vector | in-process index, persisted alongside the graph | separate vector service — **Qdrant** (Apache-2.0), already run in this estate | **yes, both** |
| 3 | Relational | embedded single-file SQL engine | networked SQL server | **yes, both** |
| 4 | Search | **unnamed — `GAP-021`** | **OpenSearch** (Apache-2.0) | **yes, and it now carries `FR-017`** |
| 5 | ~~Text-search~~ | dropped 2026-08-20 | — | — |
| 6 | Key-value | in-process map | networked key-value server | no — no consumer |

### The three findings this matrix produces

> **Amended 2026-08-20.** Findings 1–3 below were written when six slots existed and the search slot had
> no consumer. The requester has since **dropped text-search and placed lexical ranking in the search
> slot**. Net effect: finding 1 is now half-true (key-value only), finding 2 is **void** — slot 5's
> optionality is moot because slot 5 is gone — and finding 3 is **resolved rather than relocated**, since
> a general-purpose search engine satisfies per-document update natively. The findings are kept as written
> with this note, because the reasoning is what justifies the new placement.

**Finding 1 — two slots have no consumer.** Slots 4 and 6 are required by the capability list and
consumed by no capability in `analysis/0001`. An abstraction with no consumer cannot be validated,
and its conformance suite would be testing an interface nobody calls. Filed as `GAP-011`. The
recommendation is to specify them and not build them until a consumer exists — which is what
`EXT-4` and `EXT-6` do.

**Finding 2 — slot 5's optionality is not slot 5's decision.** `FR-017` requires a lexical index.
Whether it lives in the graph engine or in a dedicated slot is `B3`'s placement decision. So slot 5 is
**required if and only if the chosen graph engine cannot rank lexically** — and that is decided by
slot 1's selection, not by slot 5's. This coupling is easy to miss and it means the two slots must be
screened together.

**Finding 3 — one operation in slot 5 is load-bearing and is commonly absent.** **Per-document
update.** An engine offering only whole-index create, drop and query forces full re-tokenisation of the
corpus on every index run, which directly contradicts `PERF-6` and `FR-012`. The grounding measured
exactly this in the reference implementation: its lexical indexes were dropped and rebuilt on every
run, incremental path included, because the engine exposed no per-row primitive. **This is why
`EXT-5`'s profile lists per-document update as required rather than optional** — a candidate lacking it
must be screened out, not adopted and worked around.

## The portability hazards, per slot

These are the specific things that make a slot's abstraction leak. Each is a design input for `B2`.

| Slot | Hazard | Consequence if ignored |
|---|---|---|
| Graph | **Dialects agree on read traversal and diverge on everything else** — schema definition, bulk load, index creation, extensions, and even the return type of standard functions. | A contract expressed as "we send query strings" is not portable, because the portable statements are the ones you send least. |
| Graph | **Edge kind as a relationship *type* versus as a *property*.** Some engines index by relationship type; some can carry kind as a property on one type. | Modelling edge class as a property makes the most common filter in the system unable to use the primary index on engines that index by type. **This is a `B3` decision with portability consequences and it must precede any schema.** |
| Graph | **Bulk load is engine-specific**, and it is the operation a full rebuild depends on. | The full-rebuild path is the least portable path, and it is the one `PERF-7` budgets. |
| Vector | **Width is frozen at creation.** | Changing embedding provider is a migration event, not a config change (`questions/0008`). |
| Vector | **Approximate search returns fewer results, silently.** | An index with wrong parameters is indistinguishable from an empty store unless recall is asserted against a brute-force oracle on a small fixture. |
| Relational | **This slot holds every piece of authoritative data** — repository and group registries, job state, audit records. | "Drop and rebuild" is not an available recovery here, unlike every other slot. Backup and migration matter most, and matter least everywhere else. |
| Text-search | **Per-document update** — see finding 3. | Contradicts incrementality. |
| Text-search | **Tokenisation is engine-specific**, and read and write must use the same composition. | A mismatch between index-time and query-time tokenisation returns nothing for inputs that should match, with no error. |
| All | **Read-during-write semantics differ.** | `COR-4` (no torn reads) may be satisfiable by the engine on one backend and require our own generation isolation on another — which means it is a *contract* requirement, not a backend capability to rely on. |

## The async screening record

### Status: graph slot screened on registry evidence 2026-08-20; concurrency still unscreened

**The candidate list arrived on 2026-08-20** (`questions/0010`), and the graph slot's first pass is in
[`0008-graph-slot-screening.md`](0008-graph-slot-screening.md) — licence, maintenance, adoption and shape
for all ten candidates, with four declined on specific disqualifying facts and one, `kin`, unidentifiable.

**It does not answer the async question.** Client concurrency model is not in registry metadata, so
nothing below has changed: `EXT-9`'s concurrency record remains empty and `questions/0003` remains
unanswerable from what has been screened.

**The cheapest route to the async answer is now clear, and it is not the graph slot.** If **both** vector
candidates — Lance and Qdrant — are async-only, the trait is async by that slot alone, whatever the graph
slot turns out to be. That is two checks rather than ten, and it unblocks **B7** on its own. The relational
pair is the counterweight worth knowing about: PostgreSQL has a genuine blocking Rust client rather than a
facade over a runtime, so that pair does **not** force the answer either way.

This section defines the procedure and records the one inference strong enough to be worth stating, so
sync **B7** starts from something rather than nothing.

### The procedure

For each candidate, record:

| Field | Values |
|---|---|
| Client concurrency model | synchronous only · asynchronous only · both |
| If both, is the sync path a wrapper? | yes — a blocking wrapper over an async runtime · no — genuinely sync |
| Runtime coupling | none · requires a specific async runtime · runtime-agnostic |
| Blocking-call risk | does the client perform blocking I/O that would stall an async executor? |

**Why "both" is not automatically the easy answer:** a synchronous facade implemented by blocking on an
async runtime brings the runtime as a dependency and creates a nested-runtime hazard when the caller is
itself async. That is a different situation from a genuinely synchronous client, and the screening must
distinguish them.

### ✅ Screened 2026-08-20 — the vector pair settles it

**Both halves of the vector slot are asynchronous-only, on the same runtime.**

| Candidate | Role | Evidence | Sync API? |
|---|---|---|---|
| **Qdrant** (`qdrant-client`) | networked half | every method `async fn`; `tokio` a **non-optional** dependency; gRPC over `tonic` | **none** — no blocking API, no sync feature |
| **Lance** (`lancedb`) | embedded half | builder methods terminate in `.execute().await`; depends on `tokio` | **none documented** |

`REV-2` requires **both** halves of the vector slot before v1. Neither offers a synchronous interface.
So the persistence layer above them is async, and **that conclusion holds whatever the graph slot turns
out to be** — which is why this was worth checking first: two lookups rather than ten.

**The relational pair is the counterweight, and it does not change the answer.** PostgreSQL has a genuine
blocking Rust client rather than a facade over a runtime, so that pair would have permitted either choice.
It is outvoted by a slot whose candidates permit only one.

**What this costs, stated because `questions/0003` requires the disliked consequence to be named:** the
**local shape pays**. It carries an async runtime it would otherwise not need, and every synchronous
embedded engine — a graph engine, an embedded SQL engine — needs an explicit offload strategy. Getting
that wrong puts a blocking call inside an async task, which stalls the executor precisely under the
concurrent load `PERF-1` exists to measure, and it is invisible until then.

**Still unscreened:** the graph and relational slots' clients, and whether either embedded candidate is
pure Rust or an FFI binding. Those affect the offload design; they no longer affect the async decision.

### The inference this replaces, kept for the record

**Mainstream Rust clients for networked services are predominantly asynchronous**, and where a
synchronous interface exists it is usually a blocking facade over an async runtime rather than an
independent implementation. `REV-2` requires at least one **networked** implementation for the graph,
vector and relational slots in v1.

**If that inference holds, the store trait is async, and everything above it inherits that.**

This is stated as an inference and not as the decision, for three reasons:

1. **It has not been checked.** No client has been examined. The grounding contains no Rust client
   screening because the reference implementation is not Rust.
2. **Embedded engines pull the other way.** An in-process graph or SQL engine is very likely
   synchronous, and an async trait over a synchronous embedded engine means either a blocking call
   inside an async function — which stalls an executor and is a real defect — or a thread-pool
   offload for what is a memory access.
3. **It is `B7`'s decision, not this document's**, and stating it as settled here would be exactly the
   pre-emption `CON-8` forbids.

**The uncomfortable shape of the answer, recorded so nobody is surprised by it:** the two halves of the
deployment duality point in opposite directions on this question. The networked backends the service
shape needs likely force async; the embedded backends the local shape needs are likely synchronous and
are penalised by it. Whatever `B7` decides, one shape pays. **That cost should be named in the ADR
rather than discovered**, per the house convention of recording the consequence you dislike.

### What the answer changes

| If the trait is… | Then |
|---|---|
| **async** | Every caller above it is async, up to and including the CLI's entry point. The local shape carries an async runtime it may not otherwise need. Embedded synchronous engines need an offload strategy, and getting that wrong stalls the executor under exactly the concurrent load `PERF-1` requires. |
| **synchronous** | Networked clients need a blocking bridge, which either brings a runtime anyway or restricts the candidate set to genuinely-synchronous clients. `SCALE-4`'s 64 concurrent in-flight reads per replica would then be served by threads rather than tasks, which is a capacity and memory question rather than a correctness one. |
| **both, by feature** | Two code paths above the seam, which is the option that looks cheapest and is not: it doubles the conformance surface and is the shape most likely to diverge (`IF-1`'s failure mode, one layer down). |

**None of these is free**, and the third is the one to be most suspicious of.

## Conformance suite — one per slot

`COR-6` and `QA-7`. What the suite must establish, beyond the operations in the profile:

| Property | Why it belongs in the suite rather than in a backend's own tests |
|---|---|
| Operation semantics | It **is** the slot definition. A backend passing a subset is not usable. |
| Ordering and pagination stability | Two backends that page differently produce different answers to the same query. |
| Deletion completeness | `FR-012`'s orphan requirement — a leftover vector or lexical entry is a wrong answer, not a leak. |
| Read isolation during write | `COR-4`. Whether the engine provides it or we must, the suite asserts the property either way. |
| Error classification | A caller must distinguish "not found" from "unavailable" from "malformed" identically across backends, or `OPS-7`'s explicit degradation cannot be implemented. |
| Recall, for approximate indexes | Against a brute-force oracle on a small fixture. |
| Externally runnable | `QA-7` — a backend author outside this repository must be able to run it. |

**Six suites, not one**, because the slots share no operations. What they share is the *shape* of the
suite and the requirement that passing it is binary.

## Placement — deliberately not decided

Which store owns which data is sync **B3**'s placement table, and `analysis/0001` states that a store
column there means "this capability needs this shape of access", never "this data lives here".

What this document does record, because it follows from requirements rather than from design:

| Data kind | Class | Consequence |
|---|---|---|
| Repository registry, group registry, job state, audit records | **authoritative** | Must be migrated on upgrade; cannot be rebuilt; must be backed up (`FR-073`, `REV-3`, `SEC-6`) |
| Nodes and edges | authoritative **or** derived — `B4` decides | If derived from source, rebuildable; if not, migratable |
| Flows and clusters | derived, **with externally-visible identities** | Rebuildable in principle; **not** freely rebuildable if consumers hold their identities (`questions/0004`) |
| Embeddings | derived | Rebuildable at the cost of a provider call per node |
| Lexical entries | derived | Rebuildable from stored text |

**The row that constrains most is the third**, and it is the one that looks least constraining.

## Verification

### What is proven

- **All six slots have a capability profile**, and each profile is stated as operations rather than as a
  dialect or a product.
- **Three findings are derived from the matrix itself** — two slots with no consumer, slot 5's
  optionality being slot 1's decision, and per-document update being load-bearing. The third is
  evidenced by a measured failure in prior art.
- **The async screening record honestly states that screening has not started**, defines the procedure,
  and names the one inference worth acting on while marking it as an inference.
- **The two halves of the deployment duality are identified as pulling in opposite directions on
  async**, which is the disliked consequence `B7`'s ADR must record.

### What is NOT proven

- **No candidate has been screened for anything** — not async, not licence, not the capability profile.
  Every product named is `presumed` (`questions/0010`, `GAP-010`).
- **The capability profiles are untested against any real engine.** Whether one contract can span an
  embedded and a networked implementation of the same slot without leaking either is the central bet of
  the storage abstraction, and this document does not establish it.
- **The graph slot's profile is the least confident.** Its hazard list says dialects diverge outside
  read traversal, which is itself an argument that the profile's operations may not be expressible
  uniformly. That tension is unresolved.
- **No conformance suite exists**, so "passing it is binary" is a requirement rather than an observation.
- **The authoritative-versus-derived table pre-empts nothing about placement** and therefore leaves the
  hardest question — the system of record — entirely to `B4`.

## Amendments

- **2026-08-20** — Created.

## Related

- `specs/04-interfaces-and-external-systems.md` — `EXT-1`–`EXT-9`, the requirements this matrix expands.
- `questions/0003-the-async-decision.md` — the decision this record feeds.
- `questions/0008-embedding-provider-and-vector-width.md` · `questions/0010-store-compatibility-targets.md`
- `SYNCS.md` — **B2** abstractions, **B3** data models and placement, **B7** async.
